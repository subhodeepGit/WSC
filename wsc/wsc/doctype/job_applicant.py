import frappe
from frappe import _

def update_document(doc, method):
    doc.save()
 
def setup_workflow():
    return {
        
    }

# Attach the update_document function to the "Update" button
doc_events = {
    "Doctype": {
        "on_update": update_document
    }
}

def submit_document(doc):
    # Your custom logic before submitting (if needed)
    
    # Set the document status to "Submitted"
    doc.docstatus = 1
    
    # Your custom logic after submitting (if needed)

def setup_workflow(doc):
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
    delete_user_permission(doc)
    if doc.current_status=="Applied":
        submit_document(doc)
        setup_workflow(doc)
def on_update(doc,method):
    delete_user_permission(doc)
    if doc.current_status=="Applied":
        submit_document(doc)
        setup_workflow(doc)

def on_change(doc,method):
    delete_user_permission(doc)
    if doc.current_status=="Applied":
        submit_document(doc)
        setup_workflow(doc)


def validate(doc,method):
    validate_duplicate_record(doc)
    delete_user_permission(doc)
    if doc.current_status=="Applied":
        submit_document(doc)
        setup_workflow(doc)

    
# Adding Data in Previous Application Details Table
def validate_duplicate_record(self):
        duplicateForm=frappe.get_all("Job Applicant", filters={
			"application_year":self.application_year,
			"job_title": self.job_title,
			"designation":self.designation,
            "current_status":self.current_status
		})
        if duplicateForm:
            frappe.throw(("Job Applicant is already Filled the form for this Year."))
@frappe.whitelist()
def previous_applied(aadhar_number):
    job_applicant = frappe.get_all('Job Applicant',{'aadhar_card_number':aadhar_number},['name','applicant_name','aadhar_card_number','job_title'])
    return job_applicant

def delete_user_permission(doc):
    if doc.current_status=="Disqualified":
        delete_workflow(doc)
        delete_permissions(doc)
        delete_route_history(doc)
        for user_del in frappe.get_all("User",{"name":doc.email_id}):
            frappe.delete_doc("User",user_del.name)

def delete_workflow(doc):
    for workflow_del in frappe.get_all("Workflow Action",{"reference_name":doc.email_id,"completed_by":doc.email_id}):
        frappe.delete_doc("Workflow Action",workflow_del.name)

def delete_route_history(doc):
    for route in frappe.get_all("Route History",{"user":doc.email_id}):
        frappe.delete_doc("Route History",route.name)

def delete_permissions(doc):
    for usr in frappe.get_all("User Permission",{"allow":doc.doctype,"for_value":doc.name}):
        frappe.delete_doc("User Permission",usr.name)
    for usr in frappe.get_all("User Permission",{"reference_doctype":"Student Applicant","reference_docname":doc.name}):
        frappe.delete_doc("User Permission",usr.name)
