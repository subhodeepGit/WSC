# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from frappe import msgprint, _
from wsc.wsc.notification.custom_notification import placement_drive_eligibility_mail

class PlacementDrive(Document):
	def validate(self):
		create_placement_drive_block_list(self)
		validate_application_date(self)
		self.rounds_of_placement_check()
		if(self.docstatus == 1):
			placement_drive_eligibility_mail(self)
	
	def before_submit(self):
		tentative_date_validation(self)

	def rounds_of_placement_check(self):
		rounds_of_placement = frappe.get_all("Rounds of Placement" , {"parent":self.name} , ['round_name'])
		rounds = []
		for i in rounds_of_placement:
			rounds.append(i['round_name'].lower())

		rounds_set = set(rounds)
		# error_code = 500
		if len(rounds) != len(rounds_set):
			frappe.throw("Duplicate Round Names in rounds of placement")

	def on_submit(self):
		# placement_drive_submit(self)
		self.set_permission_to_enroll_student()


	def on_cancel(self):
		# self.delete_placement_tool_records()
		self.delete_student_permission()

	def set_permission_to_enroll_student(self):
		for stu in frappe.get_all("Current Educational Details",{"semesters":["IN",[d.semester for d in self.get("for_programs")]],"academic_year":self.academic_year,"academic_term":self.academic_term,"parent":"Student"},['parent'],group_by="parent"):
			docshare = frappe.new_doc('DocShare')
			docshare.user = frappe.db.get_value("Student",stu.parent,'user')
			docshare.share_doctype = self.doctype
			docshare.share_name = self.name
			docshare.read = 1
			docshare.select = 1
			docshare.share=1
			docshare.insert(ignore_permissions=True)

	def delete_student_permission(self):
		for d in frappe.get_all("DocShare",{"share_doctype":self.doctype,"share_name":self.name},['name']):
			frappe.delete_doc("DocShare",d.name)

	# def delete_placement_tool_records(self):
	# 	get_placement_tool_records = frappe.db.sql(""" SELECT name FROM `tabPlacement Tool` WHERE placement_drive_name='%s'"""%(self.name))
	# 	for d in get_placement_tool_records:
	# 		print('\n\n\n')
	# 		print(d)
	# 		print('\n\n\n')
	# 		pass
	# 	frappe.throw('200')
	
@frappe.whitelist()
def get_eligibility(body):
	#from placement drive
	body = json.loads(body)

	name = body['name']

	academic_year = body['academic_year']
	academic_term = body['academic_term']

	backlog = int(body['backlog'])
	req_cgpa = float(body['required_cgpa'])
	placement_drive_for = body['placement_drive_for'].lower()
	
	program = body['program']  #need loops
	eligibility_criteria = body['eligibility_criteria'] #need loops

	final_student_list=[]
	student_dict = {}
	
	for j in program:
		
		current_education= frappe.get_all("Current Educational Details" ,
				    		{	
								"academic_year":academic_year ,
	    						"academic_term":academic_term ,
								"programs":j['programs'],
								"semesters":j['semester']
							} , 
							['programs' , 'semesters' , 'academic_year' , 'academic_term',"parent"]) #from students.

		
		for t in current_education:
			# print(t , "zetoth")
			student_dict[t['parent']] = []
			# final_student_list.append(t)

	for t in student_dict:
		
		count = 0
