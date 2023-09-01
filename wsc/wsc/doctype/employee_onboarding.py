import frappe
from frappe import _
from frappe.model.document import Document

from wsc.wsc.notification.custom_notification import maildirector,mailhr,mailhr_aftercomplete
def validate(doc,method):
        
        if doc.workflow_state == "Pending Approval from Director Admin":
            director_mail(doc)
        if doc.workflow_state == "Approved" or doc.workflow_state=="Rejected":
            hr_mail(doc)
        # if doc.boarding_status=="Completed":
        #     print("\n\n\n\n\n")
        #     print(doc.boarding_status)
        # print("\n\n\n\n")
        # print(doc.boarding_status)

# def on_change(doc,method):
#     print("\n\n\nOn cahnge is working")
#     print("\n\n\n\n")
#     print(doc.boarding_status)
#     hr_mail_after_complete(doc)
#     # if doc.boarding_status == "Completed":
#     #     print("\n\n\n")
#     #     hr_mail_after_complete(doc)
#     #     print("mailsent")

def on_cancel(doc,method):
    onboarding_name = doc.name
    if onboarding_name:
        activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": onboarding_name}, fields=["name","activity_name"])
        
        for activity_record in activity_records:
            # Step v: Update status field to the new status value
            # if activity_record.activity_name in doc.subject:
            # print(activity_record.activity_name)
            # print("\n\n\n")
            frappe.db.set_value("Employee Boarding Activity", activity_record.name, "status", "")

            
            # Step vi: Save changes to each On-boarding Activity document
            frappe.db.commit()
                # frappe.msgprint("Status updated in Employee Onboarding Activities")
            # else :
            #     pass
        frappe.db.set_value(doc.doctype,doc.name, "boarding_status", "Pending")
        frappe.db.commit()
def director_mail(doc):
    director_mail = frappe.get_all("User",filters={'role':"Director"},pluck='name')
    if director_mail:
        director_mail_id = director_mail[0]
        data={}
        data["director_mail"]=director_mail_id
        data["employee_onboarding"]=doc.name
        data["current_status"]=doc.workflow_state
        data["name"]=doc.job_applicant
        maildirector(data)
    else :
        frappe.throw("Setup Director User ID")
def hr_mail(doc):
    hr_mail=frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
    if hr_mail:
        hr_mail_id = hr_mail[0]
        data ={}
        data["hr_mail"]=hr_mail_id
        data["employee_onboarding"]=doc.name
        data["current_status"]=doc.workflow_state
        data["name"]=doc.job_applicant
        mailhr(data)
    else :
        frappe.throw("Setup HR Admin User ID")

@frappe.whitelist()
def hr_mail_after_complete(docname):
    onboarding = frappe.get_doc("Employee Onboarding",docname)
    print("\n\n\n\n")
    print(onboarding)
    if onboarding.boarding_status == "Completed" :

        hr_mail=frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
        if hr_mail:
            hr_mail_id = hr_mail[0]
            data ={}
            data["hr_mail"]=hr_mail_id
            data["employee_onboarding"]=onboarding.name
            data["current_status"]=onboarding.workflow_state
            data["name"]=onboarding.job_applicant
            # print("\n\n\n\n")
            # print(data)
            mailhr_aftercomplete(data)
        else :
            frappe.throw("Setup HR Admin User ID")
# @frappe.whitelist()
# def sendfinalmail():
#     hr_mail_after_complete(doc)