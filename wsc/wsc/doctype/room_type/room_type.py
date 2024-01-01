# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoomType(Document):
	# @frappe.whitelist()
	def validate(doc):
		start_date=doc.start_date
		end_date=doc.end_date
		room_type=doc.room_type
		description=doc.description
		RT_info=frappe.db.sql("""SELECT * from `tabRoom Type` RT WHERE (RT.room_type="%s" and RT.description="%s") and (RT.start_date<=now() 
			and RT.end_date>=now())"""%(room_type,description))
		if len(RT_info)==0:
			if start_date<=end_date:
				pass
			else:
				frappe.throw("Kindly check the start date and End Date")
		else:
			end_date_info=RT_info[0][15]
			if end_date_info!=end_date:
				stu_info=frappe.db.sql("""SELECT * FROM `tabRoom Allotment` WHERE `room_type`="%s" and (`start_date`<=now() and `end_date`>=now())"""%(room_type))
				if len(stu_info)==0:
					room_info=frappe.db.sql("""SELECT * FROM `tabRoom Masters` WHERE `actual_room_type`="" and `validity`="Functional" """)
					if len(room_info)==0:
						pass
					else:
						frappe.throw("Can't update: Some of the rooms already assined with the room type and Functional")
				else:
					frappe.throw("Can't update: Student is already allotted for the Particular")
			else:
				pass		
