# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
from datetime import datetime
from frappe.model.document import Document

class EntranceExamAdmitCardTool(Document):
	pass

@frappe.whitelist()
def get_applicants(declaration):
	
	student_list = frappe.get_all("Applicant List" , {'parent':declaration , 'center_allocated_status' : 0} , [ 'applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physical_disability' , 'center_allocated_status'])
	
	return student_list
def admit_card_generate(alloted_applicant_data):
	print("\n\n\n")
	for i in alloted_applicant_data:
		if len(i) != 0:
			admit_card = frappe.new_doc("Entrance Exam Admit Card")
			admit_card.applicant_id = i['applicant_id']
			admit_card.applicant_name = i['applicant_name']
			admit_card.department = i['department']
			admit_card.academic_year = i['academic_year']
			admit_card.academic_term = i['academic_term']
			admit_card.student_category = i['student_category']
			admit_card.physical_disablity = i['physical_disability']
			admit_card.venue = i['centre_name']
			admit_card.address = i['address']
			admit_card.district = i['district']
			admit_card.pin_code = i['pincode']
			admit_card.slot = i['slot_name']
			admit_card.date_of_exam = i['starting_time'].date()
			admit_card.exam_start_time = i['starting_time'].time()
			admit_card.exam_end_time = i['ending_time'].time()
			
			admit_card.save()


