# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Resume(Document):
	pass

@frappe.whitelist()
def get_location(student_id):
	get_location_details = frappe.db.sql("""SELECT block, district, stat, pin_code FROM `tabStudent` WHERE name = '%s'"""%(student_id))
	if(len(get_location_details) > 0 and None not in get_location_details[0]):
		return(get_location_details[0][0]+','+ get_location_details[0][1] + ','+get_location_details[0][2]+'-'+get_location_details[0][3])
		