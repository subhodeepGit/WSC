# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Floor(Document):
	def on_submit(self):
		#maximum number of floors that can be created for self.building
		building_total_floor = frappe.db.get_value("Buildings",{"name":self.building_name},["total_floors"])
		building_total_rooms = frappe.db.get_value("Buildings",{"name":self.building_name},["total_rooms"])
		
		#room that have been created for current building
		existing_floor_dict = frappe.db.sql("select count(*) from `tabFloor` where docstatus = 1 and building_name=%s",self.building_name, as_dict=True)
		created_room = existing_floor_dict[0]["count(*)"]

		total_rooms_floor_dict = frappe.db.sql("select SUM(number_of_rooms) from `tabFloor` where docstatus = 1 and building_name=%s",self.building_name, as_dict=True)
		total_rooms_floor = total_rooms_floor_dict[0]["SUM(number_of_rooms)"]

		if created_room > building_total_floor:
			frappe.throw("Maximum Floors defined in Building master has been reached")

		if total_rooms_floor > building_total_rooms:
			frappe.throw("Total rooms for current building exceeds the total number from Master Building form")
	
