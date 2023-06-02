# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class AdmitCardGenerationTool(Document):
	pass

@frappe.whitelist()
def get_slots(center_allocation):
	
	center_slots = frappe.get_all('Exam Slot Timings' , {'parent':center_allocation} , ['slot_name' , 'slot_starting_time' , 'slot_ending_time'])

	return center_slots

@frappe.whitelist()
def get_applicants(centre_allocation):
	
	exam_dec = frappe.get_all("Entrance Exam Centre Allocation" , {'name':centre_allocation} , ['entrance_exam_declaration'])

	student_list = frappe.get_all("Applicant List" , {'parent':exam_dec[0]['entrance_exam_declaration']} , [ 'applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physical_disability' , 'center_allocated_status'])
	
	return student_list

@frappe.whitelist()
def slot_timings(slot , parent):
	print("\n\n\n")
	print(slot)
	selected_slot = frappe.get_all("Exam Slot Timings" , { 'slot_name':slot , 'parent':parent } , ['slot_starting_time' , 'slot_ending_time'])
	
	return selected_slot

@frappe.whitelist()
def student_allotment(body):
	print("\n\n\n\n\n")
	data = json.loads(body)
	print(data)