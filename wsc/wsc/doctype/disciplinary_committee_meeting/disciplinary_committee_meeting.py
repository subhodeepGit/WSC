# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DisciplinaryCommitteeMeeting(Document):
	# @frappe.whitelist()
	def validate(doc):
		Dc_id=doc.indisciplinary_action
		info_dc=frappe.db.sql("""SELECT * FROM `tabDisciplinary Committee Meeting` WHERE `indisciplinary_action`="%s" 
								and (`idx`!="1" and `idx`!=2) """%(Dc_id))						
		if len(info_dc)==0:
			pass
		elif len(info_dc)!=0 and info_dc[0][5]==0:
			pass
		else:
			frappe.throw("DC is already closed")
	pass



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def status_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT IA.`name` FROM `tabIndisciplinary Actions` as IA 
			JOIN `tabIndisciplinary Complaint Registration` ICR on ICR.name=IA.indisciplinary_complaint_registration_id
			WHERE `type_of_decision`="Disciplinary Committee" and ICR.status="Open" """)