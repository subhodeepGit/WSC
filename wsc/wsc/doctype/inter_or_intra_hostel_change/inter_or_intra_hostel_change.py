# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InterorIntraHostelChange(Document):
	# @frappe.whitelist()
	def validate(doc):
		if doc.allotment_no == doc.second_allotment_no:
			frappe.throw("Same student can't inter/intra change hostels!!!")
			if doc.room_type != doc.second_room_type:
				frappe.throw("Room Type of the students has to be same!!")
				if doc.first_rid == doc.second_rid:
					frappe.throw("Both the students belong to the same room!!")			
	
	def on_submit(doc):
		if doc.allotment_no != doc.second_allotment_no:
			if doc.room_type == doc.second_room_type:
				if doc.first_rid != doc.second_rid:
					frappe.db.sql("""UPDATE `tabRoom Allotment` SET `hostel_id`="%s", `room_id`="%s", `room_number`="%s" WHERE `name`="%s" """%\
										(doc.second_hostel_name,doc.second_rid,doc.second_room_no,doc.allotment_no))
					frappe.db.sql("""UPDATE `tabRoom Allotment` SET `hostel_id`="%s", `room_id`="%s", `room_number`="%s" WHERE `name`="%s" """%\
										(doc.hostel_name,doc.first_rid,doc.room_no,doc.second_allotment_no))
		# 		else:
		# 			frappe.throw("Both the students belong to the same room!!")
		# 	else:
		# 		frappe.throw("Room Type of the students has to be same!!")
		# else:
		# 	frappe.throw("Same student can't inter/intra change hostels!!!")

	def on_cancel(doc):
		if doc.allotment_no != doc.second_allotment_no:
			if doc.room_type == doc.second_room_type:
				if doc.first_rid != doc.second_rid:
					frappe.db.sql("""UPDATE `tabRoom Allotment` SET `hostel_id`="%s", `room_id`="%s", `room_number`="%s" WHERE `name`="%s" """%\
										(doc.hostel_name,doc.first_rid,doc.room_no,doc.allotment_no))
					frappe.db.sql("""UPDATE `tabRoom Allotment` SET `hostel_id`="%s", `room_id`="%s", `room_number`="%s" WHERE `name`="%s" """%\
										(doc.second_hostel_name,doc.second_rid,doc.second_room_no,doc.second_allotment_no))
				else:
					frappe.throw("Both the students belong to the same room!!")
			else:
				frappe.throw("Room Type of the students has to be same!!")
		else:
			frappe.throw("Same student can't inter/intra change hostels!!!")


@frappe.whitelist()
def get_allotment_data(allotment_no=None):
	if allotment_no:
		for d in frappe.get_all("Room Allotment",{'name':allotment_no},['student','student_name','roll_no','allotment_type','hostel_id','room_id','room_type','room_number']):
			return d

@frappe.whitelist()
def get_second_allotment_data(second_allotment_no=None):
	if second_allotment_no:
		for d in frappe.get_all("Room Allotment",{'name':second_allotment_no},['student','student_name','hostel_id','room_number','room_type','roll_no','allotment_type','room_id',]):
			return d
