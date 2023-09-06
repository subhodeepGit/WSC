# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from datetime import datetime, timedelta
from wsc.wsc.utils import get_courses_by_semester

class ParticipantGroup(Document):
	def validate(self):
		dupicate_student_group_chk(self)
		self.calculate_total_hours()
		for d in self.get("classes"):
			parent_doc = frappe.new_doc("ToT Class Schedule")
			parent_doc.participant_group_id = self.name
			parent_doc.academic_year = self.academic_year
			parent_doc.academic_term = self.academic_term
			parent_doc.course_name = self.program
			parent_doc.module_id = self.course
			parent_doc.module_name = self.module_name
			parent_doc.scheduled_date = d.scheduled_date
			# parent_doc.scheduled_time = d.scheduled_time
			parent_doc.room_number = d.room_number
			parent_doc.room_name = d.room_name
			parent_doc.from_time = d.from_time
			parent_doc.to_time = d.to_time
			parent_doc.duration = d.duration

			for td1 in self.get('participants'):
				parent_doc.append('participants', {
					'participant_id' : td1.participant,
					'participant_name' : td1.participant_name,
					# 'group_roll_number' : td1.group_roll_number,
					'active' : td1.active,	
				})
			for td2 in self.get('instructor'):
				parent_doc.append('trainers', {
					'trainer_id' : td2.instructors,
					'trainer_name' : td2.instructor_name	
				})
			parent_doc.save()	

		dulicate_trainer_chk(self)
		class_scheduling_date_validation(self)
		class_scheduling_ovelaping_chk(self)


	def calculate_total_hours(self):
		for d in self.get("classes"):
			if d.to_time and d.from_time:
				d.duration = datetime.strptime(d.to_time, '%H:%M:%S') - datetime.strptime(d.from_time, '%H:%M:%S') 

@frappe.whitelist()
def participant(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join("TP."+field + " like %(txt)s" for field in searchfields)
	participant_group_id=filters.get('participant_group_id')
	participant_details = frappe.db.sql(""" SELECT TP.name 
											FROM `tabParticipant Table` as PT
											JOIN `tabToT Participant` as TP on TP.name=PT.participant
											where (TP.{key} like %(txt)s or {scond}) and
													PT.parent = '{participant_group_id}'
											""".format(
												**{
												"key": searchfield,
												"scond": searchfields,
												"participant_group_id":participant_group_id
											}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return participant_details
				# t1 =datetime.strptime(d.from_time, "%H:%M:%S")
				# t2 = datetime.strptime(d.to_time, "%H:%M:%S")
				# delta = t2 - t1
				# ms = delta.total_seconds()/60
				# d.duration=round(ms,2)
				# if d.duration<=0:
				# 	idx=d.idx
				# 	frappe.throw(f"Time Duration can't be <b>Negative or Zero</b> for the line no <b><i>{idx}</i></b>")


def class_scheduling_ovelaping_chk(self):
	tot_start_date=self.tot_start_date
	tot_end_date=self.tot_end_date 
	error_list=[]
	for t in self.get('classes'):
		date_string = t.scheduled_date # Replace with your date string
		date_format = "%Y-%m-%d"
		parsed_date = datetime.strptime(date_string, date_format).date()
		if tot_start_date<=parsed_date <=tot_end_date:
			pass
		else:
			error_list.append(t.idx)
	if error_list:
		frappe.throw("<b>Class Schedule is beyond TOT period</b>")


def class_scheduling_date_validation(self):
	print("\n\n\n\n")

	








	student_with_class_sed=[]
	for t in self.get("participants"):
		for j in self.get("classes"):
			a={}
			if t.active==1:
				a['participant']=t.participant
				a['scheduled_date']=j.scheduled_date
				a['room_name']=j.room_name
				a['from_time']=j.from_time
				a['to_time']=j.to_time
				a['parent']=self.name
				student_with_class_sed.append(a)
				
	if student_with_class_sed:
		print(student_with_class_sed)

def dupicate_student_group_chk(self):
	data=frappe.get_all("Participant Group",{"participant_enrollment_id":self.participant_enrollment_id,
				     "course":self.course,"disabled":0,"docstatus":0},['name'])
	flag="No"
	for t in data:
		if t['name']==self.name:
			flag="Yes"
	if flag=="No":
		if data:
			frappe.throw("Participant Group Already Present")


def dulicate_trainer_chk(self):
	trainer_list=[]
	for t in self.get('instructor'):
		trainer_list.append(t.instructors)

	mylist =trainer_list
	myset = set(mylist)
	if len(mylist) != len(myset):
		frappe.throw("Duplicates Record found in the Trainer List")





@frappe.whitelist()
def get_enrollment_details(enrollment_id):
	enrollment_details = frappe.db.sql(""" SELECT  academic_year, academic_term, programs, semester FROM `tabToT Participant Enrollment` WHERE name = '%s'"""%(enrollment_id), as_dict=1)
	# modules = frappe.db.sql(""" SELECT course FROM `tabProgram Course` WHERE parent = '%s'"""%(enrollment_details[0]['programs']))
	return [enrollment_details[0]['academic_year'], enrollment_details[0]['academic_term'], enrollment_details[0]['programs'], enrollment_details[0]['semester']]

@frappe.whitelist()
def get_module_name(module_id):
	data = frappe.db.sql(""" SELECT course_name FROM `tabCourse` WHERE name = '%s'"""%(module_id), as_dict =1)
	return data[0]['course_name']

@frappe.whitelist()
def get_participants(enrollment_id):
	data = frappe.get_all("Reported Participant", filters = [['parent', '=', enrollment_id], ['is_reported', '=', 1]], fields =['participant', 'participant_name'])
	return data