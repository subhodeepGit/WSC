# Copyright (c) 2022, SOUL LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AssignmentUpload(Document):
	def before_save(doc):
		output=frappe.db.sql("""SELECT * from `tabAssignment Upload` 
		WHERE `assignment_question`="%s" and `student`="%s" and `docstatus`!=1"""%(doc.assignment_question,doc.student))
		if len(output)==0:
			output=frappe.db.sql(""" SELECT `receivable_by_students` from `tabUpload Material` WHERE `name`="%s" """%(doc.assignment_question))
			if output[0][0]==1:
				pass
			else:
				frappe.throw("Not a uploadable assignment material")	
		else:
			frappe.throw("Document Already Uploaded")	
	def on_submit(doc):
		output=frappe.db.sql("""SELECT * from `tabAssignment Upload` 
		WHERE `assignment_question`="%s" and `student`="%s" and `docstatus`!=1"""%(doc.assignment_question,doc.student))
		if len(output)==0:
			output=frappe.db.sql(""" SELECT `receivable_by_students` from `tabUpload Material` WHERE `name`="%s" """%(doc.assignment_question))
			if output[0][0]==1:
				pass
			else:
				frappe.throw("Not a uploadable assignment material")	
		else:
			frappe.throw("Document Already Uploaded")	

@frappe.whitelist()
def download_file(doc_id):
	output=frappe.db.sql(""" SELECT `attach_answers` FROM `tabAssignment Upload` WHERE `name`="%s" """%(doc_id))
	r=output[0][0]
	return r

@frappe.whitelist()
def Question(doc_id):
	output=frappe.db.sql(""" SELECT `attachment` FROM `tabAssignment Upload` WHERE `name`="%s" """%(doc_id))
	r=output[0][0]
	return r