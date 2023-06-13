# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class EntranceExamAdmitCardTool(Document):
	pass

@frappe.whitelist()
def get_applicants(declaration):
	
	student_list = frappe.get_all("Applicant List" , {'parent':declaration} , [ 'applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physical_disability' , 'center_allocated_status'])
	
	return student_list

@frappe.whitelist()
def student_allotment(declaration):
	print("\n\n\n\n\n")
	
	# exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , {'entrance_exam_declaration' : declaration} , ['name' , 'centre' , 'centre_name' , 'address' , 'district' , 'state' , 'pin_code'])
	de_alloted_student = frappe.get_all("Applicant List" , { 'parent': declaration } , ['applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physical_disability' , 'center_allocated_status'])
	# print(exam_center_allocation)
	alloted_student_data = []

	# for i in exam_center_allocation:
	# 	slots = frappe.get_all("Exam Slot Timings" , {'parent' : i['name']} , ['parent' , 'slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'seating_capacity'])

	# 	for j in de_alloted_student:
	# 		prefered_center = frappe.get_all("Exam Centre Preference" , {'parent' : j['applicant_id']} , ['state' , 'districts' , 'center_name' , 'cityvillage' , 'parent'])
	# 		print(prefered_center)
			# for k in prefered_center

	for  i in de_alloted_student:
		
		prefered_center = frappe.get_all("Exam Centre Preference" , {'parent' : i['applicant_id']} , ['state' , 'districts' , 'center_name' , 'cityvillage' , 'parent' , 'center'])
		# print(prefered_center)
		data = {}
		for k in prefered_center:
			exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , {'entrance_exam_declaration' : declaration , 'centre' : k['center']} , ['name' , 'centre' , 'centre_name' , 'address' , 'district' , 'state' , 'pin_code'])
			
			for j in exam_center_allocation:
				slots = frappe.get_all("Exam Slot Timings" , {'parent':j['name']} , ['slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'seating_capacity' , 'parent'])
				
				for m in slots:
					if j['centre'] == k['center'] and m['seating_capacity'] > 0:
						print("alot center")
						data['applicant_id'] = i['applicant_id']
						data['applicant_name'] = i['applicant_name']
						data['gender'] = i['gender']
						data['student_category'] = i['student_category']
						data['physical_disability'] = i['physical_disability']
						data['centre_name'] = j['centre_name']
						data['address'] = j['address']
						data['district'] = j['district']
						data['state'] = j['state']
						data['pincode'] = j['pin_code']
						data['slot_name'] = m['slot_name']
						data['starting_time'] = m['slot_starting_time']
						data['ending_time'] = m['slot_ending_time']
				# print(data)
			alloted_student_data.append(data)
				
	print(alloted_student_data)