# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import notify_level,notify_employee_d


class DynamicWorkflow(Document):


    def get_approver_list(self):
        if self.docstatus==1 :
            emp_approver_list = frappe.get_all("Approvers",{"parent":self.employee},["employee","email_id","role","employee_name","designation","user_id"])

            return emp_approver_list
        else :
            pass
    
    # def on_change(self):
    #     data = self.get_approver_list()
    #     if data==None:
    #         pass
    #     else :
    #         for item in data:
    #             if self.document_status=="Pending" and self.docstatus==1 and item.role=="Level 1":
    #                 self.send_level1()
    #             if item.role=="Level 1":
    #                 if self.document_status=="Approved by "+ item.employee_name+"("+item.designation+")":
    #                     self.send_level2()
    #                 if self.document_status=="Rejected by "+ item.employee_name+"("+item.designation+")":
    #                     self.send_employee()
    #             if item.role=="Level 2":
    #                 if self.document_status=="Approved by "+ item.employee_name+"("+item.designation+")":
    #                     self.send_level3()
    #                 if self.document_status=="Rejected by "+ item.employee_name+"("+item.designation+")":
    #                     self.send_employee()
    #             if item.role=="Level 3":
    #                 if self.document_status=="Approved by "+ item.employee_name+"("+item.designation+")":
    #                     self.send_level4()
    #                 if self.document_status=="Rejected by "+ item.employee_name+"("+item.designation+")":
    #                     self.send_employee()
    #             if item.role=="Level 4":
    #                 if self.document_status=="Approved by "+ item.employee_name+"("+item.designation+")" or self.document_status=="Rejected by "+ item.employee_name+"("+item.designation+")":
    #                     self.send_employee()
    #             if self.document_status=="Approved":
    #                 self.send_employee()
    #                 break
    #             if self.document_status=="Rejected":
    #                 self.send_employee()
    #                 break

    # def send_level1(self):
    #     data = self.get_approver_list()
    #     if data==None:
    #         frappe.throw("No Approvers found")
    #     else :
    #         emp_data = {}

    #         for item in data :
    #             if item.role=="Level 1":
    #                 emp_data["name"]=self.name
    #                 emp_data["status"]=self.document_status
    #                 emp_data["employee"]=self.employee
    #                 emp_data["email"]=item.email_id
    #                 break
    #         if emp_data=={}:
    #             pass
    #         else :
    #             notify_level1(emp_data)
    
    # def send_level2(self):
    #     data = self.get_approver_list()
    #     if data==None:
    #         frappe.throw("No Approvers found")
    #     else :
    #         emp_data={}
    #         for item in data :
    #             if item.role=="Level 2":
    #                 emp_data["name"]=self.name
    #                 emp_data["status"]=self.document_status
    #                 emp_data["employee"]=self.employee
    #                 emp_data["email"]=item.email_id
    #                 break
    #         if emp_data=={}:
    #             pass
    #         else :
    #             notify_level2(emp_data)
                
    
    # def send_level3(self):
    #     data = self.get_approver_list()
    #     if data==None:
    #         frappe.throw("No Approvers found")
    #     else :
    #         emp_data={}

    #         for item in data :
    #             if item.role=="Level 3":
    #                 emp_data["name"]=self.name
    #                 emp_data["status"]=self.document_status
    #                 emp_data["employee"]=self.employee
    #                 emp_data["email"]=item.email_id
    #                 break
    #         if emp_data=={}:
    #             pass
    #         else:
    #             notify_level3(emp_data)

    # def send_level4(self):
    #     data = self.get_approver_list()
    #     if data==None:
    #         frappe.throw("No Approvers found")
    #     else :
    #         emp_data={}
    #         for item in data :
    #             if item.role=="Level 4":
    #                 emp_data = {}
    #                 emp_data["name"]=self.name
    #                 emp_data["status"]=self.document_status
    #                 emp_data["employee"]=self.employee
    #                 emp_data["email"]=item.email_id
    #                 break
    #         if emp_data=={}:
    #             pass
    #         else :
    #             notify_level4(emp_data)
        
    def on_change(self):
        data = self.get_approver_list()
        if data is None:
            pass
        else:
            for item in data:
                if self.document_status == "Pending" and self.docstatus == 1 and item.role == "Level 1":
                    self.send_notification(1, self.document_status)

                elif "Level" in item.role:
                    level = int(item.role.split(" ")[1])

                    if self.document_status == f"Approved by {item.employee_name}({item.designation})" :
                        next_level = level + 1
                        self.send_notification(next_level, self.document_status)

                    if self.document_status == f"Rejected by {item.employee_name}({item.designation})":
                        self.send_employee()

                    elif self.document_status == "Approved" or self.document_status == "Rejected":
                        self.send_employee()
                    # frappe.msgprint("Hello")

                        break

    def send_notification(self,level,status):
        data = self.get_approver_list()
        if data is None:
            pass
        else:
            emp_data = {}
            for item in data:
                if item.role == f"Level {level}":
                    emp_data["name"] = self.name
                    emp_data["status"] = status
                    emp_data["employee"] = self.employee
                    emp_data["email"] = item.email_id
                    break
            if emp_data:
                notify_level(emp_data)


    def send_employee(self):
        if self.employee_email:
            data = {}
            data["name"]=self.name
            data["status"]=self.document_status
            data["employee"]=self.employee
            data["email"]=self.employee_email
            notify_employee_d(data)
            #call the function of custome_notification file and pass the data agrument
        
        else :
            pass


@frappe.whitelist()
def get_approvers(employee):
    employee_details= frappe.get_all("Employee",{"employee":employee},["name"])

    if len(employee_details)>0:
        if employee_details[0].name :
            document = employee_details[0].name
            data =frappe.get_all("Approvers",{'parent':document},["employee","email_id","role","employee_name","designation","user_id"])
            # print("\n\n")
            # print(data)    
            return data
    

