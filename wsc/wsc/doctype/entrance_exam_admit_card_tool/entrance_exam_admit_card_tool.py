# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
from datetime import datetime
from frappe.model.document import Document

class EntranceExamAdmitCardTool(Document):
	def validate(self):
		if frappe.get_all("Entrance Exam Admit Card Tool",{"entrance_exam_declaration":self.entrance_exam_declaration,"docstatus":1}):
			frappe.throw("Admit Card Tool is Already Published")
	
	def on_cancel(self):
		for i in self.deallotted_applicant_list:
			admit_card_data = frappe.get_all("Entrance Exam Admit Card" , {'applicant_id':i.applicant_id} , ['name'])
			if(len(admit_card_data) != 0):
				admit_card = frappe.get_doc("Entrance Exam Admit Card" , admit_card_data[0]['name'])

				if admit_card.docstatus == 1:
					admit_card.cancel()

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):
    
	############################## Search Field Code#################
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)    

	# data=frappe.db.sql("""
	#     SELECT `name` FROM `tabEntrance Exam Declaration` WHERE ({key} like %(txt)s or {scond})  and
	#         (`exam_start_date` <= now() AND `exam_end_date` >= now())
	#          and `docstatus`=1 
	# """.format(
	#     **{
	#         "key": searchfield,
	#         "scond": searchfields,
	#         # "info":info
	#     }),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	data=frappe.db.sql("""
	SELECT `name` FROM `tabEntrance Exam Declaration` WHERE ({key} like %(txt)s or {scond})
			and `docstatus`=1 
	""".format(
	**{
		"key": searchfield,
		"scond": searchfields,
		# "info":info
	}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})

	return data

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query2(doctype, txt, searchfield, start, page_len, filters):
    
    ############################## Search Field Code #################
    searchfields = frappe.get_meta(doctype).get_search_fields()
    searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)    

    data = frappe.db.sql("""
        SELECT 
			alot.name , slot.slot_name , slot.seating_capacity
		FROM 
			`tabEntrance Exam Centre Allocation` alot 
		INNER JOIN 
			`tabExam Slot Timings` slot
		ON slot.parent = alot.name
		WHERE 
			
		alot.entrance_exam_declaration = '{declartion}'				 
        AND slot.seating_capacity > 0
		AND alot.docstatus = 1
    """.format(
        **{
            "key": searchfield,
            "scond": searchfields,
			"declartion":filters['entrance_exam_declaration']
            # "info": info
        }), {"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	
	# ({key} like %(txt)s or {scond})  

    return data

@frappe.whitelist()
def get_applicants(declaration):
	
	student_list = frappe.get_all("Applicant List" , {'parent':declaration , 'center_allocated_status' : 0} , [ 'applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physical_disability' , 'center_allocated_status'])
	
	return student_list

def admit_card_generate(alloted_applicant_data):
	
	for i in alloted_applicant_data:

		if len(i) != 0:
			student_photo = frappe.get_all("Student Applicant" , { 'name':i['applicant_id'] } , ['image'])			
			admit_card_data = frappe.get_all("Entrance Exam Admit Card",{"entrance_exam":i['entrance_exam'] ,"applicant_id":i['applicant_id'] } , ['docstatus'])
			
			for j in admit_card_data:
				if j['docstatus'] == 0 or j['docstatus'] == 1:
					frappe.throw("Admit Card is Already Published")
			else:	
	
				admit_card = frappe.new_doc("Entrance Exam Admit Card")
				admit_card.phote = student_photo[0]['image']
				admit_card.entrance_exam = i['entrance_exam']
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
				admit_card.date_of_exam = i['slot_date']
				# admit_card.date_of_exam = i['starting_time'].date()
				admit_card.exam_start_time = i['starting_time']
				admit_card.exam_end_time = i['ending_time']
				
				admit_card.save()
				admit_card.submit()

@frappe.whitelist()
def student_allotment(body):
	
	body = json.loads(body)

	name = body['name']
	declaration = body['declaration']
	de_alloted_student = body['de_allocated_student'] #### input List
	
	alloted_applicant_data = []
	unalloted_students_after_center_allotment = []

	for i in de_alloted_student:
		
		prefered_center = frappe.get_all("Exam Centre Preference" , {'parent' : i['applicant_id']} , ['center_name' , 'parent' , 'center'] , order_by = "idx asc")
		data = {}
		for j in prefered_center:
			exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , 
					   {'entrance_exam_declaration' : declaration , 'centre': j['center_name'] , 'docstatus' : 1} , 
					 	['name' ,
						'academic_year' , 'academic_term' ,
						'department' ,
						'centre' , 'centre_name' , 'address' ,
						'district' , 'state' , 'pin_code'] ,
						order_by = "idx asc")
			print("\n", exam_center_allocation)
			slots = frappe.get_all("Exam Slot Timings" , {'parent': exam_center_allocation[0]['name']} , 
			  ['slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'slot_date' , 'seating_capacity' , 'parent'])
			
			for k in slots:
				if k['seating_capacity'] > 0 and i['center_allocated_status'] == 0:
				
						data['entrance_exam'] = declaration
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
						data['slot_date'] = k['slot_date']
						data['seating_capacity'] = k['seating_capacity']
						
						i['center_allocated_status'] = 1				

						frappe.db.sql("""
								UPDATE `tabExam Slot Timings` SET seating_capacity = '{current_capacity}' WHERE parent = '{parent}' AND slot_name = '{slot_name}'
						""".format(current_capacity = k['seating_capacity'] - 1 , parent = exam_center_allocation[0]['name'] , slot_name = k['slot_name']))	

						frappe.db.sql(""" 
								UPDATE `tabApplicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}' AND parent = '{declaration}' 
							""".format(applicant_id = i['applicant_id'] , declaration = declaration))   

						frappe.db.sql("""
								UPDATE `tabDeAllotted Applicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}' AND parent = '{name}'
							""".format(applicant_id = i['applicant_id'] , name = name))

		
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

	### For Flag	
	admit_card_tool = frappe.get_doc('Entrance Exam Admit Card Tool' , name)

	if len(unalloted_students_after_center_allotment) == 0:
		admit_card_tool.flag = 2
		admit_card_tool.save()
	else:
		admit_card_tool.flag = 1
		admit_card_tool.save()

	admit_card_generate(alloted_applicant_data)
	return {
		'leftovers':unalloted_students_after_center_allotment,
	}

@frappe.whitelist()
def leftovers_allotment(body):
	body = json.loads(body)
	
	name = body['name']
	declaration = body['declaration']
	leftover_applicant = body['leftovers']
	center = body['center']

	date_format = "%Y-%m-%d"
		
	alloted_applicant_data= []
	unalloted_applicants = []

	for i in leftover_applicant:
		data = {}
		exam_center_allocation = frappe.get_all("Entrance Exam Centre Allocation" , 					   				
									  {'name':center , 'docstatus' : 1} ,
					 					['name' ,
										'academic_year' , 'academic_term' ,
										'department' ,
										'centre' , 'centre_name' , 'address' ,
										'district' , 'state' , 'pin_code'
										])
		
		slots = frappe.get_all("Exam Slot Timings" , {'parent': center} ,  
			  ['slot_name' , 'slot_starting_time' , 'slot_ending_time' , 'slot_date' , 'seating_capacity' , 'parent'])
		
		for j in slots:

			if i['center_allocated_status'] == 0 and j['seating_capacity'] > 0:
				
				data['entrance_exam'] = declaration
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
				data['slot_date'] = j['slot_date']
				data['seating_capacity'] = j['seating_capacity']

				i['center_allocated_status'] = 1				
				
				frappe.db.sql("""
						UPDATE `tabExam Slot Timings` SET seating_capacity = '{current_capacity}' WHERE parent = '{parent}' AND slot_name = '{slot_name}'
				""".format(current_capacity = j['seating_capacity'] - 1 , parent = exam_center_allocation[0]['name'] , slot_name = j['slot_name']))	

				frappe.db.sql(""" 
					UPDATE `tabApplicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}' AND parent = '{declaration}' 
				""".format(applicant_id = i['applicant_id'] , declaration = declaration))   

				frappe.db.sql("""
					UPDATE `tabDeAllotted Applicant List` SET center_allocated_status = 1 WHERE applicant_id = '{applicant_id}' AND parent = '{name}'
				""".format(applicant_id = i['applicant_id'] , name = name))

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
	
	### For flag
	admit_card_tool = frappe.get_doc('Entrance Exam Admit Card Tool' , name)
	if len(unalloted_applicants) == 0:
		admit_card_tool.flag = 2
		admit_card_tool.save()
	else:
		admit_card_tool.flag = 1
		admit_card_tool.save()

	admit_card_generate(alloted_applicant_data)
	
	return {
		'leftovers':unalloted_applicants,
		# 'available_centers':available_center_with_slots
	}

