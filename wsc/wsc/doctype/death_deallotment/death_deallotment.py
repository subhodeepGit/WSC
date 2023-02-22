# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DeathDeallotment(Document):
	# @frappe.whitelist()	
	def on_submit(doc):
		end_date=doc.date_of_demise
		type_of_clearance="Death"
		allotment_number=doc.student
		room_id=doc.room_id	
		frappe.db.sql(""" UPDATE `tabRoom Allotment` SET `end_date`="%s",`allotment_type`="%s" WHERE `name`="%s" """%\
					(end_date,type_of_clearance,allotment_number))
				
		frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(room_id))
		status=frappe.get_all("Room Allotment",{"name":doc.student},['hostel_registration_no'])
		frappe.db.set_value("Student Hostel Admission",status[0]['hostel_registration_no'], "allotment_status", "Death-Deallotted") 			


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		SELECT `name`,`student`,`student_name`,`hostel_id` FROM `tabRoom Allotment` WHERE (`start_date` <= now() AND `end_date` >= now()) 
	"""
	)	
	