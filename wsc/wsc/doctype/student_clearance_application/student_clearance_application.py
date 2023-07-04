# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class StudentClearanceApplication(Document):
    def validate(self):
        self.validateApprovedorPending()
        self.validateAmount()

    def validateAmount(self):
        for t in self.get("departments_clearance_status"):
            if(t.clearance_status=='Select'):
                frappe.throw(("Provide action in clearance status"))
            if(t.clearance_status=='Dues'):
                if(t.amount <= 0):
                    frappe.throw(("Dues amount should be greater than Zero"))
       
    def validateApprovedorPending(self):
        flag=len(self.get("departments_clearance_status"))
        for t in self.get("departments_clearance_status"):
            if(t.clearance_status=='No-Dues'):
                flag -= 1
    
        if flag ==0:
            self.status = "Clearance Approved"
        else:
            self.status = "Clearance Pending"

@frappe.whitelist()
def current_student_detail(student_id):
    clearanceDepartment=[]
    current_education_data=frappe.get_all("Current Educational Details",{"parent":student_id},['programs','semesters','academic_year','academic_term'])
    if not current_education_data:
        return None
    academicYear = current_education_data[0]['academic_year']
    academicTerm = current_education_data[0]['academic_term']
    userDisableDate = frappe.db.get_value(
        "Clearance Master",
        filters={"academic_year": academicYear,"academic_term": academicTerm},
        fieldname="user_disable_date"
    )
    clearanceData= frappe.db.get_all(
        "Clearance Master",
        filters={"academic_year": academicYear,"academic_term": academicTerm,"user_disable_date":userDisableDate},
        fields="name"
    )
    if clearanceData:
         clmFieldName=clearanceData[0]["name"]
         clearanceDepartment = frappe.get_all(
            "Clearance Departments",
            filters={"parent":clmFieldName },
            fields=["department"]
         )
    return {
        "current_education_data": current_education_data,
        "user_disable_date": userDisableDate or "",
        "department_clearance":clearanceDepartment or None
    }