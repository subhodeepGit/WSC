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
def get_eligibility(name):
	print("\n\n\n")
	# print(name)
	eligibility_criteria=frappe.get_all("Eligibility Criteria",{"parent":name},['qualification',"percentage","year_of_passing"])
	student_list= frappe.get_all("Educational Details" , ['qualification' , "score" , 'year_of_completion' , 'parent'] )
	
	flag = True
	student_dict = {}
	for i in student_list:
		student_dict[i['parent']] = []

	for k in eligibility_criteria:	
		for t in student_dict:
			for j in student_list:
				if j['parent'] == t:
					if k['qualification']==j["qualification"] and k['percentage'] <= j['score']:
						list_data = student_dict[j['parent']]
						list_data.append(j)
						student_dict[j['parent']]=list_data


	count_list=len(eligibility_criteria)
	for t in student_dict:
		list_data = student_dict[t]
		if len(list_data)==count_list:
			pass
		else:
			student_dict[t]=[]
	# print(student_dict)

	
	# doc = frappe.new_doc('Elgible Students')
	# doc.student_doctype_name = 
	list_keys = list(student_dict.keys())

	for i in list_keys:    #new doctype insertion
		# print(student_dict[i])
		for j in student_dict[i]:
			print(j)
			doc = frappe.new_doc('Eligible Student')
			print(doc)
			doc.student_doctype_name = j['parent']
			doc.qualification = j['qualification']
			doc.score = j['score']
			doc.year_of_completion = j['year_of_completion']
			doc.insert()

# def eligibility_check(required_marks , student_marks ,flag):
# 	if(required_marks < student_marks):
# 		return True
# 	else:
# 		return False


def validate_application_date(doc):
	if doc.application_start_date and doc.application_end_date:
		if doc.application_end_date < doc.application_start_date:
			frappe.throw(_('Application_end_date <b>{0}</b> should be greater than application_start_date <b>{1}</b>.').format(doc.application_end_date, doc.application_start_date))

