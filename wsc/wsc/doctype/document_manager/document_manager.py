# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

from dataclasses import fields
from xmlrpc.client import SERVER_ERROR
import frappe
from frappe import _
from frappe.utils.csvutils import getlink
from frappe.model import document
from frappe.model.document import Document

class DocumentManager(Document):
	pass
@frappe.whitelist()
def filter_programs_by_department(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Programs",{"name":['like', '%{}%'.format(txt)],"department":["IN",[d.name for d in frappe.get_all("Department",{"parent_department":filters.get("department")})]],"program_grade":["IN",[d.name for d in frappe.get_all("Program Grades",{"grade":filters.get("program_grade")})]]},order_by="name asc",as_list=1)
@frappe.whitelist()
def get_documents1(programs,application_status,document_name=None,academic_year=None,department=None,program_grade=None):
	last_result=[]
	for priority_program in frappe.db.get_all("Program Priority",{'idx':1,"programs":programs},['programs','idx','parent']):
		student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title"])
		last_result.extend(student_list)
	student_detail=[]
	for t in last_result:
		student_detail.append(t["name"])
		documents=frappe.db.get_all("Document List",filters=[["parenttype","=","Student Applicant"],["parent","in",(student_detail)],["document_name","=","%s"%(document_name)]],fields=["parent","attach"])
		# str(tuple)
		# ["parent","in",str(tuple(student_detail))],
	if len(last_result)==0:
		frappe.throw(_("Not a single Student {0} for {1} as their First Priority").format(getlink("Student Applicant",application_status),(programs)))
	else:
		return documents
@frappe.whitelist()
def get_documents2(programs,application_status,document_name=None,academic_year=None,department=None,program_grade=None):
	last_result=[]
	for priority_program in frappe.db.get_all("Program Priority",{'idx':2,"programs":programs},['programs','idx','parent']):
		student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title"])
		last_result.extend(student_list)
	student_detail=[]
	for t in last_result:
		student_detail.append(t["name"])
		documents=frappe.db.get_all("Document List",filters=[["parenttype","=","Student Applicant"],["parent","in",(student_detail)],["document_name","=","%s"%(document_name)]],fields=["parent","attach"])
	if len(last_result)==0:
		frappe.throw(_("Not a single Student {0} for {1} as their Second Priority").format(getlink("Student Applicant",application_status),(programs)))
	else:
		return documents
@frappe.whitelist()
def get_documents3(programs,application_status,document_name=None,academic_year=None,department=None,program_grade=None):
	last_result=[]
	for priority_program in frappe.db.get_all("Program Priority",{'idx':3,"programs":programs},['programs','idx','parent']):
		student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title"])
		last_result.extend(student_list)
	student_detail=[]
	for t in last_result:
		student_detail.append(t["name"])
		documents=frappe.db.get_all("Document List",filters=[["parenttype","=","Student Applicant"],["parent","in",(student_detail)],["document_name","=","%s"%(document_name)]],fields=["parent","attach"])
		# str(tuple)
		# ["parent","in",str(tuple(student_detail))],
	# return documents
	if len(last_result)==0:
			frappe.throw(_("Not a single Student {0} for {1} as their Third Priority").format(getlink("Student Applicant",application_status),(programs)))
	else:
		return documents

	
@frappe.whitelist()
def generate_passport_photo(programs,academic_year=None,department=None,program_grade=None):
	last_result=[]
	for priority_program in frappe.db.get_all("Program Priority",{'idx':1,"programs":programs},['programs','idx','parent']):
		student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1},["name","title","passport_photo"])
		last_result.extend(student_list)
	return last_result