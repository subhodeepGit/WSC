# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document

class ScholarshipApplication(Document):
	def validate(self):
		duplicacy_check(self)
		validate_elgibility(self)
		validate_ifsc_code(self)
		if self.student_category!=self.student_catagory:
			frappe.throw("Student don’t belong to the student category given by the company")
		if len(self.document_list_tab) == 0:     
			add_document_list_rows(self)

	def on_submit(self):
		for t in self.document_list_tab:
			if t.mandatory==1 and (t.attach==None or t.attach==""):
				frappe.throw("Document List not uploded. Kindly upload the Document")		
def validate_ifsc_code(self):
	if self.bank_ifsc:
		if not contains_only_characters(self.bank_ifsc):
			frappe.throw("Invalid IFSC Code")
	if self.ac_number:
		if not contains_only_characters(self.ac_number):
			frappe.throw("Invalid IFSC Code")
def contains_only_characters(bank_ifsc):
    return all(char.isalpha() or char.isspace() or char.isdigit() for char in bank_ifsc)
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

@frappe.whitelist()
def eligibility(scholarship_id_data):
	data=frappe.get_all("Scholarship Eligibility Paramete",{"parent":scholarship_id_data},['name','parameter','percentagecgpa','eligible_score'])
	return data

@frappe.whitelist()
def valid_scholarship(doctype, txt, searchfield, start, page_len, filters):
	from frappe import utils
	today = utils.today()
	fil_data=frappe.db.sql(""" Select name from tabScholarships where start_date<'%s' and end_date>'%s' and docstatus=%s """%(today,today,filters.get('docstatus')))
	return fil_data

def validate_elgibility(self):
	scholarship_elgibility=frappe.get_all("Scholarship Eligibility Paramete",
				       {"parent":self.scholarship_id},['name','parameter','percentagecgpa','eligible_score'],order_by="idx")
	not_matching_parameter=[]
	for t in self.get('scholarship_eligibility_parameter'):
		for j in scholarship_elgibility:
			if t.parameter==j['parameter']:
				if float(j['eligible_score'])>float(t.eligible_score):
					not_matching_parameter.append(t.parameter)

	if not_matching_parameter:
		frappe.throw("Eligibility parameters for scholarship don't match as per the eligibility criteria given by the company")

	semester_1_marks=self.semester_1_marks
	semester_2_marks=self.semester_2_marks
	sem_data=frappe.get_all("Scholarships",{"name":self.scholarship_id},['semester_1_marks','semester_2_marks'])
	if sem_data[0]['semester_1_marks']>semester_1_marks:
		frappe.throw("Semester Eligibility parameters for scholarship don't match as per the eligibility criteria given by the company")
	if sem_data[0]['semester_2_marks']>semester_2_marks:
		frappe.throw("Semester Eligibility parameters for scholarship don't match as per the eligibility criteria given by the company")	
