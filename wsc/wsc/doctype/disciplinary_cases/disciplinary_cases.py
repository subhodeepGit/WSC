# Copyright (c) 2023, SOUL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Disciplinarycases(Document):
    def validate(self):
        if self.employee == self.raised_by:
            frappe.throw("Employee must be unique in both <b>Employee</b> and <b>Raised By</b>")
        act=frappe.get_all("Employee",{"name":self.employee},["action"])
        if act[0]["action"] == "Termination":
            frappe.throw("This Employee is already terminated")
        for t in self.get("discipline_committee"):
            if self.employee == t.committee_member:
                frappe.throw("Member sould not same with Disciplinary Cases Employee")
            if self.raised_by == t.committee_member:
                frappe.throw("Member sould not same with Raised By Employee")
        duplicate_row_validation(self, "discipline_committee",['committee_member'])
    
    def on_update_after_submit(self):
        duplicate_row_validation(self, "discipline_committee",['committee_member'])
    
    def on_submit(self):
        self.db_set("complaint_status","Complaint Files")

    def on_change(self):
        employee_update(self)
        termination_emp(self)
        for t in self.get("discipline_committee"):
            if self.employee == t.committee_member:
                frappe.throw("Member sould not same with Disciplinary Cases Employee")
            if self.raised_by == t.committee_member:
                frappe.throw("Member sould not same with Raised By Employee")

# def update_field(self):
#     if self.complaint_status=="":
#         frappe.throw("You cannot able to select Blank data in Complaint Status")
#     if self.complaint_status=="Action Taken":
#         frappe.db.set_value("Employee",self.employee,"disciplinary_action",self.disciplinary_action)
#         frappe.db.set_value("Employee",self.employee,"complaint_status",self.complaint_status)
#         frappe.db.set_value("Employee",self.employee,"complaint",self.complaint)
#         frappe.db.set_value("Employee",self.employee,"action",self.action)
#         frappe.db.set_value("Employee",self.employee,"action_description",self.action_description)
#     if self.complaint_status=="Complaint Files":
#         frappe.db.set_value("Employee",self.employee,"disciplinary_action","")
#         frappe.db.set_value("Employee",self.employee,"complaint_status",self.complaint_status)
#         frappe.db.set_value("Employee",self.employee,"complaint",self.complaint)
#         frappe.db.set_value("Employee",self.employee,"action","")
#         frappe.db.set_value("Employee",self.employee,"action_description","")
#     if self.complaint_status=="Resolved":
#         frappe.db.set_value("Employee",self.employee,"disciplinary_action","")
#         frappe.db.set_value("Employee",self.employee,"complaint_status",self.complaint_status)
#         frappe.db.set_value("Employee",self.employee,"complaint",self.complaint)
#         frappe.db.set_value("Employee",self.employee,"action","")
#         frappe.db.set_value("Employee",self.employee,"action_description","")

    
def duplicate_row_validation(doc,table_field_name,comapre_fields):
    row_names=[]
    for row in doc.get(table_field_name):
        row_names.append(row.name)

    for row in doc.get(table_field_name):
        filters={"parent":row.parent,"idx":("!=",row.idx)}
        for field in comapre_fields:
            filters[field]=row.get(field)
        for duplicate in frappe.get_all(row.doctype,filters,['idx','name']):
            if duplicate.name in row_names:
                frappe.throw("#Row {0} Duplicate values in <b>Discipline Committee</b> Not Allowed".format(duplicate.idx))

def termination_emp(self):
    if self.complaint_status=="Action Taken":
        if self.action=="Termination":
            emp=frappe.db.get_all("User", {'email':self.employee_email},['name','enabled'])
            if emp[0]["enabled"]==1:
                update_doc = frappe.get_doc("User",emp[0]["name"])
                update_doc.enabled=0
                update_doc.save()
            if emp[0]["enabled"]==0:
                pass
        else:
            emp=frappe.db.get_all("User", {'email':self.employee_email},['name','enabled'])
            if emp[0]["enabled"]==1:
                pass
            if emp[0]["enabled"]==0:
                update_doc = frappe.get_doc("User",emp[0]["name"])
                update_doc.enabled=1
                update_doc.save()

def employee_update(self):
    if self.complaint_status=="Complaint Files":
        pass
    elif self.complaint_status=="Action Taken":
        ref_party_doc=frappe.get_doc('Employee', self.employee)
        ref_party_doc.append("disciplinary_action",{
            "date":self.date,
            "disciplinary_cases":self.disciplinary_cases,
            "raised_by":self.raised_by,
            "disciplinary_action":self.disciplinary_action,
            "complaint_status":self.complaint_status,
            "complaint":self.complaint,
            "action":self.action,
            "action_description":self.action_description,
        })
        ref_party_doc.save()
    elif self.complaint_status=="Resolved":
        ref_party_doc=frappe.get_doc('Employee', self.employee)
        ref_party_doc.append("disciplinary_action",{
            "date":self.date,
            "disciplinary_cases":self.disciplinary_cases,
            "raised_by":self.raised_by,
            "disciplinary_action":"",
            "complaint_status":self.complaint_status,
            "complaint":self.complaint,
            "action":"",
            "action_description":"",
        })
        ref_party_doc.save()