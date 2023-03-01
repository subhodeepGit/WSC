# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import msgprint, _
from wsc.wsc.notification.custom_notification import placement_drive_submit

class PlacementDrive(Document):
	def validate(self):
		validate_application_date(self)
		self.rounds_of_placement_check()

	def rounds_of_placement_check(self):
		rounds_of_placement = frappe.get_all("Rounds of Placement" , {"parent":self.name} , ['round_name'])
		rounds = []
		for i in rounds_of_placement:
			rounds.append(i['round_name'].lower())

		rounds_set = set(rounds)
		# error_code = 500
		if len(rounds) != len(rounds_set):
			print(len(rounds) , len(rounds_set))
			frappe.throw("Duplicate Round Names in rounds of placement")

	def on_submit(self):
		placement_drive_submit(self)
		self.set_permission_to_enroll_student()


	def on_cancel(self):
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
	
@frappe.whitelist()
def get_eligibility(name , academic_year , academic_term , placement_drive_for , required_cgpa , backlog):
	backlog = int(backlog)
	req_cgpa = float(required_cgpa)
	placement_drive_for = placement_drive_for.lower()

	programs = frappe.get_all("Place Eligible Programs" , {"parent":name} , ['programs' , 'semester'])  #from placement drive

	eligibility_criteria=frappe.get_all("Eligibility Criteria",{"parent":name},['qualification',"percentage","year_of_passing"]) #from placement drive
	
	final_studnet_list=[]
	student_dict = {}
	for j in programs:
		
		current_education= frappe.get_all("Current Educational Details" ,
				    		{	
								"academic_year":academic_year ,
	    						"academic_term":academic_term ,
								"parenttype":"Student" ,
								"programs":j['programs'],
								"semesters":j['semester']
								    } , 
							['programs' , 'semesters' , 'academic_year' , 'academic_term',"parent","name"]) #from students.
		for t in current_education:
			student_dict[t['parent']] = []
			final_studnet_list.append(t)
	
	
	for t in student_dict:
		student_list= frappe.get_all("Educational Details",{"parent":t}, ['qualification',"score",'year_of_completion','parent'])  #from student
		experience_detail = frappe.get_all("Experience child table" , {"parent":t} , ['job_duration' , 'parent'])  #from student
		student_cgpa = frappe.get_all("Exam Assessment Result" , {"student":t, "docstatus":1} , ['name' ,'overall_cgpa' , 'result'])
		backlog_record = frappe.get_all("Evaluation Result Item" , {"parent":student_cgpa[0]['name']} , ['result' , 'parent'])  

		count = 0
		for m in backlog_record:

			if m['result'] == 'F':
				count+=1
		
		list_data = student_dict[t]

		if len(experience_detail) == 0 and placement_drive_for == "freshers":  #For freshers only
			
			for k in student_list:
					for j in eligibility_criteria:	
						if k['qualification'] == j['qualification'] and k['score'] >= j['percentage'] and req_cgpa <= student_cgpa[0]['overall_cgpa'] and count >= backlog:
							list_data.append(k)

		elif len(experience_detail) > 0 and placement_drive_for == "experience": #For Experience only
			
			for k in student_list:
				for j in eligibility_criteria:	
					if k['qualification'] == j['qualification'] and k['score'] >= j['percentage'] and req_cgpa <= student_cgpa[0]['overall_cgpa'] and count >= backlog:
						list_data.append(k)

		elif placement_drive_for == "both":
			
			for k in student_list:
				for j in eligibility_criteria:	
					if k['qualification'] == j['qualification'] and k['score'] >= j['percentage'] and req_cgpa <= student_cgpa[0]['overall_cgpa'] and count >= backlog:
						list_data.append(k)

		student_dict[t]=list_data

	for i in student_dict:
		for j in final_studnet_list:
			for k in student_dict[i]:
				k['programs'] = j['programs']
				k['academic_year'] = j['academic_year']
				k['name'] = j['name']
	
	return student_dict

	
def validate_application_date(doc):
	if doc.application_start_date and doc.application_end_date:
		if doc.application_end_date < doc.application_start_date:
			frappe.throw(_('Application_end_date <b>{0}</b> should be greater than application_start_date <b>{1}</b>.').format(doc.application_end_date, doc.application_start_date))

