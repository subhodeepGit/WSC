# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Floor(Document):

	def validate(self):
		floor_check(self)
		if self.is_new():
			validate_floor_duplicate(self)
			validate_floor_no(self)
			number_of_rooms_data=frappe.get_all("Floor",{"building_name":self.building_name},['number_of_rooms'])
			if number_of_rooms_data:
				total_rooms = [int(rooms['number_of_rooms']) for rooms in number_of_rooms_data]
				total_rooms=sum(total_rooms)
				total_rooms=total_rooms+self.number_of_rooms 
				buildings_details_info=buildings_details(self)
				if buildings_details_info[0]['total_rooms']<total_rooms:
					frappe.throw("<b>No of Room can't be more then Total No. of rooms mentioned in Building</b>")
			else:
				buildings_details_info=buildings_details(self)
				if buildings_details_info[0]['total_rooms']<self.number_of_rooms :
					frappe.throw("<b>No of Room can't be more then Total No. of rooms mentioned in Building</b>")		
		else:
			doc_before_save = self.get_doc_before_save()
			if doc_before_save.floor_number!=self.floor_number:
				validate_floor_duplicate(self)
				validate_floor_no(self)
			number_of_rooms_data=frappe.get_all("Floor",[["building_name",'=',self.building_name],['name','!=',self.name]],['number_of_rooms'])
			total_rooms = [int(rooms['number_of_rooms']) for rooms in number_of_rooms_data]
			total_rooms=sum(total_rooms)
			total_rooms=total_rooms+self.number_of_rooms
			buildings_details_info=buildings_details(self)
			if buildings_details_info[0]['total_rooms']<total_rooms:
				frappe.throw("<b>No of Room can't be more then Total No. of rooms mentioned in Building</b>")	


def validate_floor_no(self):
	total_floors_data=frappe.get_all("Buildings",{"name":self.building_name},['total_floors'])
	no_rooms=total_floors_data[0]['total_floors']
	flag="No"
	for t in range(1,no_rooms+1):
		if t==self.floor_number:
			flag="Yes"
			break 
	if flag=="No":
		frappe.throw("Floor Is Out of Range")



def validate_floor_duplicate(self):
	if frappe.get_all("Floor",{"building_name":self.building_name,"floor_number":self.floor_number,"enabled":1}):
		frappe.throw("Floor no <b>%s</b> already exists for the building <b>%s</b> "%(self.floor_number,self.building_name))


def buildings_details(self):
	data=frappe.get_all("Buildings",{"name":self.building_name},['total_rooms'])
	return data


def floor_check(self):
	if self.floor_number<=0:
		frappe.throw("Field <b>Floor number</b> must not be zero or negative")
	
	if self.number_of_rooms<=0:
		frappe.throw("Field <b>Number of room</b> must not be zero or negative")

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def building_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT name  from `tabBuildings` WHERE `start_date`<=now() and `end_date`>=now() """)		