# Copyright (c) 2024, SOUL Limited and contributors
# For license information, please see license.txt

from pydoc import doc
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils.data import today
from frappe.utils.data import getdate
from wsc.wsc.utils import duplicate_row_validation

class OnlineApplicationForm(Document):

	def on_update_after_submit(doc):
		duplicate_row_validation(doc,"program_priority",["programs"])
		check_profilePhoto(doc)
		real_applicant(doc)
		concat_name(doc)
		validate_edu_details(doc)
		validate_duplicate_record(doc)
		validate_dob(doc)
		validate_pin_code(doc)
		validate_mobile_no(doc)
		validate_adharcard(doc)
		validate_applicant_name(doc)
		get_cateogry_detail(doc)
		restrict_applicant(doc)

	def validate(doc):
		duplicate_row_validation(doc,"program_priority",["programs"])
		validate_duplicate_record(doc)
		validate_dob(doc)
		validate_pin_code(doc)
		validate_mobile_no(doc)
		validate_adharcard(doc)
		validate_applicant_name(doc)
		validate_edu_details(doc)
		get_cateogry_detail(doc)
		duplicate_row_validation(doc,"program_priority",["programs"])

	def on_submit(doc):
		duplicate_row_validation(doc,"program_priority",["programs"])
		# real_applicant(doc)
		concat_name(doc)
		frappe.db.set_value(
				"Online Application Form", doc.name,"declaration", 
				"I hereby confirm that, all the data furnished in the form are correct and if any information is found incorrect then my candidature for admission will be cancelled. In case of any wrong information leading to legal, reputational hazard for WSC, it will have the right to take legal action. The final decision of application and admission process is solely lies with WSC. WSC can change the process of admission including data at its own discretion"
			)
def restrict_applicant(doc):
	roles = frappe.get_roles(frappe.session.user)
	if doc.docstatus==1 and doc.application_status=="Approved" and "Applicant"  in roles:
		if doc.doc_approved==1:
			frappe.throw("Unable to Edit the form once the application is Approved")
			doc.doc_approved=1
	if doc.docstatus==1 and doc.application_status=="Approved":
		frappe.db.set_value("Online Application Form",doc.name,'doc_approved',1)
		for t in doc.get("program_priority"):
			if t.approve!=1:
				t.approve=1
def check_profilePhoto(doc):
	if not doc.image:
		frappe.throw("Please attach your photo on Top Left Corner of the Screen")
def concat_name(doc):
	if doc.first_name and doc.last_name and doc.middle_name:
		fname=doc.first_name
		mname=doc.middle_name
		lname=doc.last_name
		stu_name=fname + " " + mname + " " + lname
		frappe.db.set_value(
				"Online Application Form", doc.name,"title", stu_name
			)
	if doc.first_name and doc.last_name and doc.middle_name==None:
		fname=doc.first_name
		lname=doc.last_name
		stu_nam=fname + " " + lname
		frappe.db.set_value(
				"Online Application Form", doc.name,"title", stu_nam
			)
def validate_duplicate_record(doc):
		duplicateForm=frappe.get_all("Online Application Form", filters={
			"academic_term":doc.academic_term,
			"program_grade": doc.program_grade,
			"department": doc.department,
			"student_email_id":doc.student_email_id,
			"name":("!=",doc.name)
		})
		if duplicateForm:
			frappe.throw(("Student Applicant is already Filled the form for this Academic Term."))
def validate_dob(self):
	# current_date = today()
	if self.date_of_birth:
		if self.date_of_birth >= self.application_date:
			frappe.throw("Date of birth should not be today's date or future date")

def validate_pin_code(doc):
	if not (doc.pin_code).isdigit():
			frappe.throw("Field <b>Pincode</b> Accept Digits Only")
	if doc.pin_code:
		if len(doc.pin_code)<6:
			frappe.throw("Field <b>Pincode</b> must be 6 Digits")
		if len(doc.pin_code)>6:
			frappe.throw("Field <b>Pincode</b> must be 6 Digits")
	
def validate_applicant_name(doc):
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

# def education_details_validation(doc):
# 	if doc.student_category and doc.student_admission:
# 		for d in get_eligibility_parameter_list_for_category(doc.student_admission,doc.student_category):
# 			if d.parameter not in [ed.qualification for ed in doc.get("education_qualifications_details")]:
# 				frappe.throw("Please Add <b>{0}</b> in Education Details Table".format(d.parameter))

def get_document_list_by_category(doc):
	filters={"student_category":doc.student_category}
	group_by=""
	filters.update({"parent":["IN",[d.student_admission for d in doc.get('program_priority')]],"parenttype":"Student Admission"})
	group_by="document_name"

	doc_list  = frappe.db.sql("""SELECT DL.document_name, DL.mandatory, DL.is_available from `tabDocuments Template List` as DL 
	inner join `tabDocuments Template` as D on DL.parent= D.name where D.student_category='{0}' and D.academic_year = '{1}' and D.department = '{2}' ORDER BY document_name ASC""".format(doc.student_category,doc.academic_year,doc.department) ,as_dict=1)
	return doc_list if doc_list else []

