import frappe
from frappe import _
from wsc.wsc.notification.custom_notification import send_mail_to_jobapplicants_final_notification,send_mail_to_jobapplicants_notification
from datetime import datetime

def update_document(doc, method):
	roles = frappe.get_roles(frappe.session.user)
	if "HR Admin" in roles or "Admin" in roles or "Administrator" in roles:
		doc.save()
		doc.submit()
		doc.update()

 
def setup_workflow(doc):
	roles = frappe.get_roles(frappe.session.user)
	if "HR Admin" in roles or "Admin" in roles or "Administrator" in roles:
		return {
		doc.update()
	}


	roles = frappe.get_roles(frappe.session.user)
	if "HR Admin" in roles or "Admin" in roles or "Administrator" in roles:
		doc_events = {
			
			"Doctype": {
				"on_update": update_document
			}
		}

def submit_document(doc):
	roles = frappe.get_roles(frappe.session.user)
	if "HR Admin" in roles or "Admin" in roles or "Administrator" in roles:
		doc.docstatus = 1
		doc.docstatus = 0
	

def setup_workflow(doc):
	
	roles = frappe.get_roles(frappe.session.user)
	if "HR Admin" in roles or "Admin" in roles or "Administrator" in roles:
		return {
			"workflow_state_field": "docstatus",
			"states": {
				"0": _("Draft"),
				"1": _("Submitted"),
			},
			"transitions": [
				{
					"action": "Submit",
					"source": "0",
					"target": "1",
				},
			],
			"action": submit_document,
		}
def on_update_after_submit(doc,method):
	# delete_user_permission(doc)
	roles = frappe.get_roles(frappe.session.user)
	if doc.current_status=="Applied" and "HR Admin" in roles or "Admin" in roles or "Administrator" in roles:
		submit_document(doc)
		setup_workflow(doc)
	data={}
	data["email_id"]=doc.email_id
	data["job_title"]=doc.job_title
	data["current_status"]=doc.current_status
	send_mail_to_jobapplicants_final_notification(data)
	# send_mail_to_jobapplicants_notification(data)
def on_update(doc,method):
# 	delete_user_permission(doc)
	roles = frappe.get_roles(frappe.session.user)
	if doc.current_status=="Applied" and "HR Admin" in roles or "Admin" in roles or "Administrator" in roles:
		submit_document(doc)
		setup_workflow(doc)
	data={}
	data["email_id"]=doc.email_id
	data["job_title"]=doc.job_title
	data["current_status"]=doc.current_status
	send_mail_to_jobapplicants_final_notification(data)
def on_change(doc,method):
# 	delete_user_permission(doc)
	if doc.current_status=="Applied":
		submit_document(doc)
		setup_workflow(doc)

def validate(doc,method):
	# validate_duplicate_record(doc)
	# delete_user_permission(doc)
	data={}
	data["email_id"]=doc.email_id
	data["job_title"]=doc.job_title
	data["current_status"]=doc.current_status
	send_mail_to_jobapplicants_notification(data)
	my_field = doc.get("aadhar_card_number") 
	if not my_field.isdigit():
		frappe.throw("AAdhar Field must contain only digits.")
	lower_range = doc.get("lower_range") 
	higher_range =doc.get("upper_range") 


	if lower_range is not None and higher_range is not None and higher_range < lower_range:
		frappe.throw("Higher range cannot be less than the lower range.")

	roles = frappe.get_roles(frappe.session.user)
	if doc.current_status=="Applied" and "HR Admin" in roles or "Admin" in roles or "Administrator" in roles:
		submit_document(doc)
		setup_workflow(doc)
	validate_job_applicant_name(doc)
	mobile_number_validation(doc)

	#Code to throw error after submitting the form after the deadline.

	if doc.application_deadline:
		current_datetime = datetime.now()
		if current_datetime>doc.application_deadline:
			frappe.throw("Sorry, the submission deadline has expired.")
	
	

def validate_job_applicant_name(doc):
    if doc.applicant_name:
            if not contains_only_characters(doc.applicant_name):
                frappe.throw("Applicant Name should be only characters")
def contains_only_characters(applicant_name):
    return all(char.isalpha() or char.isspace() for char in applicant_name)
def mobile_number_validation(doc):

    if doc.phone_number:
        if not (doc.phone_number).isdigit():
            frappe.throw("Field <b>Mobile Number</b> Accept Digits Only")
        if len(doc.phone_number)>10:
            frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")
        if len(doc.phone_number)<10:
            frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")
        
    # if doc.alternate_number:
       
    #     if not (doc.alternate_number).isdigit():
    #         frappe.throw("Field <b>Alternate Contact Number</b> Accept Digits Only")
    #     if len(doc.alternate_number)<10:
    #         frappe.throw("Field <b>Alternate Contact Number</b> must be 10 Digits")
    #     if len(doc.alternate_number)>10:
    #         frappe.throw("Field <b>Alternate Contact Number</b> must be 10 Digits")


	
# Adding Data in Previous Application Details Table
# def validate_duplicate_record(self):
#         duplicateForm=frappe.get_all("Job Applicant", filters={
# 			"application_year":self.application_year,
# 			"job_title": self.job_title,
# 			"designation":self.designation,
#             "current_status":self.current_status,
#             "email_id":self.email_id
# 		})
#         if duplicateForm:
#             frappe.throw(("Job Applicant is already Filled the form for this Year."))
@frappe.whitelist()
def previous_applied(aadhar_number):
	job_applicant = frappe.get_all('Job Applicant',{'aadhar_card_number':aadhar_number},['name','applicant_name','aadhar_card_number','job_title'])
	return job_applicant

# def delete_user_permission(doc):
# 	if doc.current_status=="Disqualified":
# 		delete_workflow(doc)
# 		delete_permissions(doc)
# 		delete_route_history(doc)
# 		for user_del in frappe.get_all("User",{"name":doc.email_id}):
# 			frappe.delete_doc("User",user_del.name)

# def delete_workflow(doc):
# 	for workflow_del in frappe.get_all("Workflow Action",{"reference_name":doc.email_id,"completed_by":doc.email_id}):
# 		frappe.delete_doc("Workflow Action",workflow_del.name)

# def delete_route_history(doc):
# 	for route in frappe.get_all("Route History",{"user":doc.email_id}):
# 		frappe.delete_doc("Route History",route.name)

# def delete_permissions(doc):
# 	for usr in frappe.get_all("User Permission",{"allow":doc.doctype,"for_value":doc.name}):
# 		frappe.delete_doc("User Permission",usr.name)
# 	for usr in frappe.get_all("User Permission",{"reference_doctype":"Student Applicant","reference_docname":doc.name}):
# 		frappe.delete_doc("User Permission",usr.name)
