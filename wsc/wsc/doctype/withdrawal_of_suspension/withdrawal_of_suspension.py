# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WithdrawalofSuspension(Document):
	# @frappe.whitelist()
	def validate(doc):
		ID_ac_id=doc.indisciplinary_action_id
		info=frappe.db.sql("""SELECT * FROM `tabWithdrawal of Suspension` WHERE `indisciplinary_action_id`="%s" 
								and (`idx`!="1" and `idx`!=2)"""%(ID_ac_id))
		if len(info)==0:
			pass
		elif len(info)!=0 and info[0][5]==0:
			info=frappe.db.sql("""SELECT `allotment_number` FROM `tabIndisciplinary Complaint Registration Student` WHERE `parent`="%s" """%(ID_ac_id))
			for t in range(len(info)):
				frappe.db.sql("""UPDATE `tabRoom Allotment` SET `allotment_type`="Allotted" WHERE `name`="%s" """%(info[t][0]))
			pass
		else:
			frappe.throw("Already suspension is withdrawal")


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def type_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		SELECT IA.name, IA.indisciplinary_complaint_registration_id, IA.type_of_decision FROM `tabIndisciplinary Actions` as IA 
		JOIN `tabIndisciplinary Complaint Registration` as ICR On IA.indisciplinary_complaint_registration_id = ICR.name 
		WHERE IA.type_of_decision = "Suspension Letter" and ICR.status="Open" 
	"""
	)	
