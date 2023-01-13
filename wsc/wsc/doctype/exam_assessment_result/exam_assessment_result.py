# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.exceptions import DocumentAlreadyRestored
from frappe.model.document import Document
from frappe import _
from frappe.utils import flt
from education.education.api import get_grade
from education.education.api import get_assessment_details
from frappe.utils.csvutils import getlink
import education.education
from wsc.wsc.utils import duplicate_row_validation

class ExamAssessmentResult(Document):
    def on_submit(self):
        duplicate_row_validation(self, "assessment_result_item", ['course','assessment_criteria'])
        self.set_evaluation_result_item()
        self.set_grade()
        self.map_fields()
        self.calculate_cgpa()
        self.validate_duplicate_for_submit()
        self.complete_course_enrollment()
        self.get_sgpa_into_total_credit()
    def validate(self):
        self.get_sgpa_into_total_credit()
        self.set_evaluation_result_item()
        self.set_grade()
        self.calculate_cgpa()
        if len(self.assessment_result_item) > 0:
            self.calculate_sgpa()
    def on_change(self):
        # if len(self.assessment_result_item) > 0:
        #     self.calculate_sgpa()
        # self.calculate_cgpa()
        self.get_sgpa_into_total_credit()

    @frappe.whitelist()
    def set_assessment_result_items(self):
        print("\n\n\nHello15")
        allocations=0
        self.assessment_result_item = []
        result = []
        for allocation in frappe.get_all("Assessment Credits Allocation",{"docstatus":1,"student":self.student,"academic_year":self.academic_year,"academic_term":self.academic_term},["course","earned_credits","total_credits","final_marks","out_of_marks","assessment_criteria"]):
            print("\n\nAllocation")
            print(allocation.total_credits)
            allocations+=allocation.total_credits
            row = {
                "course":allocation.course,
                "earned_cr":allocation.earned_credits,
                "total_cr":allocation.total_credits,
                "earned_marks":allocation.final_marks,
                "total_marks":allocation.out_of_marks,
                "assessment_criteria":allocation.assessment_criteria
            }
            if row not in result:
                result.append(row)
        for r in result:
            self.append("assessment_result_item", r)
        self.credit_point=allocations
    def get_sgpa_into_total_credit(self):
        allocations=0
        # sgpa_in_to_credit_points=0
        for allocation in frappe.get_all("Assessment Credits Allocation",{"docstatus":1,"student":self.student,"academic_year":self.academic_year,"academic_term":self.academic_term},["course","earned_credits","total_credits","final_marks","out_of_marks","assessment_criteria"]):
            print("\n\nAllocation")
            print(allocation.total_credits)
            allocations+=allocation.total_credits
        print("\n\nafter allocation")
        print(allocations)
        print("\n\ncCreate sgpa")
        print(self.sgpa)
        # print(self.sgpa_in_to_credit_point)
        self.credit_point=allocations
        print("\n\nNEw Credit_point")
        print(self.credit_point)
        # sgpa_in_to_credit_points= float(self.credit_point) * float(self.sgpa)
        # resu = "{:.2f}".format(sgpa_in_to_credit_points)
        # self.sgpa_in_to_credit_point=resu
        # frappe.db.set_value("Exam Assessment Result",self.name,"credit_point",allocations)
        # frappe.db.set_value("Exam Assessment Result",self.name,"sgpa_in_to_credit_point",resu)
        # frappe.db.set("credit_point",allocations)
    @frappe.whitelist()
    def set_assessment_result_item(self):
        print("\n\n\nHello15")
        allocations=0
        self.assessment_result_item = []
        result = []
        for allocation in frappe.get_all("Assessment Credits Allocation",{"docstatus":1,"student":self.student,"academic_year":self.academic_year,"academic_term":self.academic_term},["course","earned_credits","total_credits","final_marks","out_of_marks","assessment_criteria"]):
            print("\n\nAllocation")
            print(allocation.total_credits)
            allocations+=allocation.total_credits
            row = {
                "course":allocation.course,
                "earned_cr":allocation.earned_credits,
                "total_cr":allocation.total_credits,
                "earned_marks":allocation.final_marks,
                "total_marks":allocation.out_of_marks,
                "assessment_criteria":allocation.assessment_criteria
            }
            if row not in result:
                result.append(row)
        for r in result:
            self.append("assessment_result_item", r)
        self.credit_point=allocations
    # def on_submit(self):
        # print("\n\n\n\n\n\nhelll4")
        # self.validate_duplicate_for_save()
        # self.complete_course_enrollment()
        # if len(self.assessment_result_item) > 0:
        #     self.calculate_sgpa()
        # self.set_evaluation_result_item()
        # self.validate_duplicate_for_submit()
        # self.update_program_enrollment_result()

    def set_grade(self):
        print("\n\n\nHello14")
        self.total_score = 0.0
        self.maximum_score=0.0
        total_pass=0
        for d in self.assessment_result_item:
            if flt(d.total_marks) > 0.0 :
                d.grade = get_grade(self.grading_scale, (flt(d.earned_marks)/flt(d.total_marks))*100)
                self.total_score += flt(d.earned_marks)
                self.maximum_score +=flt(d.total_marks)
                
            for g in frappe.get_all("Grading Scale Interval",{"parent":self.grading_scale,"grade_code":d.grade},['result']):
                if g.result=="PASS":
                    d.result="P"
                else:
                    d.result="F"
                    
            for cr in frappe.get_all("Credit distribution List",{"parent":d.course,"assessment_criteria":d.assessment_criteria},['passing_marks']):
                if flt(cr.passing_marks) > flt(d.earned_marks):
                    d.result="F"
                else:
                    d.result="P"

            if d.result=="P":
                total_pass+=1

        if len(self.assessment_result_item)==total_pass and total_pass > 0:
            self.result="Pass"  
        
        elif total_pass!=0:
            self.result="Backlog"

        if self.maximum_score > 0:
            self.grade = get_grade(self.grading_scale, (self.total_score/self.maximum_score)*100)

        for d in self.evaluation_result_item:
            print("\n\n\nHello13")
            if flt(d.total_marks) > 0.0 :
                d.grade = get_grade(self.grading_scale, (flt(d.earned_marks)/flt(d.total_marks))*100)
                self.total_score += flt(d.earned_marks)
                self.maximum_score +=flt(d.total_marks)
            assessment_criteria = [a.assessment_criteria for a in self.assessment_result_item if a.course == d.course ]
            for cr in frappe.get_all("Credit distribution List",{"parent":d.course,"assessment_criteria":assessment_criteria[0]},['passing_marks']):
                if flt(cr.passing_marks) > flt(d.earned_marks):
                    d.result="F"
                else:
                    d.result="P"
                
            for g in frappe.get_all("Grading Scale Interval",{"parent":self.grading_scale,"grade_code":d.grade},['result']):
                if g.result=="PASS":
                    d.result="P"
                else:
                    d.result="F"

    # def validate_duplicate_for_save(self):
    #     print("\n\n\nHello12")
    #     assessment_result = frappe.get_list("Exam Assessment Result", filters={"name": ("not in", [self.name]),
    #         "student":self.student, "docstatus":0,'programs':self.programs, 'program':self.program})
    #         # "docstatus":1,
    #     if assessment_result:
    #         frappe.throw(_("Exam Assessment Result record {0} already exists.").format(getlink("Exam Assessment Result",assessment_result[0].name)))
    def validate_duplicate_for_submit(self):
        print("\n\n\nHello11")
        assessment_result = frappe.get_list("Exam Assessment Result", filters={"name": ("not in", [self.name]),
            "student":self.student, "docstatus":1,'programs':self.programs, 'program':self.program})
            # "docstatus":1,
        if assessment_result:
            frappe.throw(_("Exam Assessment Result record {0} already exists.").format(getlink("Exam Assessment Result",assessment_result[0].name)))
    # def validate_years(self):
    #     duplicateForm=frappe.get_all("Self Appraisal Form", filters={
    #         "employee_id":self.employee_id,
    #         "appraisal_year": self.appraisal_year,
    #         "name":("!=",self.name)
    #     })
    #     if duplicateForm:
    #         frappe.throw(("Employee is already Filled the form for this Year."))
    def calculate_sgpa(self):
        
        earn_and_garde=earn=0
        # evaluation_result_item
        for d in self.get("evaluation_result_item"):
            if self.grade and self.grading_scale:
                if d.earned_cr:
                    earn+=d.earned_cr
                    for g in frappe.get_all("Grading Scale Interval",{"parent":self.grading_scale,"grade_code":d.grade},['grade_point']):
                        earn_and_garde+=((d.earned_cr or 0)*(g.grade_point or 0))
        if earn > 0 :
            # self.sgpa=(earn_and_garde/earn)
            self.sgpa=round((earn_and_garde/earn),2)
            self.sgpa="{:.2f}".format(earn_and_garde/earn)
            print("\n\ncredit_point")
            print(self.credit_point)
            print(self.sgpa)
            sgpa_in_credit_points=0
            sgpa_in_credit_points = float(self.credit_point) * float(self.sgpa)
            self.sgpa_in_to_credit_point=sgpa_in_credit_points
            print("\n\nYO:YOsgpa_in_to_credit_point")
            print(self.sgpa_in_to_credit_point)
    def map_fields(self):
        order_dict={1:"1ST SEM",2:"2ND SEM",3:"3RD SEM",4:"4TH SEM",5:"5TH SEM",6:"6TH SEM",7:"7TH SEM",8:"8TH SEM",9:"9TH SEM",10:"10TH SEM"}
        for d in self.get("previous_semesters_sgpa"):
            if not d.semester_order:
                db=frappe.db.sql("""select name,semester_order from `tabProgram` where name="%s" """%(d.semester))
                for sem in frappe.db.get_all("Program",{"name":"%s"%(d.semester)},['name',"semester_order"]):
                    d.seemster_order=order_dict.get(sem.semester_order)
				
    def calculate_cgpa(self):
        total_sgpa=0
        credit_points=0
        semester_numbers=0
        tot_multi_credit=0
        sgpa_in_to_credit_points=0
        overall_cgpa=0
        order_dict={1:"1ST SEM",2:"2ND SEM",3:"3RD SEM",4:"4TH SEM",5:"5TH SEM",6:"6TH SEM",7:"7TH SEM",8:"8TH SEM",9:"9TH SEM",10:"10TH SEM"}
        for sem in frappe.get_all("Program",{"name":self.program},['name',"semester_order"],order_by="semester_order"):
            for result in frappe.get_all("Exam Assessment Result",{"student":self.student},['sgpa','program','programs','sgpa_in_to_credit_point','credit_point']):        
                print("\n\ncredit_point")
                print(result.credit_point)
                real_credit_point=float(result.credit_point)
                print(real_credit_point)
                print("\n\nTotal MULTI Credit")
                tot_multi_credit=float(result.sgpa_in_to_credit_point)
                print(tot_multi_credit)
                sgpa_in_to_credit_points+=tot_multi_credit
                credit_points+=real_credit_point
                print("\n\nsgpa_in_to_credit_point")
                print(sgpa_in_to_credit_points)
                # ,'program':sem.name       
                # "docstatus":1,
                self.append("previous_semesters_sgpa",{
					"semester":result.program,
                    "semester_order":order_dict.get(sem.semester_order),
                    # "semester_number":self.semester_number,
					"sgpa":round(result.sgpa,2),
                    # "sgpa_in_to_credit_point":result.sgpa_in_to_credit_point,
                    # "credit_point":result.credit_point
                    
                })
                self.programs=result.programs
                # total_sgpa+=result.sgpa
                # credit_points+=result.credit_point
                # sgpa_in_to_credit_points+=result.sgpa_in_to_credit_point
                self.semester_number=1
                semester_numbers+=self.semester_number
                self.result_p_f=frappe.db.get_value("Exam Assessment Result",result.exam_assessment_result,'result')
                # if len(self.get("previous_semesters_sgpa")):
                # self.overall_cgpa=(total_sgpa/len(self.get("previous_semesters_sgpa")))
                print("\n\nsgpa_in_to_credit_point SECOND")
                print(sgpa_in_to_credit_points)
                print("\n\ncredit_pointsss")
                print(credit_points)
                overall_cgpa=(sgpa_in_to_credit_points/credit_points)
                print("\n\nCGPA HAHA")
                print(overall_cgpa)
                    # self.overall_cgpa=((total_sgpa+self.sgpa)/total_semester_order)
                    # round(overall_cgpa,2)
                res = "{:.2f}".format(overall_cgpa)
                print("\n\nRESSS")
                print(res)
                self.overall_cgpa=res
                print("\n\nFinal CGPAAAA")
                print(self.overall_cgpa)
                #     # self.set("overall_cgpa",res)
                frappe.db.set_value("Exam Assessment Result",self.name,"overall_cgpa",res)


                    # frappe.db.set_value("", "_Test Customer", "credit_days", 10)

                    # frappe.db.set_value('Exam Assessment Result', 'name', 'overall_cgpa', 'res')
                
				# self.completed_on=result.modified
    def complete_course_enrollment(self):
        for item in self.get("evaluation_result_item"):
            if item.result=="P":
                for enroll in frappe.get_all("Course Enrollment",{"student":self.student,"course":item.course}):
                    course_enroll=frappe.get_doc("Course Enrollment",enroll.name)
                    course_enroll.status="Completed"
                    course_enroll.save()

    def set_evaluation_result_item(self):
        duplicate=[]
        self.set("evaluation_result_item",[])
        for row in self.get("assessment_result_item"):
            earned_cr=total_cr=earned_marks=total_marks=0
            if row.course not in duplicate:
                for d in self.get("assessment_result_item"):
                    duplicate.append(row.course)
                    if row.course==d.course:
                        earned_cr+=flt(d.earned_cr)
                        total_cr+=flt(d.total_cr)
                        earned_marks+=flt(d.earned_marks)
                        total_marks+=flt(d.total_marks)
                self.append("evaluation_result_item",{
                    "course":row.course,
                    "course_name":frappe.db.get_value("Course",row.course,'course_name'),
                    "course_code":frappe.db.get_value("Course",row.course,'course_code'),
                    "earned_cr":earned_cr,
                    "total_cr":total_cr,
                    "earned_marks":earned_marks,
                    "total_marks":total_marks
                })
 
