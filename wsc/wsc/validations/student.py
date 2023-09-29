import frappe
from frappe import _
from wsc.wsc.validations.workspace import make_workspace_for_user
from wsc.wsc.utils import duplicate_row_validation
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions

@frappe.whitelist()
def get_student_program(student):
	data=frappe.db.sql("""Select sp.program,sp.academic_term from `tabStudent Applicant` sp 
					left join `tabStudent` s on s.student_applicant=sp.name
					where s.name='{0}' and sp.docstatus=1""".format(student),as_dict=1)

	if len(data)>0:
		return data[0]

def after_insert(doc,method):
	# doc.user=doc.student_email_id
	if doc.student_applicant:
		student_applicant=frappe.get_doc("Student Applicant",doc.student_applicant)
		if student_applicant.get("previous_education_details"):
			for st_app in student_applicant.get("previous_education_details"):
				doc.append("educational_details",{
					"qualification":st_app.qualification,
					"institute":st_app.institute,
					"board":st_app.board,
					"score":st_app.score,
					"percentage":st_app.percentage_cgpa,
					"year_of_completion":st_app.year_of_completion
				})
		doc.append("current_education",{
			"programs":student_applicant.get('programs_'),
			"semesters":student_applicant.get('program'),
			"academic_year":student_applicant.get('academic_year'),
			"academic_term":student_applicant.get('academic_term')
		})

	create_user_permission(doc)
	# make_workspace_for_user(doc.doctype,doc.user)

def on_trash(doc,method):
	if frappe.db.exists("User",doc.user):
		user=frappe.get_doc("User",doc.user)
		user.module_profile=""
		user.save()
	delete_ref_doctype_permissions(["Student"],doc)

def on_update(doc,method):
	if doc.student_applicant:
		frappe.db.set_value("Student Applicant", doc.student_applicant, "application_status", "Approved")
def on_change(self,method):
	user_info=frappe.get_all("Student",{"name":self.name},["student_email_id","user"])
	if user_info[0]["user"]!=self.student_email_id and user_info[0]["user"]!= None:
		old_user=user_info[0]["user"]
		frappe.rename_doc("User", old_user, self.student_email_id)
		frappe.db.commit()
		user=frappe.get_doc("User",self.student_email_id)
		user.email=self.student_email_id
		user.save()
def validate(doc,method):
	validate_pin_code(doc)
	validate_job_date(doc)
	# attachImage(doc)s
	check_unique(doc)
	duplicate_row_validation(doc, "education_details", ['qualification','percentage'])
	duplicate_row_validation(doc, "siblings", ['full_name', 'gender'])
	duplicate_row_validation(doc, "disable_type", ['disability_type', 'percentage_of_disability'])
	records = frappe.get_all("Program Intermit Form",{"form_status":"Approve"},["student","student_name"])
def validate_job_date(doc):
	for d in doc.get("experience_detail"):
			if d.job_start_date  > d.job_end_date:
				frappe.throw("<b>Job Start Date</b> Should be Greater than <b>Job End Date</b>")  
def validate_pin_code(doc):
	
	if doc.pin_code:
		if len(doc.pin_code)<6:
			frappe.throw("<b>Pincode</b> must be 6 Digits")
	if doc.student_mobile_number:
		if len(doc.student_mobile_number)<10:
			frappe.throw("<b>Mobile Number</b> must be 10 Digits")
	if doc.fathers_contact_number:
		if len(doc.fathers_contact_number)<10:
			frappe.throw("<b>Father's Contact Number</b> must be 10 Digits")
	if doc.mothers_contact_number:
		if len(doc.mothers_contact_number)<10:
			frappe.throw("<b>Mother's Contact Number</b> must be 10 Digits")
	if doc.local_guardian_contact_no:
		if len(doc.local_guardian_contact_no)<10:
			frappe.throw("<b>Local Guardians Contact Number</b> must be 10 Digits")

	if not check_int(doc.pin_code):
		frappe.throw("Pincode must be a valid number.")
	if doc.student_mobile_number:
		if not check_int(doc.student_mobile_number):
			frappe.throw("Mobile Number must be a valid number.")
	if doc.fathers_contact_number:
		if not check_int(doc.fathers_contact_number):
			frappe.throw("Father's Contact Number must be a valid number.")
	if doc.mothers_contact_number:
		if not check_int(doc.mothers_contact_number):
			frappe.throw("Mother's Contact Number must be a valid number.")
	if doc.local_guardian_contact_no:
		if not check_int(doc.local_guardian_contact_no):
			frappe.throw("Local Guardians Contact Number must be a valid number.")

	if doc.first_name:
		if not contains_only_characters(doc.first_name):
			frappe.throw("First Name should be only characters")
	if doc.middle_name:
		if not contains_only_characters(doc.middle_name):
			frappe.throw("Middle Name should be only characters")
	if doc.last_name:
		if not contains_only_characters(doc.last_name):
			frappe.throw("Last Name should be only characters")
def contains_only_characters(first_name):
	return all(char.isalpha() or char.isspace() or char == '.' for char in first_name)
    # return all(char.isalpha() for char in first_name)

def check_int(pin_code):
	import re
	return re.match(r"[-+]?\d+(\.0*)?$", pin_code) is not None
		# frappe.throw(data)
		# return data
# def attachImage(self):
# 	if self.passport_photo!=None:
# 		self.image=self.passport_photo
def check_unique(doc):
	# make_workspace_for_user("Education",doc.user)
	"""Validates if the Student Exchange Applicant is Unique"""
	if doc.student_exchange_applicant:
		student = frappe.db.sql("select name from `tabStudent` where student_exchange_applicant=%s and name!=%s", (doc.student_exchange_applicant, doc.name))
		if student:
			frappe.throw(_("Student {0} exist against Student Exchange Applicant {1}").format(student[0][0], doc.student_exchange_applicant))

@frappe.whitelist()
def get_sem(doctype, txt, searchfield, start, page_len, filters):
	fltr = {"parent":filters.get("student")}
	if txt:
		fltr.update({"semesters":txt})
	return frappe.get_all("Current Educational Details",fltr,["semesters"],as_list=1)

@frappe.whitelist()
def get_batch(doctype, txt, searchfield, start, page_len, filters):
	fltr = {"student":filters.get("student"),"student_batch_name":("!=","")}
	if txt:
		fltr.update({"student_batch_name":txt})
	return frappe.get_all("Program Enrollment",fltr,["student_batch_name"],as_list=1)


def create_user_permission(doc):
	if doc.user:
		for stu_appl in frappe.get_all("Student Applicant",{"student_email_id":doc.user}):
			add_user_permission("Student Applicant",stu_appl.name, doc.user,doc)

		for stu_appl in frappe.get_all("Student Exchange Applicant",{"student_email_id":doc.user}):
			add_user_permission("Student Exchange Applicant",stu_appl.name, doc.user,doc)

# @frappe.whitelist()
# def get_program_intermit_students():
# 	data = frappe.get_all("Program Intermit Form",{"form_status":"Approve"},["student","student_name"])
# 	if len(data)==0 :
# 		frappe.throw("There is No Applicants to Intermit a Program")
# 	else :
# 		print("\n\n\n\n\nData is ")
# 		print(data)
# 		frappe.throw(data)
# 		return data