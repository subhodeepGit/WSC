# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.utils import semester_belongs_to_programs,duplicate_row_validation

class PlacementBlockedStudent(Document):
	def validate(self):
		self.validate_student()
		# self.validate_placement_drive()
		semester_belongs_to_programs(self)
		duplicate_row_validation(self,'block_drive_list',['placement_drive'])
		duplicate_row_validation(self,'blocked_student',['student'])
	
	def validate_student(self):
		for stu in self.get("blocked_student"):
			if not frappe.db.count("Program Enrollment",{"docstatus":1,"student":stu.get("student"),"program":self.get("semester"),"academic_year":self.get("academic_year")},['student','student_name']):
				frappe.throw("Student <b>'{0}'</b> Not Enrolled in this <b>Academic Year</b> and <b>Semester</b>".format(stu.student))

	def validate_placement_drive(self):
		for drive in self.get("block_drive_list"):
			if not frappe.db.count("Placement Department",{"parenttype":"Placement Drive","department":frappe.db.get_value("Programs",self.get("programs"),'department'),'parent':drive.placement_drive}):
				frappe.throw("Placement Drive <b>'{0}'</b> Not belongs to Programs's Department".format(drive.placement_drive))

@frappe.whitelist()
def get_placement_drive(doctype, txt, searchfield, start, page_len, filters):
	return frappe.get_all("Placement Department",{"parenttype":"Placement Drive","department":frappe.db.get_value("Programs",filters.get("programs"),'department'),"docstatus":1,"parent":['like', '%{}%'.format(txt)]},['parent'],group_by="parent",as_list=1)

@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
	return frappe.get_all("Program Enrollment",{"docstatus":1,"program":filters.get("semester"),"academic_year":filters.get("academic_year"),"student":['like', '%{}%'.format(txt)]},['student','student_name'],group_by="student",as_list=1)


@frappe.whitelist()
def instructor(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

	placement_drive_id = filters.get('placement_drive_id')
	student_details = frappe.db.sql(""" SELECT student_doctype_name FROM `tabEligible Student` where ({key} like %(txt)s or {scond}) and
				    parent = '{placement_drive_id}'
				    """.format(
						**{
						"key": searchfield,
						"scond": searchfields,
						"placement_drive_id":placement_drive_id
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return student_details