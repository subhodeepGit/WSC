# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Land(Document):
	def validate(self):
		dateValidate(self)
		pincode(self)
		self.enabled_land()
		# phone(self)

	def enabled_land(self):
		land_details_info=frappe.get_all("Land Details",{"land_plot_number":self.name},["parent","parenttype","name"])
		for t in land_details_info:
			doc=frappe.get_doc(t['parenttype'],t['parent'])
			for j in doc.get("land_details"):
				if j.name==t['name']:
					j.enabled=self.enabled
			doc.save()
		if  self.enabled==0:
			today = frappe.utils.nowdate()
			if self.end_date > today:
				frappe.throw("<b>Disabling Land in can't be in Future date</b>")
			


# To validate if the start date is not after the end date
def dateValidate(self):
	if self.start_date > self.end_date:
		frappe.throw("Start date cannot be greater than End date")
		

# Validation for pincode length	
def pincode(self):
	if not self.pin_code:
		return

	if len(self.pin_code)>6:
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

	if len(self.pin_code)<6:	
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

def phone(self):
	if len(self.phone)>10:
		frappe.throw("Field <b>Phone number</b> must be 10 Digits")
	
	if len(self.phone)<10:
		frappe.throw("Field <b>Phone number</b> must be 10 Digits")