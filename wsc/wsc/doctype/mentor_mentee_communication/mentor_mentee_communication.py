# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.doctype.user_permission import add_user_permission
from wsc.wsc.notification.custom_notification import mentor_mentee_communication_submit


class MentorMenteeCommunication(Document):
    @frappe.whitelist()
    def get_missing_fields(self):
        data={}
        data["programs"]=frappe.db.get_value("Current Educational Details",{"parent":self.student},"programs")
        data["mentor"]=frappe.db.get_value("Mentee List",{"student":self.student},"parent")
        data["mentor_name"]=frappe.db.get_value("Mentor Allocation",{"name":data["mentor"], 'docstatus':1},"mentor_name")
        return data

    def validate(doc):
        if not doc.get("__islocal"):
            set_user_permission(doc)
            mentor_mentee_communication_submit(doc)
    
    def on_trash(doc): 
        delete_permission(doc)
   
def set_user_permission(doc):
    for stu in frappe.get_all("Student",{"name":doc.student},['user']):
        add_user_permission("Mentor Mentee Communication",doc.name, stu.user, doc)
    for mentor in frappe.get_all("Mentor Allocation", {'name':doc.mentor}, ['mentor']):
        for emp in frappe.get_all("Employee", {'name':doc.mentor}, ['user_id']):
            add_user_permission("Mentor Mentee Communication",doc.name,emp.user_id,doc)

def delete_permission(doc):
    for d in frappe.get_all("User Permission",{"reference_doctype":doc.doctype,"reference_docname":doc.name}):
        frappe.delete_doc("User Permission",d.name)

@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
    for d in frappe.get_all("Mentor Allocation",{"name":filters.get("mentor")},["name"]):
        return frappe.get_all("Mentee List",{"parent":d.name},['student'],as_list=1)