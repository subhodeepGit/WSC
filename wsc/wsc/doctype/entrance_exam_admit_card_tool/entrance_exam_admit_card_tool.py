# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
import datetime
from frappe.model.document import Document

class EntranceExamAdmitCardTool(Document):
	pass

@frappe.whitelist()
def get_applicants(declaration):
	
	student_list = frappe.get_all("Applicant List" , {'parent':declaration , 'center_allocated_status' : 0} , [ 'applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physical_disability' , 'center_allocated_status'])
	
	return student_list

@frappe.whitelist()
def student_allotment(body):
	
	print("\n\n\n\n\n")
	body = json.loads(body)
	
	declaration = body['declaration']
	de_alloted_student = body['de_allocated_student']

	alloted_student_data = []

	exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , {'entrance_exam_declaration' : declaration} , 
					 		['name' , 'academic_year' , 'academic_term' , 'department' , 'centre' , 'centre_name' , 'pin_code' , 'address' , 'district' , 'state' , 'pin_code'])
	
	for i in exam_center_allocation:
		slots = frappe.get_all("Exam Slot Timings" , {'parent':i['name']} , ['slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'seating_capacity' , 'parent'])
		
		data = {}
		for j in slots:
			for k in de_alloted_student:
				prefered_center = frappe.get_all("Exam Centre Preference" , {'parent' : k['applicant_id']} , ['center_name' , 'parent' , 'center'])
				
				for l in prefered_center:
					if i['centre'] == l['center'] and j['seating_capacity'] > 0 and k['center_allocated_status'] == 0:
						
						data['applicant_id'] = k['applicant_id']
						data['applicant_name'] = k['applicant_name']
						data['gender'] = k['gender']
						data['student_category'] = k['student_category']
						data['physical_disability'] = k['physical_disability']
						data['academic_year'] = i['academic_year']
						data['academic_term'] = i['academic_term']
						data['department'] = i['department']
						data['centre'] = i['centre']
						data['centre_name'] = i['centre_name']
						data['address'] = i['address']
						data['district'] = i['district']
						data['state'] = i['state']
						data['pincode'] = i['pin_code']
						data['slot_name'] = j['slot_name']
						data['starting_time'] = j['slot_starting_time']
						data['ending_time'] = j['slot_ending_time']
						data['seating_capacity'] = j['seating_capacity']
						
						k['center_allocated_status'] = 1
		if len(data) != 0:
			alloted_student_data.append(data)

	
	for i in alloted_student_data:
		print(i['starting_time'].time())
		if len(i) != 0:

			exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , {'centre':i['centre']} , ['centre' , 'name'])
			de_alloted_student = frappe.get_all("Applicant List" , { 'applicant_id' : i['applicant_id'] } , ['center_allocated_status' , 'applicant_id'])			

			if de_alloted_student[0]['center_allocated_status'] != 0:
				frappe.db.sql("""
						UPDATE `tabExam Slot Timings` SET seating_capacity = '{current_capacity}' WHERE parent = '{parent}' AND slot_name = '{slot_name}'
					""".format(current_capacity = i['seating_capacity'] - 1 , parent = exam_center_allocation[0]['name'] , slot_name = i['slot_name']))	
			
				frappe.db.sql(""" 
						UPDATE `tabApplicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}'
					""".format(applicant_id = i['applicant_id']))   

				frappe.db.sql("""
						UPDATE `tabDeAllotted Applicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}'
				""".format(applicant_id = i['applicant_id']))

				
				admit_card = frappe.new_doc("Entrance Exam Admit Card")
				admit_card.applicant_id = i['applicant_id']
				admit_card.applicant_name = i['applicant_name']
				admit_card.department = i['department']
				admit_card.academic_year = i['academic_year']
				admit_card.academic_term = i['academic_term']
				admit_card.venue = i['centre_name']
				admit_card.address = i['address']
				admit_card.district = i['district']
				admit_card.pin_code = i['pincode']
				admit_card.slot = i['slot_name']
				admit_card.date_of_exam = i['starting_time'].date()
				admit_card.exam_start_time = i['starting_time'].time()
				admit_card.exam_end_time = i['ending_time'].time()
				
				admit_card.save()