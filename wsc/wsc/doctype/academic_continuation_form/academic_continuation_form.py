# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.doctype.student_exchange_applicant.student_exchange_applicant import get_academic_calender_table
from wsc.wsc.doctype.semesters.semesters import get_courses

class AcademicContinuationForm(Document):

    def on_submit(self):
        frappe.db.set_value("Student",self.student,"enabled",1) #After submission the student will be enabled again.
        data = frappe.get_all("Program Intermit Form",{"student":self.student},["name"]) #fetching the doc name where the student value is Self.student
        if len(data)== 0 : 
            pass
        else :
            frappe.set_value("Program Intermit Form",data[0]["name"],"enabled",0) #if the data exits , then i will set the enable value to 0


@frappe.whitelist()
def get_student_value(doctype, txt, searchfield, start, page_len, filters):

    # frappe.throw(data[0])
    return data

@frappe.whitelist()
def get_student_previous_records(student):
    data = frappe.get_all("Current Educational Details",{"parent":student},["academic_year","academic_term","programs","semesters"])
    if len(data)==0:
        pass
    else:
        return data[0] 
@frappe.whitelist()
def enroll_student(source_name):

    st_name = frappe.get_all("Academic Continuation Form",{'name':source_name},["student","academic_term","academic_year","programs","semester","program_grade"])

    studentname=st_name[0]["student"]
    student_details = frappe.get_all("Student",{"name":studentname},['name','student_category','student_name','roll_no','gender'])
    program_enrollment = frappe.new_doc("Program Enrollment")
    program_enrollment.student = studentname
    program_enrollment.student_category = student_details[0].student_category
    program_enrollment.student_name = student_details[0].student_name
    program_enrollment.roll_no = student_details[0].roll_no
    program_enrollment.programs = st_name[0].programs
    program_enrollment.program = st_name[0].semester
    program_enrollment.academic_year=st_name[0].academic_year
    program_enrollment.academic_term=st_name[0].academic_term
    program_enrollment.reference_doctype="Academic Continuation Form"
    program_enrollment.reference_name=source_name
    program_enrollment.program_grade = st_name[0].program_grade
    program_enrollment.gender=student_details[0].gender
       
    return program_enrollment

@frappe.whitelist()
def get_data(student):
    data = frappe.get_all("Student",{"name":student},["name","student_name","student_category"])
    return data