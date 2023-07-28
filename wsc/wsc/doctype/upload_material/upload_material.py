# Copyright (c) 2022, SOUL LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UploadMaterial(Document):
	def on_submit(doc):
		if doc.start_date<=doc.end_date:
			pass
		else:
			frappe.throw("End Date should be greater then End Date")








@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def Teacher_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT `employee`,`name` FROM `tabInstructor` WHERE `status`="Active" """)


emp_id=""
teacher_name1=""
student_group=""


@frappe.whitelist()
def emp_id_call(emp_code=None,teacher_name=None):
	global emp_id,teacher_name1
	emp_id=emp_code
	teacher_name1=teacher_name


@frappe.whitelist()
def student_group_call(Group=None):
	global student_group
	student_group=Group

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def Student_group_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT Instructor_Log.student_group,Instructor.name,Instructor_Log.program,Instructor_Log.course
								from `tabInstructor` As Instructor
								JOIN `tabInstructor Log` AS Instructor_Log ON Instructor_Log.Parent=Instructor.name
								JOIN `tabStudent Group` AS Student_Group ON Student_Group.name=Instructor_Log.student_group
								WHERE Instructor.employee="%s"  and Instructor_Log.student_group!="Null" and Student_Group.disabled!=1 """%(emp_id))

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def Course_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT `course`,`course_code` 
								from `tabStudent Group Instructor`
								WHERE `parent`="%s" and `instructor`="%s" """%(student_group,teacher_name1))

@frappe.whitelist(allow_guest=True)
def Submission_of_task(**args):
	output=frappe.db.sql(""" SELECT `name` from `tabStudent` WHERE `student_email_id`="%s" """%(args["student"]))
	if len(output)!=0:
		Doc_id=args["name"]
		Student_id=output[0][0]
		return {"Doc_id":Doc_id,"Student_id":Student_id}
	else:
		frappe.throw("Only Student is assigned for uploding task")	

@frappe.whitelist()
def download_file(doc_id):
	output=frappe.db.sql(""" SELECT `attachemnet_of_file_video` from `tabUpload Material` WHERE `name`="%s" """%(doc_id))
	r=output[0][0]
	return r							