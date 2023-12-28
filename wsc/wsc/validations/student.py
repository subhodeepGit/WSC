import frappe
from frappe import _
from wsc.wsc.validations.workspace import make_workspace_for_user
from wsc.wsc.utils import duplicate_row_validation
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from frappe.desk.form.linked_with import get_linked_doctypes

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
	pass
	# if not self.is_new():
	# 	print("\n\n\n\n")
	# 	print(self.is_new())
	# 	print(self.name)
	# 	a=frappe.db.sql(""" select name from `tabStudent` where name="%s" """%(self.name))
	# 	print(a)
	# 	user_update(self)
	# user_info=frappe.get_all("Student",{"name":self.name},["student_email_id","user"])
	# if user_info[0]["user"]!=self.student_email_id and user_info[0]["user"]!= None:
	# 	old_user=user_info[0]["user"]
	# 	frappe.rename_doc("User", old_user, self.student_email_id)
	# 	frappe.db.commit()
	# 	user=frappe.get_doc("User",self.student_email_id)l
	# 	user.email=self.student_email_id
	# 	user.save()
	
def validate(doc,method):
	validate_email(doc)
	validate_pin_code(doc)
	validate_job_date(doc)
	# attachImage(doc)s
	check_unique(doc)
	duplicate_row_validation(doc, "education_details", ['qualification','percentage'])
	duplicate_row_validation(doc, "siblings", ['full_name', 'gender'])
	duplicate_row_validation(doc, "disable_type", ['disability_type', 'percentage_of_disability'])
	# records = frappe.get_all("Program Intermit Form",{"form_status":"Approve"},["student","student_name"])
	student = frappe.get_all("Student",{"name":doc.name},{"roll_no",'permanant_registration_number',"student_name"})
	if student:
		if doc.roll_no!=student[0]["roll_no"]:
			update_student_records_roll(doc)
		if doc.permanant_registration_number!=student[0]["permanant_registration_number"]:
			update_student_records_permanent_registration(doc)
		if 	doc.student_name!=student[0]["student_name"]:
			update_student_name_in_linked_doctype(doc)

	if not doc.is_new():
		if validate_email(doc):
			user_update(doc)

	# student = frappe.get_all("Student",{"name":doc.name},{"roll_no"})
	# if student:
	# 	if doc.roll_no!=student[0]["roll_no"]:
	# 		roll(doc)
			


def user_update(self):
	present_email=self.student_email_id
	doc_before_save = self.get_doc_before_save()
	old_email=doc_before_save.student_email_id
	if present_email!=old_email:
		frappe.rename_doc("User", old_email, present_email)
		frappe.db.commit()
		user=frappe.get_doc("User",self.student_email_id)
		user.email=self.student_email_id
		user.save()
		if self.user: 
			self.user=present_email
		if self.student_applicant:
			frappe.db.sql(""" UPDATE `tabStudent Applicant` SET  student_email_id='%s' WHERE name='%s' """%(present_email,self.student_applicant))


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

def roll(doc):
    id_card = frappe.db.get_all("Identity Card",filters=[["student","=",doc.name]],fields=["name"])
    if id_card:
        if len(id_card)==1:
            frappe.db.sql(""" update `tabIdentity Card` set roll_no="%s" where name = "%s" """%(doc.roll_no,id_card[0]["name"]))
        else:
            id_info=tuple([t["name"] for t in id_card])
            frappe.db.sql(""" update `tabIdentity Card` set roll_no="%s" where name in %s"""%(doc.roll_no,id_info))


def update_student_records_roll(self):
	linked_doctypes = get_linked_doctypes("Student")
	for d in linked_doctypes:
		meta = frappe.get_meta(d)
		if not meta.issingle:
			if "roll_no" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student" and d != "Student Group":			
					frappe.db.sql("""UPDATE `tab{0}` set roll_no = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.roll_no, self.name))
			if "child_doctype" in linked_doctypes[d].keys() and "roll_no" in [
				f.fieldname for f in frappe.get_meta(linked_doctypes[d]["child_doctype"]).fields
			]:
				frappe.db.sql(
					"""UPDATE `tab{0}` set roll_no = %s where {1} = %s""".format(
						linked_doctypes[d]["child_doctype"], linked_doctypes[d]["fieldname"][0]
					),
					(self.roll_no, self.name),
				)


def update_student_records_permanent_registration(self):
	linked_doctypes = get_linked_doctypes("Student")
	for d in linked_doctypes:
		meta = frappe.get_meta(d)
		if not meta.issingle:			
			if "permanent_registration_number" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student":
					frappe.db.sql("""UPDATE `tab{0}` set permanent_registration_number = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.permanant_registration_number, self.name))
			if "permanant_registration_number" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student":
					frappe.db.sql("""UPDATE `tab{0}` set permanant_registration_number = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.permanant_registration_number, self.name))
			if "registration_number" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student":
					frappe.db.sql("""UPDATE `tab{0}` set registration_number = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.permanant_registration_number, self.name))				


def update_student_name_in_linked_doctype(self):
	linked_doctypes = get_linked_doctypes("Student")
	for d in linked_doctypes:
		meta = frappe.get_meta(d)
		if not meta.issingle:
			if "student_name" in [f.fieldname for f in meta.fields]:
				if d != "Student":
					frappe.db.sql(
						"""UPDATE `tab{0}` set student_name = %s where {1} = %s""".format(
							d, linked_doctypes[d]["fieldname"][0]
						),
						(self.student_name, self.name),
					)

			if "child_doctype" in linked_doctypes[d].keys() and "student_name" in [
				f.fieldname for f in frappe.get_meta(linked_doctypes[d]["child_doctype"]).fields
			]:
				frappe.db.sql(
					"""UPDATE `tab{0}` set student_name = %s where {1} = %s""".format(
						linked_doctypes[d]["child_doctype"], linked_doctypes[d]["fieldname"][0]
					),
					(self.student_name, self.name),
				)

def validate_email(doc):
    import re
    if doc.student_email_id:
        # Updated regular expression to allow only periods in the email address
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', doc.student_email_id):
            frappe.throw("<b>{0}</b> is an invalid email address. Please enter a valid email address.".format(doc.student_email_id))
            return False
    return True
