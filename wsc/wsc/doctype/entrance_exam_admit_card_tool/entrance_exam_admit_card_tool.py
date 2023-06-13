# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
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
	# de_alloted_student = frappe.get_all("Applicant List" , { 'parent': declaration } , ['applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physical_disability' , 'center_allocated_status'])
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
					if i['centre'] == l['center'] and j['seating_capacity'] > 0:
						
						data['applicant_id'] = k['applicant_id']
						data['applicant_name'] = k['applicant_name']
						data['gender'] = k['gender']
						data['student_category'] = k['student_category']
						data['physical_disability'] = k['physical_disability']
						data['academic_year'] = i['academic_year']
						data['academic_term'] = i['academic_term']
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

		alloted_student_data.append(data)
 
	for i in alloted_student_data:
		exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , {'centre':i['centre']} , ['centre' , 'name'])
		# slots = frappe.get_all("Exam Slot Timings" , {'parent':exam_center_allocation[0]['name']} , )
		frappe.db.sql("""
					UPDATE `tabExam Slot Timings` SET seating_capacity = '{current_capacity}' WHERE parent = '{parent}' AND slot_name = '{slot_name}'
				""".format(current_capacity = i['seating_capacity'] - 1 , parent = exam_center_allocation[0]['name'] , slot_name = i['slot_name']))	
		
		frappe.db.sql("""
					UPDATE `tabApplicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}'
		""".format(applicant_id = i['applicant_id']))
		print(frappe.get_all("Applicant List" , {'applicant_id': i['applicant_id']} , ['applicant_id' , 'applicant_name' , 'center_allocated_status']))

	# for  i in de_alloted_student:   
	# 	prefered_center = frappe.get_all("Exam Centre Preference" , {'parent' : i['applicant_id']} , ['state' , 'districts' , 'center_name' , 'cityvillage' , 'parent' , 'center'])
	# 	data = {}
	# 	for k in prefered_center:
	# 		exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , {'entrance_exam_declaration' : declaration , 'centre' : k['center']} , ['name' , 'centre' , 'centre_name' , 'address' , 'district' , 'state' , 'pin_code' , 'academic_year' , 'academic_term'])
			
	# 		for j in exam_center_allocation:
	# 			slots = frappe.get_all("Exam Slot Timings" , {'parent':j['name']} , ['slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'seating_capacity' , 'parent'])
				
	# 			for m in slots:
	# 				if j['centre'] == k['center'] and m['seating_capacity'] > 0:
	# 					pass
						

			# alloted_student_data.append(data)
				
	# print(alloted_student_data[1])

	# for i in alloted_student_data:
	# 	exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , {'academic_year' : i['academic_year'] , 'academic_term' : i['academic_term'] , 'centre' : i['centre']} , ['name'])
	# 	slots = frappe.get_all("Exam Slot Timings" , {'parent': exam_center_allocation[0]['name']} , ['slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'seating_capacity' , 'parent'])
		
		# for j in slots:
		# 	if i['slot_name'] == j['slot_name']:
		# 		print(j['slot_name'] , i['slot_name'])	
		
	# frappe.db.sql("""
	# 				UPDATE `tabExam Slot Timings` SET seating_capacity = '{current_capacity}' WHERE parent = '{parent}' AND slot_name = '{slot_name}'
	# 			""".format(current_capacity = m['seating_capacity'] - 1 , parent = m['parent'] , slot_name = m['slot_name']))

						#data['applicant_id'] = i['applicant_id']
						# data['applicant_name'] = i['applicant_name']
						# data['gender'] = i['gender']
						# data['student_category'] = i['student_category']
						# data['physical_disability'] = i['physical_disability']
						# data['academic_year'] = j['academic_year']
						# data['academic_term'] = j['academic_term']
						# data['centre'] = j['centre']
						# data['centre_name'] = j['centre_name']
						# data['address'] = j['address']
						# data['district'] = j['district']
						# data['state'] = j['state']
						# data['pincode'] = j['pin_code']
						# data['slot_name'] = m['slot_name']
						# data['starting_time'] = m['slot_starting_time']
						# data['ending_time'] = m['slot_ending_time']