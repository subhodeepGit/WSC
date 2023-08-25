# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import send_clearance_notification_to_department,send_pendingDues_notification_to_student
class StudentClearanceApplication(Document):
    def on_submit(self):
        if not self.get("departments_clearance_status"):
            frappe.throw("Department Clearance is not present")

        for t in self.get("departments_clearance_status"):
            if(t.clearance_status == 'Select'):
                frappe.throw(("Provide action in clearance status"))

        if self.status != "Clearance Approved":
            frappe.throw(("Document cannot be submitted. Status must be 'Clearance Approved'."))
    
    def before_save(self):
        if self.is_new():
            self.sendEmailToDepartment()
        if self.total_dues>0:
            self.sendDuesEmailToStudent()

    def validate(self):
        self.validateApprovedorPending()
        self.validateAmount()

    def sendDuesEmailToStudent(self):
        send_pendingDues_notification_to_student(self)

    def sendEmailToDepartment(self):
        if len(self.departments_clearance_status)>0:
            send_clearance_notification_to_department(self)

    def validateAmount(self):
        for t in self.get("departments_clearance_status"):
            if(t.clearance_status == 'Dues' and t.amount <= 0):
                    frappe.throw(("Dues amount should be greater than Zero"))
       
    def validateApprovedorPending(self):
        flag=len(self.get("departments_clearance_status"))
        for t in self.get("departments_clearance_status"):
            if(t.clearance_status == 'No-Dues'):
                flag -= 1
        if flag == 0:
            self.status = "Clearance Approved"
        else:
            self.status = "Clearance Pending"

@frappe.whitelist()
def current_student_detail(student_id):
    clearanceDepartment=[]
    current_education_data=frappe.get_all("Current Educational Details",{"parent":student_id},['programs','semesters','academic_year','academic_term'])
    if not current_education_data:
        frappe.throw("Education Details not found")
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
            fields=['department','department_email_id']
         )
    if len(clearanceDepartment)==0:
        frappe.throw("Clearance Master is not created for this Academic Term or Academic Year")
    return {
        "current_education_data": current_education_data or None,
        "user_disable_date": userDisableDate or "",
        "department_clearance":clearanceDepartment or None
    }

@frappe.whitelist()
def get_attrition_student_id(attrition_id):
    current_student_attrition_data=frappe.db.sql("""Select student_no,student_name,student_email_address from `tabStudent Attrition Form` where name = %s""",attrition_id)
    if not current_student_attrition_data:
        return None

    return {
        "current_student_attrition_data": current_student_attrition_data,
    }

@frappe.whitelist()
def is_student(user):
    roles=frappe.get_roles(user)
    if 'Student' in roles:
        return {"is_student": True}
    else:
        return {"is_student": False}


    