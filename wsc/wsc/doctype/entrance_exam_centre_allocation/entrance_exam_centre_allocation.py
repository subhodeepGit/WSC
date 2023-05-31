# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EntranceExamCentreAllocation(Document):
	pass

@frappe.whitelist()
def get_centers(center_selection):

	# center_selection = frappe.get_all('Entrance Exam Centre Selection' , { 'academic_year':academic_year , 'academic_term':academic_term } , ['name'] )

	current_centers = frappe.get_all('Current Centers' ,{'parent':center_selection }, ['center'])
	print("\n\n\n")
	print(current_centers)
	
	return current_centers

@frappe.whitelist()
def get_centers_data(center):
	
	current_centers = frappe.get_all("Current Centers" , {'center':center , 'docstatus':1} , ['center_name' ,'center_name' , 'address' , 'district' , 'state' , 'pincode'])

	return current_centers