# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document

class ScholarshipApplication(Document):
	def validate(self):
		duplicacy_check(self)
		if len(self.document_list_tab) == 0:     
			add_document_list_rows(self)



	def on_submit(self):
		for t in self.document_list_tab:
			print(t)
			print(t.attach)
			if t.mandatory==1 and (t.attach==None or t.attach==""):
				frappe.throw("Document List not uploded. Kindly upload the Document")		

@frappe.whitelist()
def calculateAge(student_no):
	student_data=frappe.get_all("Student",{"name":student_no},["date_of_birth"])
	birthDate=student_data[0]['date_of_birth']
	age=''
	if birthDate:
		today = date.today()
		age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
	return age

@frappe.whitelist()
def current_education(student_no):
	current_education_data=frappe.get_all("Current Educational Details",{"parent":student_no},['programs','semesters','academic_year','academic_term'])
	return current_education_data


def add_document_list_rows(self): 
	if self.student_catagory and self.academic_year:
		self.set("document_list_tab",[])
	document_temp=frappe.get_all("Scholarships",{"name":self.scholarship_id},['name','document_required'])
	document_temp_data=frappe.get_all("Documents Template List",{"parent":document_temp[0]['document_required']},['document_name','mandatory','is_available'])
	for t in document_temp_data:
		self.append("document_list_tab",{
                "document_name":t['document_name'],
                "mandatory":t['mandatory'],
                "is_available" :t['is_available']
            })

def duplicacy_check(self):
	data=frappe.get_all("Scholarship Application",{"student_id":self.student_id,"scholarship_id":self.scholarship_id,"docstatus":1})
	if data:
		frappe.throw("Application has already filled up for this Scholarship Notification")  