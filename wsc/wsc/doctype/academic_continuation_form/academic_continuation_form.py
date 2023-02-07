# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AcademicContinuationForm(Document):

    def on_submit(self):
        # update_user(doc)
        # data = frappe.get_all("Academic Continuation Form",{"form_status":"Approve"},["student"])
        print("\n\n\n\n\nPrinting data")      #[{'student': 'EDU-STU-2023-00007'}]
        # student = data[0]["student"]
        print(self.student)
        frappe.db.set_value("Student",self.student,"enabled",1)
        data = frappe.get_all("Program Intermit Form",{"student":self.student},["name"])
        if len(data)== 0 :
            pass
        else :
            frappe.set_value("Program Intermit Form",data[0]["name"],"enabled",0)


@frappe.whitelist()
def get_student_value(doctype, txt, searchfield, start, page_len, filters):
    data = frappe.get_all("Student",{"enabled":0},["name","student_name","roll_no"],as_list=1)
    print("\n\n\n\nDisabled Student")
    print(data)
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
    print("\n\n\nIm on Enroll Student")
    from wsc.wsc.doctype.student_exchange_applicant.student_exchange_applicant import get_academic_calender_table
    from wsc.wsc.doctype.semesters.semesters import get_courses
    print("\n\n\n\nSource Name")
    print(source_name)
    # doc_name= frappe.get_doc("Academic Continuation Form",source_name)
    # doc_name= str(doc_name)
    
    # doc_name = doc_name[25:-1]
    # print("\n\n\n\n\n")
    # print(doc_name)
    st_name = frappe.get_all("Academic Continuation Form",{'name':source_name},["student","academic_term","academic_year","programs","semester","program_grade"])
    # st_name =st_name[0]["student"]
    # print("\n\n\n")
    # print(st_name)
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
        # program_enrollment.physically_disabled=st_applicant.physically_disabled
        # program_enrollment.award_winner=st_applicant.award_winner
        # program_enrollment.boarding_student=st_applicant.hostel_required

    
    # print("\n\n\n\n\nStudent Id")
    # print(student_id)
    # print("\n\n\n\n\nEnrolled Student")
    # print(data)


    # if st_applicant.program:
    #     for crs in get_courses(st_applicant.program):
    #         program_enrollment.append("courses",crs)
    # if st_applicant.student_admission:
    #     st_admission=frappe.get_doc("Student Admission",st_applicant.student_admission)
    #     if st_admission.admission_fees=="YES":
    #         for fs in st_admission.get("admission_fee_structure"):
    #             if fs.student_category==student.student_category:
    #                 program_enrollment.append("fee_structure_item",{
    #                     "student_category":student.student_category,
    #                     "fee_structure":fs.fee_structure,
    #                     "amount":fs.amount,
    #                     "due_date":fs.due_date
    #                 })
                
    #     if st_admission.academic_calendar:
    #         for d in get_academic_calender_table(st_admission.academic_calendar):
    #             program_enrollment.append("academic_events_table",d)
    return program_enrollment

@frappe.whitelist()
def get_data(student):
    data = frappe.get_all("Student",{"name":student},["name","student_name","student_category"])
    print("\n\n\n\n\n\nData")
    return data