@frappe.whitelist()
def student_allotment(body):
	
	print("\n\n\n\n\n")
	body = json.loads(body)
	
	declaration = body['declaration']
	de_alloted_student = body['de_allocated_student'] #### input List

	alloted_applicant_data = []
	unalloted_students_after_center_allotment = []
	for i in de_alloted_student:
		prefered_center = frappe.get_all("Exam Centre Preference" , {'parent' : i['applicant_id']} , ['center_name' , 'parent' , 'center'])
		data = {}
		for j in prefered_center:
			exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , 
					   {'entrance_exam_declaration' : declaration , 'centre': j['center']} , 
					 	['name' ,
						'academic_year' , 'academic_term' ,
						'department' ,
						'centre' , 'centre_name' , 'address' ,
						'district' , 'state' , 'pin_code'])
			
			slots = frappe.get_all("Exam Slot Timings" , {'parent': exam_center_allocation[0]['name']} , 
			  ['slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'seating_capacity' , 'parent'])
			
			for k in slots:
				if k['seating_capacity'] > 0 and i['center_allocated_status'] == 0:
				# if k['seating_capacity'] > 0:
						# print("if is true")
						data['applicant_id'] = i['applicant_id']
						data['applicant_name'] = i['applicant_name']
						data['gender'] = i['gender']
						data['student_category'] = i['student_category']
						data['physical_disability'] = i['physical_disability']
						data['academic_year'] = exam_center_allocation[0]['academic_year']
						data['academic_term'] = exam_center_allocation[0]['academic_term']
						data['department'] = exam_center_allocation[0]['department']
						data['centre'] = exam_center_allocation[0]['centre']
						data['centre_name'] = exam_center_allocation[0]['centre_name']
						data['address'] = exam_center_allocation[0]['address']
						data['district'] = exam_center_allocation[0]['district']
						data['state'] = exam_center_allocation[0]['state']
						data['pincode'] = exam_center_allocation[0]['pin_code']
						data['slot_name'] = k['slot_name']
						data['starting_time'] = k['slot_starting_time']
						data['ending_time'] = k['slot_ending_time']
						data['seating_capacity'] = k['seating_capacity']
						
						i['center_allocated_status'] = 1				
						frappe.db.sql("""
								UPDATE `tabExam Slot Timings` SET seating_capacity = '{current_capacity}' WHERE parent = '{parent}' AND slot_name = '{slot_name}'
						""".format(current_capacity = k['seating_capacity'] - 1 , parent = exam_center_allocation[0]['name'] , slot_name = k['slot_name']))	

						frappe.db.sql(""" 
								UPDATE `tabApplicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}'
							""".format(applicant_id = i['applicant_id']))   

						frappe.db.sql("""
								UPDATE `tabDeAllotted Applicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}'
							""".format(applicant_id = i['applicant_id']))

		
		data2 = {}
		if i['center_allocated_status'] == 1:
			alloted_applicant_data.append(data) #### output list 
		else:
			data2['applicant_id'] = i['applicant_id']
			data2['applicant_name'] = i['applicant_name']
			data2['gender'] = i['gender']
			data2['student_category'] = i['student_category']
			data2['physical_disability'] = i['physical_disability']
			unalloted_students_after_center_allotment.append(data2)
			

	available_center_with_slots = frappe.db.sql("""
		SELECT 
			slot.slot_name , 
			slot.seating_capacity , 
			slot.slot_starting_time ,
			alot.name , 
			alot.centre_name , 
			alot.district
			FROM `tabExam Slot Timings` slot INNER JOIN `tabEntrance Exam Centre Allocation` alot  WHERE slot.parent = alot.name AND slot.seating_capacity > 0 AND alot.docstatus = 1;
	""",as_dict=1)	

	admit_card_generate(alloted_applicant_data)
	
	return {
		'leftovers':unalloted_students_after_center_allotment,
		'available_centers':available_center_with_slots
	}

@frappe.whitelist()
def leftovers_allotment(body):
	body = json.loads(body)
	print("\n\n\n")
	
	declaration = body['declaration']
	leftover_applicant = body['leftovers']
	center = body['center']
	print(leftover_applicant)
	slot_date = datetime.strptime(center[3], '%Y-%m-%d').date()
	alloted_applicant_data= []
	unalloted_applicants = []
	for i in leftover_applicant:
		data = {}
		exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , 
					   				{'entrance_exam_declaration' : declaration , 'centre_name':center[0] , 'district' : center[2]} , 
					 					['name' ,
										'academic_year' , 'academic_term' ,
										'department' ,
										'centre' , 'centre_name' , 'address' ,
										'district' , 'state' , 'pin_code'
										])
		slots = frappe.get_all("Exam Slot Timings" , {'parent': exam_center_allocation[0]['name']} ,  
			  ['slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'seating_capacity' , 'parent'])
		
		for j in slots:
		
			if j['slot_name'] == center[1] and slot_date == j['slot_starting_time'].date():
				data['applicant_id'] = i['applicant_id']
				data['applicant_name'] = i['applicant_name']
				data['gender'] = i['gender']
				data['student_category'] = i['student_category']
				data['physical_disability'] = i['physical_disability']
				data['academic_year'] = exam_center_allocation[0]['academic_year']
				data['academic_term'] = exam_center_allocation[0]['academic_term']
				data['department'] = exam_center_allocation[0]['department']
				data['centre'] = exam_center_allocation[0]['centre']
				data['centre_name'] = exam_center_allocation[0]['centre_name']
				data['address'] = exam_center_allocation[0]['address']
				data['district'] = exam_center_allocation[0]['district']
				data['state'] = exam_center_allocation[0]['state']
				data['pincode'] = exam_center_allocation[0]['pin_code']
				data['slot_name'] = j['slot_name']
				data['starting_time'] = j['slot_starting_time']
				data['ending_time'] = j['slot_ending_time']
				data['seating_capacity'] = j['seating_capacity']

				i['center_allocated_status'] = 1				
				frappe.db.sql("""
						UPDATE `tabExam Slot Timings` SET seating_capacity = '{current_capacity}' WHERE parent = '{parent}' AND slot_name = '{slot_name}'
				""".format(current_capacity = j['seating_capacity'] - 1 , parent = exam_center_allocation[0]['name'] , slot_name = j['slot_name']))	

				frappe.db.sql(""" 
						UPDATE `tabApplicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}'
					""".format(applicant_id = i['applicant_id']))   

				frappe.db.sql("""
						UPDATE `tabDeAllotted Applicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}'
					""".format(applicant_id = i['applicant_id']))
				
		data2 = {}
		if i['center_allocated_status'] == 1:
			alloted_applicant_data.append(data) #### output list 
		else:
			data2['applicant_id'] = i['applicant_id']
			data2['applicant_name'] = i['applicant_name']
			data2['gender'] = i['gender']
			data2['student_category'] = i['student_category']
			data2['physical_disability'] = i['physical_disability']
			unalloted_applicants.append(data2)
	
	available_center_with_slots = frappe.db.sql("""
		SELECT 
			slot.slot_name , 
			slot.seating_capacity , 
			slot.slot_starting_time ,
			alot.name , 
			alot.centre_name , 
			alot.district
			FROM `tabExam Slot Timings` slot INNER JOIN `tabEntrance Exam Centre Allocation` alot  WHERE slot.parent = alot.name AND slot.seating_capacity > 0 AND alot.docstatus = 1;
	""",as_dict=1)	

	print(alloted_applicant_data)
	admit_card_generate(alloted_applicant_data)
	
	return {
		'leftovers':unalloted_applicants,
		'available_centers':available_center_with_slots
	}

