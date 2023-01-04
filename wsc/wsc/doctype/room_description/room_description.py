# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.translate import import_translations
import datetime

class RoomDescription(Document):
	# @frappe.whitelist()
	def validate(doc):
		room_description=doc.room_description
		try:
			start_date=datetime.datetime.strptime(str(doc.start_date),'%Y-%m-%d').date()
			end_date=datetime.datetime.strptime(str(doc.end_date),'%Y-%m-%d').date()
		except ValueError:
			start_date=datetime.datetime.strptime(str(doc.start_date),'%Y-%m-%d %H:%M:%S').date()
			end_date=datetime.datetime.strptime(str(doc.end_date),'%Y-%m-%d %H:%M:%S').date()
		
		if start_date<=end_date:
			Room_des_info=frappe.db.sql("""select * from `tabRoom Description` RD where 
			RD.room_description="%s" and (RD.start_date<= now() and RD.end_date>=now())"""%(room_description))
			if len(Room_des_info)==0:
				pass
			elif len(Room_des_info)!=0 and (Room_des_info[0][12]==start_date and Room_des_info[0][13]==end_date):
				pass
			else:
				frappe.throw("Room Description already present and valid")
		else:
			frappe.throw("Kindly check the start date and End Date")
