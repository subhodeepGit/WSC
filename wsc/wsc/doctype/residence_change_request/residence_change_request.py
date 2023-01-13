# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceChangeRequest(Document):
	def validate(self):
		changeRoomStatus(self)
		changeNewRoomStatus(self)
		

# To change vacancy status and employee allotment status of alloted residence and newly alloted residence
# after approval of change of residence request
def changeRoomStatus(self):
	data= self.request_status
	if data == "Approved":
		frappe.db.set_value("Residence Allotment",self.alloted_residence_serial_number,"vacancy_status","Vacant")
		frappe.db.set_value("Residence Allotment",self.alloted_residence_serial_number,"employee_allotment_status", "Not Alloted")

def changeNewRoomStatus(self):
	data= self.request_status
	if data == "Approved":
		frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Not Vacant")
		frappe.db.set_value("Building Room",self.residence_serial_number,"employee_allotment_status", "Alloted")
	

