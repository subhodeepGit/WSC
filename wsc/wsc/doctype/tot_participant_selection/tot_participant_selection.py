# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import utils

class ToTParticipantSelection(Document):
	def validate(self):
		academic_year_data=frappe.get_all("Academic Term",{"name":self.academic_term},['academic_year'])
		if academic_year_data:
			if academic_year_data[0]['academic_year']!=self.academic_year:
				frappe.throw("Academic Year Doesn't Match With Academic Term")
		else:
			frappe.throw("Academic Year has not started")

	def on_submit(self):
		if not self.get('participants'):
			frappe.throw("Participant List Can't be Empty")
		check_program_enrolement(self)	
		update_participent(self)	
	def before_submit(self):
		self.create_tot_batch()
	def create_tot_batch(self):
		tot_batch = frappe.get_doc(
			{
				"doctype": "Student Batch Name",
				"batch_name": self.tot_participant_batch,
			}
		)
			# for duplicate_batch_check in frappe.get_all("Student Batch Name",{'name':self.tot_participant_batch},['name']):
			# 	if duplicate_batch_check.name==self.tot_participant_batch:
			# 		pass
			# 	else:
		tot_batch.save()

def check_program_enrolement(self):
	participants_list=[]
	for t in self.get('participants'):
		participants_list.append(t.participant_id)

	error_data_list=[]
	if participants_list:
		for t in participants_list:
			participant_data=frappe.get_all("ToT Participant",[['name','=',t]],['name','student_no'])
			if participant_data:
				participant_data=participant_data[0]
				if participant_data['student_no']!=None:
					enrollment_data=frappe.get_all("Program Enrollment",{"student":participant_data['student_no'],
															'program_grade':self.course_type ,
															'programs':self.course,
															'program':self.semester,
															'academic_year':self.academic_year,
															'academic_term':self.academic_term,
															'docstatus':1
															},
															['name'])
					if enrollment_data:
						error_data_list.append({"participant":participant_data['name'],
												'Courese Enrollment':enrollment_data[0]['name'],
												'student':participant_data['student_no']})
	if 	error_data_list:
		frappe.throw("Following Participant already enroll for Course for this Academic Year and Academic Term %s"%(error_data_list))	
					
				


def update_participent(self):
	program_start_date=self.start_date
	program_end_date=self.end_date
	participant_selection=self.name
	academic_year=self.academic_year
	academic_term=self.academic_term
	semester=self.semester
	course=self.course
	for t in self.get('participants'):
		participants=t.participant_id
		doc=frappe.get_doc('ToT Participant',participants)
		doc.append("previous_participations",{
			"programs":course,
			"academic_year":academic_year,
			"participant_selection":participant_selection,
			"program_start_date":program_start_date,
			"program_end_date":program_end_date,
			"semester":semester,
			"academic_term":academic_term
		})
		doc.save()		
@frappe.whitelist()
def get_semester(course):
	for sem in frappe.get_all("Program",{'programs':course},['name']):
		semester=sem.name
	return semester
@frappe.whitelist()
def get_academic_term(academic_year):
	today_date=utils.today()
	data=frappe.db.sql(""" select name 
	       						from `tabAcademic Term` 
	       						where academic_year='%s' 
	       						and  (term_start_date<='%s' and  term_end_date>='%s' )"""%(academic_year,today_date,today_date),as_dict=True)
	# for acd_yr in frappe.get_all("Academic Term",{'academic_year':academic_year},['name']):
	# 	academic_term=acd_yr.name
	if data:
		for acd_yr in data:
			academic_term=acd_yr['name']	
		return academic_term
	else:
		frappe.throw("Academic Year has not started")