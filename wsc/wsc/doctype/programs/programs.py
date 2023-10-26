# -*- coding: utf-8 -*-
# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe,json
from frappe.model.document import Document
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from frappe.desk.form.linked_with import get_submitted_linked_docs

class Programs(Document):
	def validate(self):
		self.validate_abbrevation()
		self.validate_no_semesters()
		self.create_permissions()
		# self.director_permission()

##################################### - FOR INSTRUCTOR - #################################
	def create_permissions(doc):
		d=doc.get("department")
		for instuctor_log in frappe.get_all("Instructor Log",{"department":d,"programs":doc.name},['department','programs','parent']):
			for instr in frappe.get_all("Instructor",{"name":instuctor_log.parent},['department','name','employee']):
				for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id','department']):
					if emp.user_id:
						add_user_permission(doc.doctype,doc.name,emp.user_id,doc)	
##################################### - FOR DIRECTOR - #################################
	def director_permission(doc):
		d = doc.get("department")
		for dean in frappe.get_all("Dean",{"department":d},['department','employee_id']):
			for emp in frappe.get_all("Employee",{"name":dean.employee_id},['user_id','department']):
					if emp.user_id:
						add_user_permission(doc.doctype,doc.name,emp.user_id,doc)
				
	
	
	def on_change(self):
		for sem in frappe.get_all("Program",{"programs":self.name},['name'],order_by="semester_order desc"):
			if sem.name not in [d.semesters for d in self.get("semesters")]:
				frappe.delete_doc("Program",sem.name)

	def validate_no_semesters(self):
		if self.no_of_semesters==0:
			frappe.throw("<b>No of Semesters</b> Value cannot be zero")
				
	def validate_abbrevation(self):
		for programs in frappe.get_all("Programs",{"programs_abbreviation":self.programs_abbreviation,"name":("!=",self.name)}):
			frappe.throw("Programs Abbreviation already exists in Programs <b>{0}</b>".format(programs.name))
	@frappe.whitelist()
	def create_tot_course(self):
		is_existing=True
		for c in range(int(self.tot_programme)):
			is_short_term_course=frappe.get_all("Program Grades",{"name":self.program_grade},['is_short_term_course'])
			program_name=(self.programs_abbreviation)
			print(program_name)
			if not frappe.db.exists("Program",program_name):
				is_existing=False
				doc=frappe.new_doc("Program")
				doc.program_name=program_name
				doc.programs=self.name
				doc.is__tot=self.is_tot
				doc.is_short_term_course=is_short_term_course[0]['is_short_term_course']
				doc.semester_order=c+1
				doc.save()
			else:
				doc=frappe.get_doc("Program",program_name)
				doc.is__tot=self.is_tot
				doc.save()	

		return {"semesters":[d.name for d in frappe.get_all("Program",{"programs":self.name},order_by="creation",limit=int(self.tot_programme))],"is_existing":is_existing}
	@frappe.whitelist()
	def create_semesters(self):
		semesters=[]
		is_existing=True
		for c in range(int(self.no_of_semesters)):
			program_name=(self.programs_abbreviation+" Semester "+int_to_Roman(c+1))
			if not frappe.db.exists("Program",program_name):
				is_existing=False
				doc=frappe.new_doc("Program")
				doc.program_name=program_name
				doc.programs=self.name
				doc.semester_order=c+1
				doc.save()

		return {"semesters":[d.name for d in frappe.get_all("Program",{"programs":self.name},order_by="creation",limit=int(self.no_of_semesters))],"is_existing":is_existing}

def int_to_Roman(num):
	val = [
		100, 90, 50, 40,
		10, 9, 5, 4,
		1
		]
	syb = [
		"C", "XC", "L", "XL",
		"X", "IX", "V", "IV",
		"I"
		]
	roman_num = ''
	i = 0
	while  num > 0:
		for _ in range(num // val[i]):
			roman_num += syb[i]
			num -= val[i]
		i += 1
	return roman_num

@frappe.whitelist()
def create_courses(program,semester,courses):
	courses=json.loads(courses)
	for row in courses:
		doc=frappe.new_doc("Course")
		doc.course_name = row.get('course')
		# doc.course_name=frappe.db.get_value("Course",{'name':row.get('course')},"course_name")
		doc.mode=row.get('mode')
		doc.programs=program
		doc.program=semester
		doc.save()
		sem=frappe.get_doc("Program",semester)
		sem.append("courses",{
			"course":doc.name,
			"modes":doc.mode
		})
		sem.save()

	
