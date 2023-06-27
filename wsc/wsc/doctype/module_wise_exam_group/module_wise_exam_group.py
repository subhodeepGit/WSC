# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from wsc.wsc.notification.custom_notification import send_mail_to_students_mweg


class ModuleWiseExamGroup(Document):
	def validate(self):
		duplicate_validation(self)
		group_validation(self,"validate")	
		filter_group(self)
		date_validation(self)
		validate_time(self)
		self.calculate_total_hours()
		send_mail_to_students_mweg(self)

	def on_submit(self):
		group_validation(self,"on_submit")
		date_time_mandatory(self)
		time_mandatory(self)
	
	def calculate_total_hours(self):
		for d in self.get("scheduling_group_exam"):
			if d.to_time and d.from_time:
				d.total_duration_in_hours = datetime.strptime(d.to_time, '%H:%M:%S') - datetime.strptime(d.from_time, '%H:%M:%S') 	

def duplicate_validation(self):
	data=frappe.get_all("Module Wise Exam Group",{"exam_declaration_id":self.exam_declaration_id,"modules_id":self.modules_id,"docstatus":1})
	if data:
		frappe.throw("Module Wise Exam Group Has Already Been Declared")


def time_mandatory(self):
	for t in self.get("scheduling_group_exam"):
		if not t.from_time:
			frappe.throw("From Time not maintained in Exam For the Group <b>%s</b>"%(t.group_name))
		if not (t.from_time and t.to_time):
			frappe.throw("End Time not maintained in Exam For the Group <b>%s</b>"%(t.group_name))	


def validate_time(self):
	for cr in self.get("scheduling_group_exam"):
		if cr.to_time and cr.from_time:
			from_time= datetime.strptime(cr.from_time, '%H:%M:%S').time()
			to_time= datetime.strptime(cr.to_time, '%H:%M:%S').time()
			if from_time>to_time:
				frappe.throw("Row <b>{0}</b> From Time cannot be greater than To Time".format(cr.idx))

def date_validation(self):
	for t in self.get('scheduling_group_exam'):
		if t.examination_date:
			if self.module_exam_start_date<=t.examination_date and self.module_exam_end_date >= t.examination_date:
				pass
			else:
				frappe.throw("Date provided in Exam Group:- <b> %s </b> is not in between Module Exam Start Date and Module Exam End Date"%(t.group_name))	

def date_time_mandatory(self):
	idx=[]
	for t in self.get('scheduling_group_exam'):
		if not (t.examination_date or t.from_time or t.to_time):
			frappe.throw("Date Time Not Mentioned in the Exam Group :- <b>%s</b> "%(t.group_name))


def group_validation(self,method):
	idx=[]
	for t in self.get("student_list"):
		if t.examination_qualification_approval==1 and (t.group_name==None or t.group_name==""):
			idx.append(t.idx)
	if idx:
		if method=="validate":
			frappe.msgprint("Group Name not given for following Line %s"%(idx))
		if method=="on_submit":
			frappe.throw("Group Name not given for following Line %s"%(idx))			

def filter_group(self):
	group_name=[]
	for t in self.get("student_list"):
		if t.group_name:
			group_name.append(t.group_name)
	group_name=list(set(group_name))
	group_name.sort()

	present_list=[]
	for t in self.get("scheduling_group_exam"):
		a={}
		a['group_name']=t.group_name
		a['examination_date']=t.examination_date
		a['from_time']=t.from_time
		a['to_time']=t.to_time
		a['total_duration_in_hours']=t.total_duration_in_hours
		present_list.append(a)		

	if not present_list:
		for t in group_name:
			self.append("scheduling_group_exam",{
				"group_name":t
			})
	else:
		for t in group_name:
			flag="No"
			for j in self.get("scheduling_group_exam"):
				if j.group_name==t:
					flag="Yes"
					break
			if flag=="No":
				self.append("scheduling_group_exam",{                                     
					"group_name":t,                                                                   
				})

