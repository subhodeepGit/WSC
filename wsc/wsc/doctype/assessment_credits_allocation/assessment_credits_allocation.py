# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from wsc.wsc.utils import academic_term
from frappe.utils.csvutils import getlink
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions


class AssessmentCreditsAllocation(Document):
    def validate(self):
        self.validate_student()
        self.validate_assessment_criteria()
        self.validate_duplicate_record()
        academic_term(self)
        self.passing_marks_calculation()
        self.final_earned_marks_calculation_child()
        self.qualifying_status_child()
        self.validate_marks()
        self.validate_checker()

    def on_submit(self):
        self.create_permissions()

    def on_cancel(self):
        self.delete_permissions()

    def create_permissions(doc):
        for instr in frappe.get_all("Instructor",{"name":doc.checker},['department','name','employee']):
            for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id','department']):
                if emp.user_id:
                    add_user_permission(doc.doctype,doc.name,emp.user_id,doc)	
    
    def delete_permissions(doc):
        for usr in frappe.get_all("User Permission",{"allow":doc.doctype,"for_value":doc.name}):
            frappe.delete_doc("User Permission",usr.name)
        for usr in frappe.get_all("User Permission",{"reference_doctype":"Course Assessment","reference_docname":doc.name}):
            frappe.delete_doc("User Permission",usr.name)

    def validate_checker(self):
        for id in frappe.get_all("Instructor",{"email_id":frappe.session.user},['name','email_id']):
            if id.name==self.checker:
                pass
            else:
                if not self.module_exam_group:
                    frappe.throw("Enter the Module Exam Group Id")
                else:
                    frappe.throw("You do not have the permission to check the marks of the students for this module!!!")

    def qualifying_status_child(self):
        for t in self.get("final_credit_item"):
            if flt(t.final_earned_marks)<=t.passing_marks:
                t.qualifying_status="Fail"
            else:
                t.qualifying_status="Pass"


    def final_earned_marks_calculation_child(self):
        for t in self.get("final_credit_item"):
            earned_marks=flt(t.earned_marks)
            grace_marks=flt(t.grace_marks)
            t.final_earned_marks=grace_marks+earned_marks
            data=frappe.get_all("Course Assessment",{"name":t.course_assessment},['exam_declaration'])
            t.exam_declaration=data[0]['exam_declaration']

    def passing_marks_calculation(self):
        coures_code=self.course
        assessment_criteria=self.assessment_criteria	
        cdl_list=frappe.get_all("Credit distribution List",{"parent":coures_code,"assessment_criteria":assessment_criteria},['passing_marks'])
        if cdl_list:
            for t in self.get("final_credit_item"):
                if not t.passing_marks:
                    t.passing_marks=cdl_list[0]['passing_marks']
        else:
            frappe.throw("Passing marks not maintained for Assessment Criteria %s in Module Screen for the Module code %s"%(assessment_criteria,coures_code))
    
    def validate_duplicate_record(self):
        if self.student and self.course and self.assessment_criteria and self.academic_year and self.academic_term:
            for a in frappe.get_all('Assessment Credits Allocation', {'student':self.student, 'course':self.course,'assessment_criteria':self.assessment_criteria,'academic_year':self.academic_year, 'academic_term':self.academic_term, 'docstatus':('!=', 2)}):
                if a.name and a.name != self.name:
                    frappe.throw("The data is already exist in <b>{0}</b>".format(a.name))
    
    def validate_student(self):
        for st in frappe.get_all("Student",{"name":self.student},["enabled"]):
            if not st.enabled:
                frappe.throw("Student is not <b>Enabled</b>")

    def validate_assessment_criteria(self):
        lst = []
        # ,"status":("!=","Completed")
        for i in frappe.get_all("Course Enrollment",{'student':self.get("student"),"course":self.get("course")},['name']):
            fltr={"parent":i.get("name")}
            for j in frappe.get_all("Credit distribution List",fltr,["assessment_criteria"]):
                lst.append(j.assessment_criteria)
        if self.assessment_criteria not in lst:
            frappe.throw("Please Select the Assessment Criteria In Course <b>{0}</b>".format(self.get("course")))

    def validate_marks(self):
        for cr in self.get("final_credit_item"):
            addition=(flt(cr.earned_marks)+flt(cr.grace_marks))
            self.final_marks=addition
            self.grace_marks=flt(cr.grace_marks)
            self.passing_marks=flt(cr.passing_marks)
            self.weightage_marks=flt(cr.earned_marks)
            self.out_of_marks=flt(cr.total_marks)
            self.qualifying_status="%s"%(cr.qualifying_status)
            if addition>flt(cr.total_marks):
                frappe.throw("Grace Marks Cannot be Greater than <b>{0}</b>".format(flt(cr.total_marks)-flt(cr.earned_marks)))

        if self.out_of_marks:
            if self.grace_marks > flt(self.out_of_marks):
                frappe.throw("Grace Marks <b>{0}</b> Cannot be Greater than out of marks <b>{1}</b>".format(self.grace_marks, self.out_of_marks))
            
            if flt(self.final_marks)>flt(self.out_of_marks):
                frappe.throw("<b>Final 33,Marks</b> Cannot be Greater Than <b>Out of Marks</b>")

        if flt(self.earned_credits)>flt(self.total_credits):
            frappe.throw("<b>Earned Credits</b> Cannot be Greater Than <b>Total Credits</b>")

    @frappe.whitelist()
    def get_course_details(self):
        course=frappe.get_doc("Course",self.course)
        for d in course.get("credit_distribution"):
            if self.assessment_criteria == d.assessment_criteria:
                return d

