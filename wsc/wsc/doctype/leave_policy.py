
import frappe
from frappe import _
from frappe.model.document import Document

from wsc.wsc.notification.custom_notification import send_mail_to_director,send_mail_to_hr
def validate(doc,method):
        
        if doc.workflow_state == "Pending Approval":
            director_mail(doc)
        if doc.workflow_state == "Approved" or doc.workflow_state=="Rejected":
            hr_mail(doc)
        for detail in doc.get("leave_policy_details"):
            if detail.annual_allocation < 0:
                frappe.throw(_("Annual allocation cannot be negative"))
def director_mail(doc):
    director_mail = frappe.get_all("User",filters={'role':"Director"},pluck='name')
    if director_mail:
        director_mail_id = director_mail[0]
        data={}
        data["director_mail"]=director_mail_id
        data["leave_policy"]=doc.title
        data["current_status"]=doc.workflow_state
        data["name"]=doc.name
        send_mail_to_director(data)
    else :
        frappe.msgprint("Setup Director User ID")
def hr_mail(doc):
    hr_mail=frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
    if hr_mail:
        hr_mail_id = hr_mail[0]
        data ={}
        data["hr_mail"]=hr_mail_id
        data["leave_policy"]=doc.title
        data["current_status"]=doc.workflow_state
        data["name"]=doc.name
        send_mail_to_hr(data)
    else :
        frappe.msgprint("Setup HR Admin User ID")