# 'docstatus' : 1
		placement_drive_appl_status = frappe.get_all("Placement Drive Application" , {'student': t , 'docstatus' : 1} , ['student' , 'placement_drive' , 'status'])

		status_appl_drive = 0
		print(placement_drive_appl_status , "\n")
		for m in placement_drive_appl_status:
			if m['status'].lower() == 'hired':
				status_appl_drive = 1
				break

		# print(t, "first\n")
		print(status_appl_drive, "\n")
		if status_appl_drive == 1:
			print
			continue
		else:
			print(t, name , "\n")
			student_list= frappe.get_all("Educational Details",{"parent":t}, ['qualification',"score",'year_of_completion','parent'])  #from student
			experience_detail = frappe.get_all("Experience child table" , {"parent":t} , ['job_duration'])  #from student  #can be empty
			student_cgpa = frappe.get_all("Exam Assessment Result" , {"student":t, "docstatus":1} , ['name' ,'overall_cgpa'])

			print(student_cgpa , "\n cgpa")
			print(experience_detail , "\n exp")
			print(student_list , "\n past score")

			if(len(student_cgpa) != 0 and len(student_list) != 0):
				backlog_record = frappe.get_all("Evaluation Result Item" , {"parent":student_cgpa[0]['name']} , ['result' , 'parent'])  
				for m in backlog_record:

					if m['result'] == 'F':
						count+=1
			
				if len(experience_detail) == 0 and placement_drive_for == "freshers":  #For freshers only
					print("fresh\n")
					for k in student_list:
							for j in eligibility_criteria:	
								if k['qualification'] == j['qualification'] and k['score'] >= j['percentage'] and req_cgpa <= student_cgpa[0]['overall_cgpa'] and count <= backlog:
									# list_data.append(k)
									final_student_list.append(k)
									
				elif len(experience_detail) > 0 and placement_drive_for == "experience": #For Experience only
					print("exp details\n")
					for k in student_list:
						for j in eligibility_criteria:	
							if k['qualification'] == j['qualification'] and k['score'] >= j['percentage'] and req_cgpa <= student_cgpa[0]['overall_cgpa'] and count <= backlog:
								# list_data.append(k)
								final_student_list.append(k)

				elif placement_drive_for == "both":
					print("both\n")
					for k in student_list:
						for j in eligibility_criteria:	
							if k['qualification'] == j['qualification'] and k['score'] >= j['percentage'] and req_cgpa <= student_cgpa[0]['overall_cgpa'] and count <= backlog:
								# list_data.append(k)
								final_student_list.append(k)
			else:
				continue	
	for i in final_student_list:
		
		student = frappe.get_all("Exam Assessment Result" , {"student":i['parent']} , ['academic_year' , 'programs' , 'student_name'])
		
		i['student_name'] = student[0]['student_name']
		i['academic_year'] = student[0]['academic_year']
		i['programs'] = student[0]['programs']
	return final_student_list

	
def validate_application_date(doc):
	if doc.application_start_date and doc.application_end_date:
		if doc.application_end_date < doc.application_start_date:
			frappe.throw(_('Application_end_date <b>{0}</b> should be greater than application_start_date <b>{1}</b>.').format(doc.application_end_date, doc.application_start_date))


@frappe.whitelist()
def create_placement_drive_block_list(self):
	blocklist_count = frappe.db.sql(""" SELECT Count(*) FROM `tabPlacement Blocked Student` WHERE placement_drive_id = '%s'"""%(self.name))
	if(blocklist_count[0][0] == 0):
		result = frappe.new_doc('Placement Blocked Student')
		result.date = self.posting_date
		result.academic_year = self.academic_year
		result.placement_drive_id = self.name
		result.append("block_drive_list",{
			"placement_drive" : self.name,
			"placement_drive_name" : self.title
		})
		for d in self.get("for_programs"):
			result.append("for_courses",{
				"programs":d.programs,
				"semester": d.semester
			})
		result.save()
		get_blocklist_name = frappe.db.sql(""" SELECT name FROM `tabPlacement Blocked Student` WHERE placement_drive_id = '%s'"""%(self.name))
		self.blocklist_id = get_blocklist_name[0][0]

def tentative_date_validation(self):
	if(self.tentative_joining_date):
		for d in self.get('rounds_of_placement_table'):
			if(self.tentative_joining_date < d.date):
				frappe.throw('Tentative Joining Date cannot be before date of the placement rounds')