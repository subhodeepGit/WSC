# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import msgprint, _
from wsc.wsc.notification.custom_notification import placement_drive_submit

class PlacementDrive(Document):
	def validate(self):
		validate_application_date(self)

	def on_submit(self):

		placement_drive_submit(self)
		self.set_permission_to_enroll_student()


	def on_cancel(self):
		self.delete_student_permission()

	def set_permission_to_enroll_student(self):
		for stu in frappe.get_all("Current Educational Details",{"semesters":["IN",[d.semester for d in self.get("for_programs")]],"academic_year":self.academic_year,"academic_term":self.academic_term},['parent'],group_by="parent"):
			docshare = frappe.new_doc('DocShare')
			docshare.user = frappe.db.get_value("Student",stu.parent,'user')
			docshare.share_doctype = self.doctype
			docshare.share_name = self.name
			docshare.read = 1
			docshare.select = 1
			docshare.insert(ignore_permissions=True)

	def delete_student_permission(self):
		for d in frappe.get_all("DocShare",{"share_doctype":self.doctype,"share_name":self.name},['name']):
			frappe.delete_doc("DocShare",d.name)
	
@frappe.whitelist()
def get_eligibility(name , academic_year , academic_term , placement_drive_for):
	# print(academic_year , academic_term)

	current_education= frappe.get_all("Current Educational Details" ,{"academic_year":academic_year , "academic_term":academic_term,"parenttype":"Student"} , 
	['programs' , 'semesters' , 'academic_year' , 'academic_term',"parent","name"]) #from students.
	
	programs = frappe.get_all("Place Eligible Programs" , {"parent":name} , ['programs' , 'semester'])  #from placement drive

	eligibility_criteria=frappe.get_all("Eligibility Criteria",{"parent":name},['qualification',"percentage","year_of_passing"]) #from placement drive
	
	final_studnet_list=[]
	for j in programs:
		for t in current_education:
			# if j['programs']==t['programs'] and j['semester']==t['semesters'] :
			if j['programs'] == t['programs']:
				final_studnet_list.append(t)
	print(programs)
	student_dict = {}
	for i in final_studnet_list:
		student_dict[i['parent']] = []
	
	for t in student_dict:
		student_list= frappe.get_all("Educational Details",{"parent":t}, ['qualification',"score",'year_of_completion','parent'])  #from student
		experience_detail = frappe.get_all("Experience child table" , {"parent":i} , ['job_duration' , 'parent'])  #from student

		list_data=student_dict[t]

		for j in experience_detail:
			
			if placement_drive_for == "fresher" and j['job_duration'] == 0:
				for k in student_list:
					for j in eligibility_criteria:	
						if k['qualification'] == j['qualification'] and k['score'] >= j['percentage']:
							list_data.append(k)
			
			elif placement_drive_for == "Experience" and j['job_duration'] > 0:
				for k in student_list:
					for j in eligibility_criteria:	
						if k['qualification'] == j['qualification'] and k['score'] >= j['percentage']:
							list_data.append(k)
			
			else:
				for k in student_list:
					for j in eligibility_criteria:	
						if k['qualification'] == j['qualification'] and k['score'] >= j['percentage']:
							list_data.append(k)

		student_dict[t]=list_data
			
	for i in student_dict:
		# print(student_dict[i])
		for j in final_studnet_list:
			# print(j)
			for k in student_dict[i]:
				k['programs'] = j['programs']
				k['academic_year'] = j['academic_year']
				k['name'] = j['name']
				# print(k)
	print("\n\nstudent_dict")
	print(student_dict)
	return student_dict
	
def validate_application_date(doc):
	if doc.application_start_date and doc.application_end_date:
		if doc.application_end_date < doc.application_start_date:
			frappe.throw(_('Application_end_date <b>{0}</b> should be greater than application_start_date <b>{1}</b>.').format(doc.application_end_date, doc.application_start_date))

