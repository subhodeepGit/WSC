# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StudentsGrievance(Document):
	def validate(self):
		validate_date(self)
		# mobile_number_validation(self)

	def on_cancel(self):
		data=frappe.get_all("Grievance Cell",{"students_grievance":self.name})
		if data:
			frappe.throw("Your Complaint Has Already Been Registered")       
        

def validate_date(self):
	if self.date_of_incident and  self.posting_date and self.date_of_incident > self.posting_date:
		frappe.throw("Date of Incident <b>'{0}'</b> Must Be a valid Date <b>'{1}'</b>".format(self.date_of_incident, self.posting_date))
def mobile_number_validation(self):

    if self.emergency_phone_no:
        if not (self.emergency_phone_no).isdigit():
            frappe.throw("Field <b>Emergency Phone Number</b> Accept Digits Only")
        if len(self.emergency_phone_no)>10:
            frappe.throw("Field <b>Emergency Phone Number</b> must be 10 Digits")
        if len(self.emergency_phone_no)<10:
            frappe.throw("Field <b>Emergency Phone Number</b> must be 10 Digits")

@frappe.whitelist()
def get_register_complaint(source_name):
	all_details = frappe.get_all("Students Grievance",{"name":source_name},["name","raised_by","email_id","student_name","gender","emergency_phone_no",
																		 "contact_phone_no","posting_date","date_of_incident","type_of_grievance","status",
																		 "description_of_grievance","areas_of_grivence",'roll_no'])
	grievance_cell=frappe.new_doc("Grievance Cell")
	grievance_cell.student=all_details[0].raised_by
	grievance_cell.roll_no=all_details[0].roll_no
	grievance_cell.student_name= all_details[0].student_name
	grievance_cell.emergency_phone_no=all_details[0].emergency_phone_no
	grievance_cell.gender=all_details[0].gender
	grievance_cell.email_id=all_details[0].all_details
	grievance_cell.contact_phone_no=all_details[0].contact_phone_no
	grievance_cell.posting_date=all_details[0].posting_date
	grievance_cell.date_of_incident=all_details[0].date_of_incident
	grievance_cell.type_of_grievance=all_details[0].type_of_grievance
	grievance_cell.description_of_grievance=all_details[0].description_of_grievance
	grievance_cell.areas_of_grivence=all_details[0].areas_of_grivence
	grievance_cell.status=all_details[0].status
	grievance_cell.students_grievance = all_details[0].name

	return grievance_cell