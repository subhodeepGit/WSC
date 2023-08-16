# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import employee_reporting_aprover,employee_hr
import datetime
from typing import Dict, Optional, Tuple, Union

import frappe
from frappe import _
from frappe.query_builder.functions import Max, Min, Sum

from frappe.model.document import Document
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
import re
class EmployeeProfileUpdation(Document):
    def approver_mail(self):
        data={}
        data["reporting_authority_email"]=self.reporting_auth_id
        data["employee_name"]=self.employee_name
        data["current_status"]=self.workflow_state
        data["name"]=self.name
        data["hr_email"]=self.hr_id
        employee_reporting_aprover(data)
        
    def after_insert(self):
        print("\n\n\n")
        print("Hello Profile")
        self.set_shift_request_permission_reporting_authority()	
        
    def validate(self):
        self.check_email_format()
        self.validate_mobile_number()
        if self.workflow_state == "Draft":
            self.approver_mail()
        if self.workflow_state=="Pending Approval From HR":
            self.send_to_hr()
    
    def send_to_hr(self):
        data = {}
        data["hr_email"] = self.hr_id
        data["employee_name"]=self.employee_name
        data["current_status"]=self.workflow_state
        data["name"]=self.name
        employee_hr(data)
        
    def on_submit(self):
        print("\n\n\n")
        print("Profile Updation")
        employee = frappe.get_doc("Employee", self.employee)
        employee.education = []
        for row in self.education:
            child_row = employee.append("education", {})
            child_row.school_univ = row.school_univ
            child_row.qualification = row.qualification
            child_row.level=row.level
            child_row.year_of_passing=row.year_of_passing
            child_row.class_per= row.class_per
        
        employee.family_background_details = []
        for row in self.family:
            child_row = employee.append("family_background_details", {})
            child_row.name1 = row.name1
            child_row.relation = row.relation
            child_row.occupation=row.gender
            child_row.contact=row.contact
            
        employee.current_address=self.current_address
        employee.permanent_address=self.permanent_address
        employee.cell_number=self.mobile
        employee.person_to_be_contacted=self.emergency_contact_name
        employee.emergency_phone_number=self.emergency_contact
        employee.relation=self.relation
        employee.personal_email=self.personal_email
        employee.employee_name = self.employee_name
        employee.gender = self.gender
        employee.date_of_birth = self.date_of_birth
        employee.user_id = self.user_id
        employee.department = self.department
        employee.employee_number = self.employee_number
        employee.designation = self.designation
        employee.branch = self.branch
        employee.employment_type = self.employment_type
        employee.blood_group = self.blood_group
        employee.save()

        my_profile = frappe.get_doc("My Profile",self.employee)
        my_profile.employee_name = self.employee_name
        my_profile.gender = self.gender
        my_profile.date_of_birth = self.date_of_birth
        my_profile.user_id = self.user_id
        my_profile.department = self.department
        my_profile.employee_number = self.employee_number
        my_profile.designation = self.designation
        my_profile.branch = self.branch
        my_profile.mobile = self.mobile
        my_profile.personal_email = self.personal_email
        my_profile.company_email = self.company_email
        my_profile.current_address = self.current_address
        my_profile.permanent_address = self.permanent_address
        my_profile.emergency_contact_name = self.emergency_contact_name
        my_profile.emergency_contact = self.emergency_contact
        my_profile.blood_group = self.blood_group
        my_profile.employment_type  = self.employment_type
        my_profile.save()
        frappe.msgprint("Employee profile updated successfully.")


    def set_shift_request_permission_reporting_authority(doc):
        for emp in frappe.get_all("Employee", {'reporting_authority_email':doc.reporting_auth_id}, ['reporting_authority_email']):
            if emp.get('reporting_authority_email'):
                print(emp.get('reporting_authority_email'))
                add_user_permission("Employee Profile Updation",doc.name, emp.get('reporting_authority_email'), doc)
            else:
                frappe.throw("Reporting Authority Not Found")	
        
    def check_email_format(self):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        company_email = self.company_email
        personal_email = self.personal_email

    
        if re.match(email_pattern, company_email) and re.match(email_pattern,personal_email):
            pass
        else:
            frappe.throw("Invalid Email format")
    def validate_mobile_number(self):
        mobile_number = self.mobile
        if mobile_number:
            if len(mobile_number)>10 or len(mobile_number)<10 :
                frappe.throw("Mobile Number should not be less or greater than 10")
            if not mobile_number.isdigit():
                frappe.throw("Mobile Number should contain only digits")
            else :
                pass
#populate Reporting Authority 
@frappe.whitelist()
def get_employee_details(employee):
    data =frappe.get_all("Employee",{'name':employee},["employee_name","department","branch","designation","employee_number","reports_to","reporting_authority_email","gender","date_of_birth","user_id","blood_group","employment_type"])
    if data != None  or data != ['']:
        print(data[0])
        return data[0]
    else :
        pass


#Populate HR Admin
@frappe.whitelist()
def get_hr_mail():
    hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
    if hr_mail:
        hr_mail_id = hr_mail[0]
        return hr_mail_id


#popuate Education Details 
@frappe.whitelist()
def get_education(employee):
    data = frappe.get_all("Employee Education",{"parent":employee},["school_univ","qualification","level","year_of_passing","class_per"])
    if data :
        # print("\n\n\n\n\n",data)
        return data

#populate family details
@frappe.whitelist()
def get_family_background(employee):

    data = frappe.get_all("Family Background Details",{"parent":employee},["name1","relation","occupation","gender","contact"])
    if data :
        # print("\n\n\n\n\n",data)
        return data
    
#get Address and Contact Details
@frappe.whitelist()
def addr_contact(employee):
    data = frappe.get_all("Employee",{"name":employee},["current_address","permanent_address","cell_number","person_to_be_contacted","emergency_phone_number","relation","personal_email"])
    if data :
        # print("\n\n\n\n\n",data)
        return data[0]

@frappe.whitelist()
def is_verified_user(docname):
    # if frappe.db.exists(docname):

    doc = frappe.get_doc("Employee Profile Updation",docname)
    # emp_user_id = frappe.get_all("Employee",{"name":doc.employee},["user_id"])
    # if emp_user_id:
    # 	employee_user_id = emp_user_id[0]["user_id"]
    reporting_auth_id = doc.reporting_auth_id
    roles = frappe.get_roles(frappe.session.user)

    if "HR Admin" in roles or "Department Head" in roles or "HR Manager/CS Officer" in roles or "Administrator" in roles or "Admin" in roles:
        return True
    if doc.workflow_state == "Draft" and frappe.session.user ==reporting_auth_id :
        return True
    else :
        return False

