# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt
from dataclasses import fields
from unicodedata import name
from frappe import _
from frappe.utils.csvutils import getlink
import frappe
from frappe.model.document import Document

class DownloadStudentPassportPhoto(Document):
	pass
@frappe.whitelist()
def filter_programs_by_department(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Programs",{"name":['like', '%{}%'.format(txt)],"department":["IN",[d.name for d in frappe.get_all("Department",{"parent_department":filters.get("department")})]],"program_grade":["IN",[d.name for d in frappe.get_all("Program Grades",{"grade":filters.get("program_grade")})]]},order_by="name asc",as_list=1)
@frappe.whitelist()
def generate_passport_photo(programs,have_you_approved_the_selected_program,application_status,academic_year=None,department=None,program_grade=None):
	last_result=[]
	if(have_you_approved_the_selected_program=="1"):
		for priority_program in frappe.get_all("Program Priority",{'idx':1,"programs":programs,"approve":1},['programs','idx','parent']):
			student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title","passport_photo"])
			last_result.extend(student_list)
		if len(last_result)==0:
			frappe.throw(_("Not a single Student {0} for {1} as their First Priority").format(getlink("Student Applicant",application_status),(programs)))
		else:
			return last_result
	else:
		for priority_program in frappe.db.get_all("Program Priority",{'idx':1,"programs":programs},['programs','idx','parent']):
			student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title","passport_photo"])
			last_result.extend(student_list)
		if len(last_result)==0:
			frappe.throw(_("Not a single Student {0} for {1} as their First Priority").format(getlink("Student Applicant",application_status),(programs)))
		else:
			return last_result
@frappe.whitelist()
def generate_passport_photo2(programs,have_you_approved_the_selected_program,application_status,academic_year=None,department=None,program_grade=None):
	last_result=[]
	if(have_you_approved_the_selected_program=="1"):
		for priority_program in frappe.db.get_all("Program Priority",{'idx':2,"programs":programs,"approve":1},['programs','idx','parent']):
			student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title","passport_photo"])
			last_result.extend(student_list)
		if len(last_result)==0:
				frappe.throw(_("Not a single Student {0} for {1} as their Second Priority").format(getlink("Student Applicant",application_status),(programs)))
		else:
			return last_result
	else:
		for priority_program in frappe.db.get_all("Program Priority",{'idx':2,"programs":programs},['programs','idx','parent']):
			student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title","passport_photo"])
			last_result.extend(student_list)
		if len(last_result)==0:
				frappe.throw(_("Not a single Student {0} for {1} as their Second Priority").format(getlink("Student Applicant",application_status),(programs)))
		else:
			return last_result
@frappe.whitelist()
def generate_passport_photo3(programs,have_you_approved_the_selected_program,application_status,academic_year=None,department=None,program_grade=None):
	last_result=[]
	if(have_you_approved_the_selected_program=="1"):
		for priority_program in frappe.db.get_all("Program Priority",{'idx':3,"programs":programs,"approve":1},['programs','idx','parent']):
			student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title","passport_photo"])
			last_result.extend(student_list)
		if len(last_result)==0:
			frappe.throw(_("Not a single Student {0} for {1} as their Third Priority").format(getlink("Student Applicant",application_status),(programs)))

		else:
			return last_result
	else:
		for priority_program in frappe.db.get_all("Program Priority",{'idx':3,"programs":programs},['programs','idx','parent']):
			student_list = frappe.db.get_all("Student Applicant",{"name":priority_program.parent,"academic_year":academic_year,"department":department,"program_grade":program_grade,"docstatus":1,"application_status":application_status},["name","title","passport_photo"])
			last_result.extend(student_list)
		if len(last_result)==0:
			frappe.throw(_("Not a single Student {0} for {1} as their Third Priority").format(getlink("Student Applicant",application_status),(programs)))

		else:
			return last_result
@frappe.whitelist()
def student_passport_photo(student_applicant):
	ind_student_photo=frappe.get_all("Student Applicant",filters=[["name","=","%s"%(student_applicant)],["docstatus","=",1]],fields=["name","title","passport_photo"])
	return ind_student_photo