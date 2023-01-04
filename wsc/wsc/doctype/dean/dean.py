# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions

class Dean(Document):
	# pass

	def validate(self):
		pass
		# self.dean_permission()
		# self.individual_dean()
		# self.program_permission()
	
	def dean_permission(doc):
		d=doc.get("department")
		for instuctor_dean in frappe.get_all("Instructor",{"department":d},['name','department']):
			instu_direct=frappe.get_doc("Instructor",instuctor_dean.name)
			instu_direct.save()
		for get_programs in frappe.db.get_all("Programs",{"department":d},['name','department']):
			print("\n\n\nget_programs")
			print(get_programs)
			programss=frappe.get_doc("Programs",get_programs.name)
			programss.save()
	def individual_dean(doc):
		d=doc.get("user_id")
		for direct in frappe.get_all("Dean",{"name":d},['department','name','employee_id']):
			for emp in frappe.get_all("Employee",{"name":direct.employee_id},['user_id']):
				if emp.user_id:
					add_user_permission(doc.doctype,doc.name,emp.user_id,doc)
@frappe.whitelist()
def get_enroll_instructors(department=None):
	if not department:
		frappe.throw("Select Your Department")
	# filter={}
	# if department:
	# 	filter.update({"department":department})
	instructor_table=[]
	for instructor in frappe.get_all("Instructor",{"department":department},['department','gender','name'],group_by="name"):
		instructor_table.append(instructor)
	if len(instructor_table)==0:
		frappe.msgprint("No Records Found")
	return instructor_table
	####################################################################################################
	# def program_permission(doc):
	# 	d = doc.get("department")
	# 	for instru_department in frappe.get_all("Department",{"name":d},['name']):
	# 		for instru_programs in frappe.get_all("Programs",{"department":instru_department.name},['name','department']):
	# 			for instr in frappe.get_all("Instructor",{"department":instru_programs.department},['department','instructor_name','name','employee']):
	# 				for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id','department']):
	# 					print("\n\nemployee_programs")
	# 					print(emp)
	# 					if emp.user_id:
	# 						add_user_permission(doc.doctype,doc.name,emp.user_id,doc)
	# 						# for get_programs in frappe.db.get_all("Programs",{"department":emp.department},['name','department']):
	# 						programss=frappe.get_doc("Programs",instru_programs.name)
	# 						programss.save()
	########################################################################################################

