# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import sendHR_goal,sendRa_goal,sendDh_goal,sendDirector_goal,sendEmployee_goal

class GoalSetting(Document):
    def validate(self):

        duplicate_records = self.check_duplicate_records()

        if duplicate_records:
            frappe.throw("Duplicate records found for the same details. Please review.")

        # if self.workflow_state == "Pending Approval from Reporting Authority":
        #     self.send_mail_ra()
        # if self.workflow_state == "Pending Approval from Department Head":
        #     #code needs to be added 
        #     self.send_mail_dh()
        # if self.workflow_state == "Pending Approval from Director Admin" :
        #     self.send_mail_director()
        # if self.workflow_state == "Approved" or self.workflow_state=="Rejected" or self.workflow_state == "Cancelled":
        #     self.send_mail_hr()
        #     sendEmployee_goal(self)
        

    def check_duplicate_records(self):
        # Fetch existing records excluding the current one
        existing_records = frappe.get_all('Goal Setting',filters={"employee":self.employee,"year":self.year,"department":self.department,"docstatus":1,"status":"Approved"},fields=['name'])

        return existing_records

    #Send mail to  HR
    def send_mail_hr(self):
        hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
        if hr_mail==[None]:
            frappe.throw("HR Admin mail id not found")
            

            # sendHR(data)
        else :
            hr_mail_id = hr_mail[0]
            data={}
            data["hr_mail"]=hr_mail_id
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["name"]=self.name
            sendHR_goal(data)

    #Send mail to Department Head
    def send_mail_dh(self):
        #take the department of the employee , find the user id of that particular department head
        department = self.department
        department_head = frappe.get_all("Department",filters = {"name":department},pluck="department_head")
        if department_head==[None]:
            frappe.throw("Department Head Mail Not found")
            

        else :
            dh_id = department_head[0]
            data = {}
            data["dh_mail"]=dh_id
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["name"]=self.name
            # sendDh(data)
            sendDh_goal(data)
    
    #Send Mail to Director
    def send_mail_director(self):
        director_mail = frappe.get_all("User",filters={"role":"Director"},pluck='name')
        if director_mail==[None]:
            frappe.throw("Director Mail not found")
        else :
            director_mail_id = director_mail[0]
            data={}
            data["director_mail"]=director_mail_id
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["name"]=self.name
            # sendDirector(data)
            sendDirector_goal(data)

    #send mail to reporting authority
    def send_mail_ra(self):
        ra_mail = self.reporting_authority
        if ra_mail:
            data={}
            data["ra_mail"]=ra_mail
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["name"]=self.name
            # sendRa(data)
            sendRa_goal(data)
        else :
            frappe.throw("Reporting Authority mail not found")
