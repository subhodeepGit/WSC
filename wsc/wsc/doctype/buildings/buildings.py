# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Buildings(Document):
	def validate(self):
		dateValidate(self)
		pincode(self)
		room_validation(self)
		self.enabled_building()
		self.enabled_land()

		if self.building_valuation_in_rs < 0:
			frappe.throw("<B> Building valuation</b> cannot be negative")

		if self.land_size_in_sq_ft < 0:
			frappe.throw("<B> Building Size</b> cannot be negative")
		
	def enabled_building(self):
		if  self.enabled==0:
			today = frappe.utils.nowdate()
			if self.end_date > today:
				frappe.throw("<b>Disabling Building in can't be in Future date</b>")

		floor_name=frappe.get_all("Floor",{"building_name":self.name},['name'])
		for t in floor_name:
			doc=frappe.get_doc("Floor",t['name'])
			doc.enabled=self.enabled
			doc.save()

	def enabled_land(self):
		for k in self.get("land_details"):
			land_plot_number_data=frappe.get_all("Land Details",[['land_plot_number','=',k.land_plot_number],
																['parenttype','IN',['Floor',"Building Room"]]],
																["parent","parenttype","name"])
			for t in land_plot_number_data:
				doc=frappe.get_doc(t['parenttype'],t['parent'])
				for j in doc.get("land_details"):
					if j.name==t['name']:
						j.enabled=k.enabled
				doc.save()

# To validate if the start date is not after the end date
def dateValidate(self):
	if self.start_date > self.end_date:
		frappe.throw("Start date cannot be greater than End date")

# Validation for pincode length			
def pincode(self):
	if self.pin_code:
		if not (self.pin_code).isdigit():
			frappe.throw("Field <b>Pin Code</b> Accept Digits Only")

	if len(self.pin_code)>6:
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

	if len(self.pin_code)<6:	
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

def room_validation(self):
	if self.total_rooms<=0:
		frappe.throw("Field <b>Total rooms</b> must not be zero or negative")
	
	if self.total_floors<=0:
		frappe.throw("Field <b>Total floors</b> must not be zero or negative")

# To fetch only those buildings which are between start and end date of the Land with respect to today’s date
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def room_type_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT name,land_complete_address from `tabLand` WHERE `start_date`<=now() and `end_date`>=now()""")