# @frappe.whitelist()
# def get_eligibility_parameter_list_for_category(admission,category):
# 	parameter_list = frappe.get_all("Eligibility Parameter List",{"parent":admission,"student_category":category},['parameter'],order_by="parameter_name asc")
# 	return parameter_list

def validate_attachment(doc):
	for d in doc.get("education_qualifications_details"):
		if d.mandatory==1 and not d.board and not d.score and d.year_of_completion:
			frappe.throw("Please enter the details of <b>{0}</b>".format(d.document_name))


def validate_student_admission(doc):
	for i in doc.program_priority:
		stud_admi_data = frappe.db.sql("""SELECT CA.student_admission, CS.name from `tabProgram Priority` as CA inner join `tabStudent Applicant`  as CS on CA.parent = CS.name where CS.academic_year = '{0}' and CS.docstatus=1""".format(doc.academic_year), as_dict=1)
		if i.student_admission in [d.student_admission for d in stud_admi_data]:
			exist_data = ', '.join(map(str, [d.name for d in stud_admi_data]))
			frappe.throw("Student admission <b>'{0}'</b> already exists in Counselling Structure <b>'{1}'</b> ".format(i.student_admission, exist_data))

def validate_edu_details(doc):
	if len(doc.education_qualifications_details) == 0:
		for result in frappe.get_all("Eligibility Parameter List",{"parent":doc.student_admission,"parenttype":"Student Admission"},["parameter","percentagecgpa","is_mandatory","eligible_score"] , order_by="parameter",group_by="parameter"):
			doc.append("education_qualifications_details",{
				"qualification":result.parameter,
				"percentage_cgpa":result.percentagecgpa,
				"mandatory":result.is_mandatory,
				"admission_percentage":result.eligible_score
		})
			
def validate_adharcard(doc):
	if doc.aadhaar_no:
		if not (doc.aadhaar_no).isdigit():
			frappe.throw("Field <b>Aadhaar Number</b> Accept Digits Only")
		if len(doc.aadhaar_no)>12:
			frappe.throw("Field <b>Aadhaar Number</b> must be 12 Digits")
		if len(doc.aadhaar_no)<12:
			frappe.throw("Field <b>Aadhaar Number</b> must be 12 Digits")

def validate_mobile_no(doc):
	if doc.student_mobile_number:
		if not (doc.student_mobile_number).isdigit():
			frappe.throw("Field <b>Mobile Number</b> Accept Digits Only")
		if len(doc.student_mobile_number)>10:
			frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")
		if len(doc.student_mobile_number)<10:
			frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")


def get_cateogry_detail(doc):
	if doc.physically_disabled==0:
		if doc.student_category=="OBC" and doc.gender=="Male" and doc.physically_disabled==0:
			doc.category= "General Men"
		elif doc.student_category=="OBC" and doc.gender=="Female" and doc.physically_disabled==0:
			doc.category= "General Women"
		elif doc.student_category=="OBC" and doc.physically_disabled==1:
			doc.category = "General PWD"
		else:
			doc.category=""
		for res in frappe.get_all("Category",{"gender":doc.gender,"caste_category":doc.student_category},['name']):
			if res.name:
				doc.category= res.name
	
	if doc.physically_disabled==1:
		if doc.student_category=="OBC" and doc.physically_disabled==1:
			doc.category = "General PWD"
		for res in frappe.get_all("Category",{"caste_category":doc.student_category,"is_physically_disabled":doc.physically_disabled},['name']):
			if res.name:
				doc.category= res.name
			


@frappe.whitelist()
def get_admission_and_semester_by_program(programs,program_grade,academic_year):
	for d in frappe.get_all("Student Admission",{"admission_program":programs,"program_grade":program_grade,"academic_year":academic_year},['name','admission_program','semester']):
		return d
	return {"no_record_found":1}

# @frappe.whitelist()
# def get_cateogry_details(category):
# 	for res in frappe.get_all("Category",{"category":category},['gender']):
# 		return res
	
@frappe.whitelist()
def get_validate_course(doctype, txt, searchfield, start, page_len, filters):
	x = frappe.db.sql(""" Select admission_program from `tabStudent Admission` where department='{0}' and program_grade='{1}' and academic_term='{2}'and (applicable_for_all_gender=1 OR gender_type = '{3}') """.format(filters.get("department"),filters.get("program_grade"),filters.get("academic_term"),filters.get("gender")),dict(txt="%{}%".format(txt)))
	return x

def real_applicant(doc):	
	if doc.docstatus==1 and doc.application_status=="Approved" and doc.is_applicant_reported==1:
		student_app = frappe.get_list("Student Applicant",  filters= {"student_application_id": doc.name})
		if len(student_app)==0 and doc.docstatus==1:
			student_app = get_mapped_doc("Online Application Form", doc.name,
				{
				"Online Application Form": {
					"doctype": "Student Applicant",
					"field_map": {
						"name": "student_application_id"
					}
				},
				"Education Qualifications Details": {
					"doctype": "Education Qualifications Details"
				},
			}, ignore_permissions=True)
			student_app.save()
			# student=frappe.get_doc("Student",student)
			# student_app.student_category_1=doc.category
			# student_app.block=doc.blocks
			# student_app.district=doc.districts
			# student_app.save()