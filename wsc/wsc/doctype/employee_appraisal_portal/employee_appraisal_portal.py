# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import notify_level_app,notify_employee_app,sendHR_app
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from datetime import datetime

class EmployeeAppraisalPortal(Document):
    def validate(self):
        get_dimenssions(self)
        if self.workflow_state == "Pending Approval from Reporting Authority":
            self.send_mail_ra()
        if self.workflow_state == "Pending Approval from Department Head":
            #code needs to be added 
            self.send_mail_dh()
        if self.workflow_state == "Pending Approval from Director Admin" :
            self.send_mail_director()
        if self.workflow_state == "Approved" or self.workflow_state=="Rejected":
            self.send_mail_hr()
        # self.validate_date(self.ros_review_meeting_date, "ROS Review Meeting")
        # self.validate_date(self.department_head_review_meeting_date, "Department Head Review Meeting")
        # self.validate_date(self.director_review_meeting_date, "Director Review Meeting")

        #cHECKING Duplicate records
        duplicate_records = self.check_duplicate_records()
        print(duplicate_records)

        if duplicate_records:
            frappe.throw("Employee has already applied for the same . Please review.")

        if self.workflow_state == "Submit" :
            self.send_notification("Level 2")

    def validate_date(self,date_field, field_name):
        if date_field:
            current_date = datetime.now().date()

            if isinstance(date_field, str):
                selected_date = datetime.strptime(date_field, '%Y-%m-%d').date()
            else:
                selected_date = date_field

            if selected_date > current_date:
                frappe.throw(f"{field_name} date cannot be greater than the current date.")

    def on_cancel(self):
        if self.workflow_state=="Rejected":
            frappe.db.set_value("Employee Appraisal Portal",self.name, "approval_status","Rejected")
        if self.workflow_state=="Rejected":
            self.send_employee()
            self.send_mail_hr()

    def on_update_after_submit(self):     
        if  self.workflow_state!="Submit" and self.workflow_state!="Draft" and self.workflow_state!="Rejected":
            workflow_list=frappe.get_all("Workflow Document State",{"parent":"Appraisal Workflow","state":self.workflow_state},['state','allow_edit'])
            leval_approval=workflow_list[0]['allow_edit']
            emp_workflow_list=frappe.get_all("Approver Details for Appraisal",{"parent":self.employee},
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
                frappe.db.set_value("Employee Appraisal Portal",self.name, "approval_status","Approved")
                self.send_mail_hr()
                self.send_employee()
            else:
                data=frappe.get_all("Employee",{"name":emp_no},["employee_name","designation"])
                designation=""
                if data[0]['designation']!="":
                    designation="(%s)"%(data[0]['designation'])
                text="Approved By %s %s"%(data[0]['employee_name'],designation)
                frappe.db.set_value("Employee Appraisal Portal",self.name, "approval_status",text)

                ####Notification function called###########

        # if self.workflow_state=="Rejected":
        #     frappe.db.set_value("Goal Setting",self.name, "approval_status","Rejected")
        if self.workflow_state == "Approved by Level 2":
            self.send_notification("Level 3")
        if self.workflow_state == "Approved by Level 3":
            self.send_notification("Level 4")
        if self.workflow_state=="Rejected":
            self.send_employee()
            self.send_mail_hr()

    def check_duplicate_records(self):
        # Fetch existing records excluding the current one
        existing_records = frappe.get_all('Employee Appraisal Portal',filters={"employee":self.employee,"appraisal_year":self.appraisal_year,"appraisal_cycle":self.appraisal_cycle,"docstatus":1,"status":"Approved"},fields=['name'])

        return existing_records

    def get_approver_list(self):
        if self.docstatus==1 :
            emp_approver_list = frappe.get_all("Approver Details for Appraisal",{"parent":self.employee},["employee","email_id","level_of_approval","employee_name","designation"])

            return emp_approver_list
        else :
            pass



    def set_user_permission(doc):
        if doc.reporting_authority:
                for emp in frappe.get_all("Employee", {'reporting_authority_email':doc.reporting_authority}, ['reporting_authority_email']):
                    if emp.get('reporting_authority_email'):
                        print(emp.get('reporting_authority_email'))
                        add_user_permission("Employee Appraisal Portal",doc.name, emp.get('reporting_authority_email'), doc)
                    else:
                        frappe.msgprint("Reporting Authority Not Found")

    ############Notification coding #################
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
            sendHR_app(data)
            

#Send to level of approver
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
                notify_level_app(emp_data)

    def send_employee(self):
        if self.email:
            data = {}
            data["name"]=self.name
            data["status"]=self.approval_status
            data["employee"]=self.employee
            data["email"]=self.email
            notify_employee_app(data)
        
        else :
            pass


@frappe.whitelist()
def get_appraisal_cycle(doctype, txt, searchfield, start, page_len, filters):
    data = frappe.get_all("Employee Appraisal Cycle",{"year":filters.get("appraisal_year"),"status":"Open"},["name"],as_list=1)
    return data
    

# @frappe.whitelist()
# def get_kras(appraisal_template):
#     data =frappe.get_all("KRA Rating",{'parent':appraisal_template},["kra"])
#     return data

@frappe.whitelist()
def get_goals(employee,appraisal_year):
    goal_setting = frappe.get_all("Goal Setting",{"employee":employee,"year":appraisal_year,"approval_status":"Approved"},["name"])

    if len(goal_setting)>0:
        if goal_setting[0].name :
            document = goal_setting[0].name
            data =frappe.get_all("Goals",{'parent':document},["goal","category","due_date"])
            print(data)
            return data

def get_dimenssions(self):
    if len(self.self_rating) == 0:
        for data in frappe.get_all("Dimenssions for Appraisal",{"is_active":1},["name","description"]):
            self.append("self_rating",{
                "dimenssion":data.name,
                "description":data.description
            })
    
@frappe.whitelist()
def get_mid_year_grade(employee,appraisal_year):
    frappe.msgprint("Triggered")
    for data in frappe.get_all("Employee Appraisal Portal",{"employee":employee,"appraisal_year":appraisal_year,"appraisal_round":'Mid Year'},["final_grade"]):
        print(data)
        print("\n\n\n")
        if len(data)>0 :
            return data[0]
        else :
            return " "