# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BuildingRoom(Document):
	def validate(self):
		duplicate(self)
		dateValidate(self)

# To filter out buildings which are currently between start and end date
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def room_type_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT `name` from `tabBuildings` WHERE `start_date`<=now() and `end_date`>=now()""")

# To check for any duplicate record within a building regarding room no. or room type
def duplicate(self):
	data=frappe.get_all("Building Room",{"room_no":self.room_no,"building_name":self.building_name,"type_of_room":self.type_of_room})
	if data:
		frappe.throw("Same room no. can't exist within the building")

# To validate if the start date is not after the end date in allotable room type
def dateValidate(self):
	if self.allotment_status == "Allottable":
		if self.start_date > self.end_date:
			frappe.throw("Start date cannot be greater than End date")
	else:
		pass
