# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import notify_hr,notify_director,notify_employee,notify_committee

class EmployeeSuggestion(Document):
    def notification_to_hr(self):
        data = {}
        hr = get_hr_mail()
        if hr != None:

            data["hr_email"] = hr
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["employee_suggestion"]=self.name
            data["name"]=self.name


            notify_hr(data)
        else :
            frappe.throw("HR Admin Email ID  Not Found")
    def notification_to_director(self):
        data = {}
        director = get_director_mail()
        if director != None :

            data["director_email"] = director
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["employee_suggestion"]=self.name
            data["name"]=self.name


            notify_director(data)
        else :
            frappe.throw("Director Email ID  Not Found")
    def notification_to_employee(self):
        data = {}
        employee_mail = self.user_id
        if employee_mail != None:

            data["employee_email"] = employee_mail
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["employee_suggestion"]=self.name
            data["name"]=self.name


            notify_employee(data)
        else :
            frappe.throw("Employee Email ID  Not Found")
    def validate(self):
        if self.user_id == None :
            frappe.msgprint("Employee User ID not found")
        if self.workflow_state == "Pending Approval From HR":
            self.notification_to_hr()
        if self.workflow_state=="Pending Approval From Committee":
            notify_committee(self)
        if self.workflow_state == "Pending Approval from Director Admin":
            self.notification_to_director()
        
        if self.workflow_state == "Approved" or self.workflow_state=="Rejected":
            self.notification_to_employee()

    # def on_cancel(self):
    #     suggestion = self.name
    #     if suggestion:
    #         # activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": onboarding_name}, fields=["name","activity_name"])
            
    #         # for activity_record in activity_records:
    #         #     # Step v: Update status field to the new status value
    #         #     # if activity_record.activity_name in doc.subject:
    #         #     # print(activity_record.activity_name)
    #         #     # print("\n\n\n")
    #         #     frappe.db.set_value("Employee Boarding Activity", activity_record.name, "status", "")

                
    #         #     # Step vi: Save changes to each On-boarding Activity document
    #         #     frappe.db.commit()
    #         #         # frappe.msgprint("Status updated in Employee Onboarding Activities")
    #         #     # else :
    #         #     #     pass
    #         frappe.db.set_value(self.doctype,self.name, "status", "Cancelled")
    #         frappe.db.commit()
    

#Getting HR Mail
@frappe.whitelist()
def get_hr_mail():
    hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
    if hr_mail :
        hr_mail_id = hr_mail[0]
        return hr_mail_id
    # else :
    # 	frappe.msgprint("Set HR Admin Mail ID")

#getting Director Mail
@frappe.whitelist()
def get_director_mail():
    director_mail = frappe.get_all("User",filters={'role':"Director"},pluck='name')
    if director_mail :
        director_mail_id = director_mail[0]
        return director_mail_id
    # else :
    # 	frappe.msgprint("Set Director Mail ID ")