@frappe.whitelist()
def get_grade_result(grading_scale, earned_marks, total_marks):
    grade = get_grade(grading_scale, (flt(earned_marks)/flt(total_marks))*100)
    for g in frappe.get_all("Grading Scale Interval",{"parent":grading_scale,"grade_code":grade},['result']):
        if g.result=="PASS":
            result="P"
        else:
            result="F"
        return {'grade': grade, 'result':result}        

@frappe.whitelist()
def get_assessment_status(student,semester,academic_year,academic_term):
    completed=False
    for course_enroll in frappe.get_all("Course Enrollment",{"student":student,"academic_year":academic_year,"academic_term":academic_term, "semester": semester}):
        for enroll_item in frappe.get_all("Credit distribution List",{"parent":course_enroll.name},['assessment_criteria']):
            completed=True
            if len(frappe.get_all("Assessment Credits Allocation",{'student':student,'assessment_criteria':enroll_item.assessment_criteria,"academic_year":academic_year,"academic_term":academic_term,"docstatus":1}))==0:
                completed=False 
    return completed  

@frappe.whitelist()
def get_student_details(student):
    if student:
        data=frappe.get_all("Program Enrollment",{'student':student,'docstatus':1},['programs', 'program', 'academic_year', 'academic_term'],limit=1)
        if len(data)>0:
            return data[0]  
        else:
            frappe.throw("Program not enrolled by student {0}".format(student))  
        
@frappe.whitelist()
def filter_courses(doctype, txt, searchfield, start, page_len, filters):
    print("\n\n\nHello1")
    if len(frappe.get_all("Exam Application",{'student':filters.get('student'),'docstatus':1},['name'])) > 0:
        for app in frappe.get_all("Exam Application",{'student':filters.get('student'),'docstatus':1},['name']):
            return frappe.get_all("Exam Application Courses",{'parent':app.get('name'),'course_name': ['like', '%{}%'.format(txt)]},['course', 'course_name'], as_list=1)
    else:
        frappe.msgprint("Exam Application not found for student")
        return []
