# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document

class ScholarshipApplication(Document):
	def validate(self):
		if len(self.document_list_tab) == 0:     
			add_document_list_rows(self)


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
	# get_document_list_by_category(self)
        # for d in get_document_list_by_category(doc):
        #     doc.append("document_list",{
        #         "document_name":d.document_name,
        #         "mandatory":d.mandatory,
        #         "is_available" :d.is_available
        #     })

def get_document_list_by_category(self):
    filters={"student_category":self.student_category}
    group_by=""
    # if doc.counselling_structure:
    #     filters.update({"parent":doc.counselling_structure,"parenttype":"Counselling Structure"})
    # else:
    #     filters.update({"parent":["IN",[d.student_admission for d in doc.get('program_priority')]],"parenttype":"Student Admission"})
    #     group_by="document_name"
    # doc_list  = frappe.db.sql("""SELECT DL.document_name, DL.mandatory, DL.is_available from `tabDocuments Template List` as DL 
    # inner join `tabDocuments Template` as D on DL.parent= D.name where D.student_category='{0}' and D.academic_year = '{1}' ORDER BY document_name ASC""".format(doc.student_category,doc.academic_year) ,as_dict=1)
    # return doc_list if doc_list else []	    