@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                        Select 
                                enroll_cr.course,
                                enroll_cr.course_name,
                                enroll_cr.course_code
                        from `tabProgram Enrollment` enroll
                        left join `tabProgram Enrollment Course` enroll_cr on enroll.name=enroll_cr.parent 
                        where enroll.student='{0}' and enroll.docstatus=1  and (enroll_cr.course LIKE %(txt)s or enroll_cr.course_name LIKE %(txt)s or enroll_cr.course_code LIKE %(txt)s) 
                        GROUP BY enroll_cr.course
                    """.format(filters.get("student")),dict(txt="%{}%".format(txt)))    

@frappe.whitelist()
def get_assessment_criteria(doctype, txt, searchfield, start, page_len, filters):
    lst = []
    # ,"status":("!=","Completed")
    for i in frappe.get_all("Course Enrollment",{'student':filters.get("student"),"course":filters.get("course")},['name','status']):
        print(i.status)
        fltr={"parent":i.get("name")}
        if txt:
            fltr.update({'assessment_criteria': ['like', '%{}%'.format(txt)]})
        for j in frappe.get_all("Credit distribution List",fltr,["assessment_criteria"]):
            lst.append(j.assessment_criteria)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_course_assessment(student,course,assessment_criteria):
    total_earned_marks=total_total_marks=weightage_marks=0
    data_list=[]
    len_ca = len(frappe.get_all("Course Assessment",{"student":student,"course":course,"assessment_criteria":assessment_criteria, "docstatus":1},["name","earned_marks","total_marks"]))
    if len_ca > 0 :
        for d in frappe.get_all("Course Assessment",{"student":student,"course":course,"assessment_criteria":assessment_criteria, "docstatus":1},["name","earned_marks","total_marks"]):
            total_earned_marks+=flt(d.earned_marks)
            total_total_marks+=flt(d.total_marks)
            for cr in frappe.get_all("Credit distribution List",{"parent":course,"assessment_criteria":assessment_criteria},['total_marks']):
                weightage_marks=flt((total_earned_marks/total_total_marks)*flt(cr.total_marks))
            d.update({"total_earned_marks":total_earned_marks,"total_total_marks":total_total_marks,"weightage_marks":weightage_marks})
            data_list.append(d)
        return data_list
    else:
        frappe.msgprint("No evaluation found for student")
        return data_list
        

