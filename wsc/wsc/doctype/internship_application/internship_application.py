# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import datetime

class InternshipApplication(Document):
	def validate(self):
		if self.is_new():
			if frappe.get_all("Internship Application", {"participant_type":self.participant_type,
											 		"participant_id":self.participant_id,
													"select_internship":self.select_internship,
													"docstatus":1}):
				frappe.throw("</b>Participant Has Already Applied For Internship Drive</b>")



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_select_internship(doctype, txt, searchfield, start, page_len, filters):
	data=[]
	today_date=filters.get("today_date")
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)
	data=frappe.db.sql("""select name,title_of_drive 
								from `tabInternship Drive` 
								where ({key} like %(txt)s or {scond}) 
								and (application_start_date<='{data}' and application_end_date>='{data}')
								and enable=1
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"data":today_date
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return data

@frappe.whitelist()
def get_internship_name(internship_id):
	internship_name = frappe.db.sql(""" SELECT title_of_drive FROM `tabInternship Drive` WHERE name = '%s'"""%(internship_id))
	return internship_name[0][0]

@frappe.whitelist()
def get_participant_name(participant_type = None, participant_id = None):
	if(len(participant_id) > 0):
		if(participant_type == 'Student'):
			student_name = frappe.db.sql(""" SELECT student_name FROM `tabStudent` WHERE name ='%s'"""%(participant_id))
			return student_name[0][0]
		elif(participant_type == 'Employee'):
			employee_name = frappe.db.sql(""" SELECT employee_name FROM `tabEmployee` WHERE name ='%s'"""%(participant_id))
			return employee_name[0][0]
		

# get filtered drives
@frappe.whitelist()
def drive_filter(doctype, txt, searchfield, start, page_len, filters):
	formatted_date = datetime.date.today().strftime("%d-%m-%Y") #formatted date "dd-mm-yyyy"
	participant_id=filters.get('participant_id')
	enrollment_details = frappe.db.sql(""" SELECT programs, program FROM `tabProgram Enrollment` WHERE student='%s'"""%(participant_id))
	course = enrollment_details[0][0]
	semester = enrollment_details[0][1]
	drive_course_details = frappe.db.sql(""" SELECT parent FROM `tabInternship for Programs` where programs = '{course}' and semester = '{semester}'
				    """.format(
						**{
						"course":course,
						"semester" : semester
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return drive_course_details