# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions


class CourseAssessment(Document):
    def validate(self):
        self.validate_attendance()
        self.validate_marks()
        self.qualifying_status()
        self.exam_type()
        self.get_module_wise_exam_group()
        self.validate_marker()
    def on_submit(self):
        self.create_permissions()
    def create_permissions(doc):
        for instr in frappe.get_all("Instructor",{"name":doc.trainer_id},['department','name','employee']):
            for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id','department']):
                if emp.user_id:
                    add_user_permission(doc.doctype,doc.name,emp.user_id,doc)	

    def validate_marker(self):
        for id in frappe.get_all("Instructor",{"email_id":frappe.session.user},['name','email_id']):
            if id.name==self.trainer_id:
                pass
            else:
                frappe.throw("You do not have the permission to give marks to the students for this module!!!")
    def get_module_wise_exam_group(self):
        exam_declaration=self.exam_declaration
        course=self.course
        data=frappe.get_all("Module Wise Exam Group",{"exam_declaration_id":exam_declaration,"modules_id":course,"docstatus":1},['name'])
        if data:
            self.module_wise_exam_group=data[0]['name']
        else:
            frappe.throw("No Module Wise Exam Group Found")
        
    def on_update_after_submit(self):
        self.qualifying_status()  

    def exam_type(self):
        exam_category=frappe.get_all("Exam Declaration",{"name":self.exam_declaration},['exam_category'])
        self.exam_category=exam_category[0]['exam_category']

    def qualifying_status(self):
        passing_marks=frappe.get_all("Credit distribution List", {"parent":self.course,"assessment_criteria":self.assessment_criteria},['passing_marks'])
        passing_marks=passing_marks[0]['passing_marks']
        self.passing_marks=flt(passing_marks)
        earned_marks=flt(self.earned_marks)
        if passing_marks<=earned_marks:
            self.qualifying_status_data="Pass"
        else:
            self.qualifying_status_data="Fail"

    def validate_marks(self):
        if flt(self.earned_marks)>flt(self.total_marks):
            frappe.throw("<b>Earned Marks</b> Cannot be Greater Than <b>Total Marks</b>")

    def validate_attendance(self):
        if self.attendence_status=="Absent":
            if flt(self.earned_marks)!=0:
                frappe.throw("If Attendence Status <b>Absent </b> Then <b>Earned Marks Can't be more the Zero </b>")

@frappe.whitelist()
def get_module_details(module,assessment_component):
	for result in frappe.get_all("Module Wise Exam Group",{"modules_id":module,"assessment_component":assessment_component},['name','marker_name','checker','marker','checker_name']):
                
		return result

@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    data=frappe.db.sql(""" Select EC.courses,EC.course_name,EC.course_code
                       from `tabExam Courses` EC
                       Join `tabExam Declaration` ED on ED.name=EC.parent 
                       where EC.parent='{0}' and ED.docstatus=1 """.format(filters.get("exam_declaration")))
    # data=frappe.db.sql("""select 
    #                             ce.course,ce.course_name,ce.course_code
    #                     from 
    #                         `tabCourse Enrollment` ce 
    #                     where status!="Completed" and student='{0}' and ce.academic_year='{1}' and ce.academic_term='{2}' and (ce.course like '%{3}%' 
    #                     or ce.course_name like '%{3}%' or ce.course_code like '%{3}%') """
    #                     .format(filters.get("student"),filters.get("academic_year"),filters.get("academic_term"),txt))
    return data if data else []
    
@frappe.whitelist()
def get_assessment_criteria(doctype, txt, searchfield, start, page_len, filters):
    data=frappe.db.sql(""" Select ED.assessment_criteria 
                        from `tabExam Declaration` ED 
                        where ED.name='{0}' and ED.docstatus=1 """.format(filters.get("exam_declaration")))
    # lst = []
    # for i in frappe.get_all("Course Enrollment",{'student':filters.get("student"),"course":filters.get("course"),"status":("!=","Completed")},['name']):
    #     fltr={"parent":i.get("name")}
    #     if txt:
    #         fltr.update({"assessment_criteria":txt})
    #     for j in frappe.get_all("Credit distribution List",fltr,["assessment_criteria"]):
    #         if j.assessment_criteria not in lst:
    #             if j.assessment_criteria:
    #                 lst.append(j.assessment_criteria)
    # return [(d,) for d in lst]
    return data if data else []

@frappe.whitelist()
def get_details(student,course):
    for ce in frappe.get_all("Course Enrollment",{"student":student,"course":course},["program_enrollment"]):
        return frappe.db.get_value("Program Enrollment",ce.program_enrollment,["programs","program","academic_year","academic_term"],as_dict=1)

@frappe.whitelist()
def get_exam_declaration(doctype, txt, searchfield, start, page_len, filters):


        # declarations=[]
    # if len(frappe.get_all("Program Enrollment",{"student":student, "docstatus":1},['programs',"program"]))!=0:
    #     for d in frappe.get_all("Program Enrollment",{"student":student, "docstatus":1},['programs',"program","name"]):
    #         filters.update({"exam_program":d.get("programs"),"docstatus":1})
    #         for ed in frappe.get_all("Exam Declaration",filters,["name","exam_name"],as_list=1):
    #             # if frappe.db.get_value("Examination Semester",{"parent":ed[0],"semester":d.get("program")}):
    #             declarations.append(ed)
    #         return declarations
    # else:
    #     return []


    student=filters.get("student")
    filters.pop("student")

    declarations=[]
    module_wise_exam_student_data=frappe.get_all("Module Wise Exam Student", {"student_no":student},['name',"parent"])
    if module_wise_exam_student_data:
        module_wise_exam_group_data=[]
        for t in module_wise_exam_student_data:
            module_wise_exam_group_data.append(t['parent'])
        module_wise_exam_group_data=list(set(module_wise_exam_group_data))
        if module_wise_exam_group_data:
            declarations=frappe.get_all("Module Wise Exam Group",filters=[["name","in",module_wise_exam_group_data],['docstatus','=','1']],fields=['exam_declaration_id'], as_list=True)
    return declarations if declarations else []





@frappe.whitelist()
def get_assessment_criteria_detail(course,criteria):
    for data in frappe.get_all("Credit distribution List",{"parent":course,"assessment_criteria":criteria},["credits","total_marks",'passing_marks']):
        return data

@frappe.whitelist()
def get_exam_assessment_plan(doctype, txt, searchfield, start, page_len, filters):
    plan=[]

    for pl in frappe.get_all("Exam Assessment Plan",{"name": ["like", "%{0}%".format(txt)],"programs":filters.get("programs"),"program":filters.get("program"),"academic_year":filters.get("academic_year"),"exam_declaration":filters.get("exam_declaration"),"docstatus":filters.get("docstatus")},as_list=1):
        for cr in frappe.get("Course Assessment Plan Item",{"parent":pl.name,"course":filters.get("course")}):
            plan.append(pl)

    return plan