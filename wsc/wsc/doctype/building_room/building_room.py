# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BuildingRoom(Document):
	def validate(self):
		duplicate(self)
		dateValidate(self)
		new_doc(self)

# To filter buildings which are currently between start and end date
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def room_type_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT `name` from `tabBuildings` WHERE `start_date`<=now() and `end_date`>=now()""")

# To check for any duplicate record within a building regarding room no. or room type
def duplicate(self):
	data=frappe.get_all("Building Room",{"room_no":self.room_no,"building_name":self.building_name,"type_of_room":self.type_of_room})
	if not data:
		return
	if data:
		name=data[0]['name']                                
		if name==self.name:
			return
		else:
			frappe.throw("Same room no. cant exist within the building")

######alternate code written in js but still required for date validation for a scnerio when the date is set by default ######
# To validate if the start date is not after the end date in allotable room type
def dateValidate(self):
	if self.start_date > self.end_date:
		frappe.throw("Start date cannot be greater than End date")

#To create a new record in Room doctype if the record made in Building Room is schedulable and is a new record
def new_doc(self):
	exists=frappe.db.exists(self.doctype, self.name)
	if exists:
		doc = frappe.get_doc('Room', self.classroom)
		doc.room_name = self.room_name
		doc.room_number = self.room_no
		doc.seating_capacity = self.seating_capacity
		doc.save()
	if not exists and self.is_scheduled==1:
		doc = frappe.new_doc('Room')
		doc.room_name = self.room_name
		doc.room_number = self.room_no
		doc.seating_capacity = self.seating_capacity
		doc.save()
		self.db_set("classroom", doc.name)