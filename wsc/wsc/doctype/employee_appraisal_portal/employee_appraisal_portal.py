# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import sendHR_appraisal,sendRa_appraisal,sendDh_appraisal,sendDirector_appraisal
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from datetime import datetime

class EmployeeAppraisalPortal(Document):
    def validate(self):
        if self.workflow_state == "Pending Approval from Reporting Authority":
            self.send_mail_ra()
        if self.workflow_state == "Pending Approval from Department Head":
            #code needs to be added 
            self.send_mail_dh()
        if self.workflow_state == "Pending Approval from Director Admin" :
            self.send_mail_director()
        if self.workflow_state == "Approved" or self.workflow_state=="Rejected":
            self.send_mail_hr()
        self.validate_date(self.ros_review_meeting_date, "ROS Review Meeting")
        self.validate_date(self.department_head_review_meeting_date, "Department Head Review Meeting")
        self.validate_date(self.director_review_meeting_date, "Director Review Meeting")

        #cHECKING Duplicate records
        duplicate_records = self.check_duplicate_records()
        print(duplicate_records)

        if duplicate_records:
            frappe.throw("Employee has already applied for the same . Please review.")
        
    def validate_date(self,date_field, field_name):
        if date_field:
            current_date = datetime.now().date()

            if isinstance(date_field, str):
                selected_date = datetime.strptime(date_field, '%Y-%m-%d').date()
            else:
                selected_date = date_field

            if selected_date > current_date:
                frappe.throw(f"{field_name} date cannot be greater than the current date.")

    def check_duplicate_records(self):
        # Fetch existing records excluding the current one
        existing_records = frappe.get_all('Employee Appraisal Portal',filters={"employee":self.employee,"appraisal_year":self.appraisal_year,"appraisal_cycle":self.appraisal_cycle,"docstatus":1},fields=['name'])

        return existing_records


    #send mail to HR
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
            data["appraisal_cycle"]=self.appraisal_cycle
            sendHR_appraisal(data)
        
    # #send mail to employee
    # def send_employee(self):
    # 	employee_user_id = frappe.get_all("Employee",filters={"name":self.employee},pluck="user_id")
    # 	if len(employee_user_id)>0:
    # 		user_id = employee_user_id[0]
    # 		data = {}
    # 		data["employee_mail"]=user_id
    # 		data["employee_name"]=self.employee_name
    # 		data["current_status"]=self.workflow_state
    # 		data["name"]=self.name
    # 		# sendEmployee(data)
        
    #Send mail to Department Head
    def send_mail_dh(self):
        #take the department of the employee , find the user id of that particular department head
        department = self.department
        department_head = frappe.get_all("Department",filters = {"name":department},pluck="department_head")
        print("\n\n\n\nDepartment Head")
        print(department_head)
        print(type(department_head[0]))
        # if department_head == [None]:
        # 	print("Hello")
        if department_head==[None]:
            frappe.throw("Department Head Mail Not found")
            

        else :
            dh_id = department_head[0]
            data = {}
            data["dh_mail"]=dh_id
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["name"]=self.name
            data["appraisal_cycle"]=self.appraisal_cycle
            # sendDh(data)
            sendDh_appraisal(data)

        

    #Send Mail to Director
    def send_mail_director(self):
        director_mail = frappe.get_all("User",filters={"role":"Director"},pluck='name')
        # print("\n\n\n")
        # print(director_mail)
        if director_mail==[None]:
            frappe.throw("Director Mail not found")
            

        else :
            director_mail_id = director_mail[0]
            data={}
            data["director_mail"]=director_mail_id
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["name"]=self.name
            data["appraisal_cycle"]=self.appraisal_cycle
            # sendDirector(data)
            sendDirector_appraisal(data)

    #send mail to reporting authority
    def send_mail_ra(self):
        ra_mail = self.reporting_authority
        if ra_mail:
            data={}
            data["ra_mail"]=ra_mail
            data["employee_name"]=self.employee_name
            data["current_status"]=self.workflow_state
            data["name"]=self.name
            data["appraisal_cycle"]=self.appraisal_cycle
            # sendRa(data)
            sendRa_appraisal(data)
        else :
            frappe.throw("Reporting Authority mail not found")

    def set_user_permission(doc):
        if doc.reporting_authority:
                for emp in frappe.get_all("Employee", {'reporting_authority_email':doc.reporting_authority}, ['reporting_authority_email']):
                    if emp.get('reporting_authority_email'):
                        print(emp.get('reporting_authority_email'))
                        add_user_permission("Employee Appraisal Portal",doc.name, emp.get('reporting_authority_email'), doc)
                    else:
                        frappe.msgprint("Reporting Authority Not Found")


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
    goal_setting = frappe.get_all("Goal Setting",{"employee":employee,"year":appraisal_year,"status":"Approved"},["name"])

    if len(goal_setting)>0:
        if goal_setting[0].name :
            document = goal_setting[0].name
            data =frappe.get_all("Goals",{'parent':document},["goal","category","due_date"])
            print(data)
            return data
@frappe.whitelist()
def get_dimenssions():
    data = frappe.get_all("Dimenssions for Appraisal",{"is_active":1},["name","description"])
    if data :
        return data
    else :
        pass
@frappe.whitelist()
def get_mid_year_grade(employee,appraisal_year):
    data = frappe.get_all("Employee Appraisal Portal",{"employee":employee,"appraisal_year":appraisal_year,"appraisal_round":'Mid Year'},["final_grade"])
    print(data)
    if data :
        return data[0]
    else :
        pass