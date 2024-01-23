# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import notify_level,sendHR_goal,notify_employee_goal

class GoalSetting(Document):
    def validate(self):

        duplicate_records = self.check_duplicate_records()
        # print("\n\n\n\n\n\n")
        # # print(self.status)
        # print("\n\n\n\n")
        if duplicate_records:
            frappe.throw("Duplicate records found for the same details. Please review.")
        
        if self.is_new():
            self.approval_status="Draft"    
        if self.workflow_state == "Submit" :
            self.send_notification("Level 2")

    def on_cancel(self):
        if self.workflow_state=="Rejected":
            frappe.db.set_value("Goal Setting",self.name, "approval_status","Rejected")

    def on_update(self):
        if self.workflow_state=="Submit":
            frappe.db.set_value("Goal Setting",self.name, "approval_status","Submit")
        

    def on_update_after_submit(self):     
        if  self.workflow_state!="Submit" and self.workflow_state!="Draft" and self.workflow_state!="Rejected":
            workflow_list=frappe.get_all("Workflow Document State",{"parent":"Workflow for Goal Setting","state":self.workflow_state},['state','allow_edit'])
            leval_approval=workflow_list[0]['allow_edit']
            emp_workflow_list=frappe.get_all("Dynamnic Workflow for Goal Setting",{"parent":self.employee},
                                             ["level_of_approval","employee"],order_by="level_of_approval asc")
            flag="Yes"
            emp_no=''
            for t in emp_workflow_list:
                if t['level_of_approval']==leval_approval:
                    flag="No"
                    emp_no=t['employee']
                else:
                    flag="Yes"
            if flag=="No":
                frappe.db.set_value("Goal Setting",self.name, "approval_status","Approved")
                self.send_mail_hr()
                self.send_employee()
            else:
                data=frappe.get_all("Employee",{"name":emp_no},["employee_name","designation"])
                designation=""
                if data[0]['designation']!="":
                    designation="(%s)"%(data[0]['designation'])
                text="Approved By %s %s"%(data[0]['employee_name'],designation)
                frappe.db.set_value("Goal Setting",self.name, "approval_status",text)

        #################Notification Code ###########################
                
        if self.workflow_state=="Rejected":
            frappe.db.set_value("Goal Setting",self.name, "approval_status","Rejected")
        if self.workflow_state == "Approved by Level 2":
            self.send_notification("Level 3")
        if self.workflow_state == "Approved by Level 3":
            self.send_notification("Level 4")
        if self.workflow_state=="Rejected":
            self.send_employee()
            self.send_mail_hr()


    def check_duplicate_records(self):
        # Fetch existing records excluding the current one
        existing_records = frappe.get_all('Goal Setting',filters={"employee":self.employee,"year":self.year,"department":self.department,"docstatus":1,"approval_status":"Approved"},fields=['name'])

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
            data["current_status"]=self.approval_status
            data["name"]=self.name
            sendHR_goal(data)

    def get_approver_list(self):
        if self.docstatus==1 :
            emp_approver_list = frappe.get_all("Dynamnic Workflow for Goal Setting",{"parent":self.employee},["employee","email_id","level_of_approval","employee_name","designation"])

            return emp_approver_list
        else :
            pass

    def send_notification(self,approval_level):
        data = self.get_approver_list()
        if data is None:
            pass
        else:
            emp_data = {}
            for item in data:
                if item.level_of_approval == approval_level:
                    emp_data["name"] = self.name
                    emp_data["status"] = self.approval_status
                    emp_data["employee"] = self.employee
                    emp_data["email"] = item.email_id
                    break
            if emp_data:
                notify_level(emp_data)


    def send_employee(self):
        if self.email:
            data = {}
            data["name"]=self.name
            data["status"]=self.approval_status
            data["employee"]=self.employee
            data["email"]=self.email
            notify_employee_goal(data)
            #call the function of custome_notification file and pass the data agrument
        
        else :
            pass
