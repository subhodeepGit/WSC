import frappe
from wsc.wsc.notification.custom_notification import send_mail_to_jobapplicants
from datetime import datetime

def validate(doc,method):
    if doc.total_years_of_experience<0 :
        frappe.throw("Total Years of Experience  Cannot be Negative")
    if doc.years_of_experience_for_the_position<0 :
        frappe.throw("Experience For the Position Cannot be Negative")

def before_save(doc,method):
    if doc.is_new():
        doc.doc_before_save = None
    else:
        doc.doc_before_save = frappe.get_doc("Job Opening", doc.name)


def on_update(doc,method):
    if doc.doc_before_save:
        # Compare field values before saving
        if doc.application_deadline:
        
            application_deadline = datetime.strptime(doc.application_deadline, "%Y-%m-%d %H:%M:%S")
            if doc.doc_before_save.application_deadline!=application_deadline:
                send_mail_to_jobapplicants(doc)
            print(doc.doc_before_save.application_deadline!=doc.application_deadline)
        else :
            frappe.throw("Kindly Enter the Application Deadline Before Save")