@frappe.whitelist()
def valid_module_as_exam_declation(doctype, txt, searchfield, start, page_len, filters):
	course_date=[]
	if txt:
		course_date=frappe.db.sql(""" Select courses,course_name,course_code,semester from `tabExam Courses` where parent='%s'"""%(txt))
	return	course_date

@frappe.whitelist()
def get_semester(declaration_id=None):
	sem_date=[]
	if declaration_id:
		sem_date=frappe.get_all("Examination Semester",{"parent":declaration_id},['name','semester'])
	return sem_date

@frappe.whitelist()
def module_start_date(modules_id=None,exam_id=None,academic_term=None):
	output_date=[]
	if modules_id and exam_id:
		output_date=frappe.get_all("Exam Courses",{"parent":exam_id,"courses":modules_id},
			     ['examination_date','examination_end_date',"attendance_criteria","minimum_attendance_criteria"])
		if output_date[0]['attendance_criteria']=="Yes":
			acd_date=frappe.get_all('Academic Term',{"name":academic_term},['term_start_date','term_end_date'])
			for t in output_date:
				t['term_start_date']=acd_date[0]['term_start_date']
				t['term_end_date']=acd_date[0]['term_end_date']
		else:
			for t in output_date:
				t['term_start_date']=''
				t['term_end_date']=''		
	return output_date

@frappe.whitelist()
def get_student(academic_term=None, programs=None,class_data=None,minimum_attendance_criteria=None,attendance_criteria=None,
				start_date_of_attendence_duration=None,end_date_of_attendence_duration=None,modules_id=None,
				semester=None):
	enrolled_students = get_program_enrollment(academic_term,programs,class_data)
	student_list=[]
	if enrolled_students:
		student_list=enrolled_students
		total_no_class_scheduled=frappe.db.count('Course Schedule', filters=[["course","=",modules_id],['program','=',semester],
								     ['schedule_date','between',[start_date_of_attendence_duration,end_date_of_attendence_duration]]])
		
		for t in student_list:
			t.update({"total_no_of_classes_scheduled": total_no_class_scheduled})
			class_att_date=frappe.db.count("Student Attendance",filters=[["student","=",t['student']],
								['course','=',modules_id],['program','=',semester],['program','=',semester],
								['date','between',[start_date_of_attendence_duration,end_date_of_attendence_duration]]])
			t.update({"total_no_of_class_attended_by_the_studen":class_att_date})
			if t.total_no_of_class_attended_by_the_studen==0:
				t.update({"attendance_percentage":0.0})
			else:
				t.update({"attendance_percentage":round((t.total_no_of_class_attended_by_the_studen/t.total_no_of_classes_scheduled)*100,2)})
			if attendance_criteria=="No":
				t.update({"elegibility_status": "Qualified"})
				t.update({"examination_qualification_approval":1})
			if attendance_criteria=="Yes":
				if t.attendance_percentage>=float(minimum_attendance_criteria):
					t.update({"elegibility_status": "Qualified"})
					t.update({"examination_qualification_approval":1})
				else:
					t.update({"elegibility_status": "Not-Qualified"})
					t.update({"examination_qualification_approval":0})		
				
		return student_list
	else:
		frappe.msgprint("No students found")
		return student_list



def get_program_enrollment(academic_term,programs=None,class_data=None):
	condition1 = " "
	condition2 = " "

	if programs:
		condition1 += " and pe.programs = %(programs)s"
	if class_data:
		condition1 +=" and pe.school_house = '%s' "%(class_data)
	condition1 +=" and s.enabled =1 "     
	return frappe.db.sql('''
		select
			pe.student, pe.student_name,pe.roll_no,pe.permanant_registration_number,s.enabled
		from
			`tabProgram Enrollment` pe {condition2}
		join `tabStudent` s ON s.name=pe.student
		where
			pe.academic_term = %(academic_term)s  {condition1}
		order by
			pe.student asc
		'''.format(condition1=condition1, condition2=condition2),
				({"academic_term": academic_term,"programs": programs}), as_dict=1) 

























