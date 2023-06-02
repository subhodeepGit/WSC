# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ToTParticipantEnrollment(Document):
	pass
@frappe.whitelist()
def get_participants(participant_selection_id):
    participant_list=frappe.get_all("Selected Participant",{'parent':participant_selection_id},['participant_id','hrms_id','district','mobile_number','email_address'])
    return participant_list
# @frappe.whitelist()
# def enroll_participants(self):
#         total = len(self.participant_list)
#         if total > 10:
#                     frappe.msgprint(_('''Student Re-registration will be created in the background.
#                         In case of any error the error message will be updated in the Schedule.'''))
#                     frappe.enqueue(enroll_stud, queue='default', timeout=6000, event='enroll_stud',self=self)
#         else:
#             enroll_stud(self)
# def enroll_stud(self):
#     total = len(self.participant_list)
#     # print("\n\ntotal",total)
#     existed_enrollment = [p.get('student') for p in frappe.db.get_list("Program Enrollment", {'student':['in', [s.student for s in self.students]],'programs':self.programs, 'program': self.new_semester,'academic_year':self.new_academic_year, 'academic_term':self.new_academic_term,'docstatus':1 }, 'student')]
#     # print("\n\nexisted_enrollment",existed_enrollment)
#     # print(len(existed_enrollment))
#     if len(existed_enrollment) > 0:
#         frappe.msgprint(_("{0} Students already enrolled").format( ', '.join(map(str, existed_enrollment))))
#     enrolled_students = []
#     for i, stud in enumerate(self.participant_list):
#         frappe.publish_realtime("student_reregistration_tool", dict(progress=[i+1, total]), user=frappe.session.user)
#         if stud.student and stud.student not in existed_enrollment:
#             prog_enrollment = frappe.new_doc("Program Enrollment")
#             prog_enrollment.student = stud.student
#             prog_enrollment.student_name = stud.student_name
#             prog_enrollment.roll_no=stud.roll_no
#             prog_enrollment.permanant_registration_number=stud.permanant_registration_number
#             prog_enrollment.programs = self.programs
#             prog_enrollment.program = self.new_semester
#             prog_enrollment.academic_year = self.new_academic_year
#             prog_enrollment.academic_term = self.new_academic_term
#             prog_enrollment.is_provisional_admission="No"
#             prog_enrollment.admission_status="Admitted"
#             # prog_enrollment.student_batch_name = stud.student_batch_name if stud.student_batch_name else self.new_student_batch
#             if self.new_student_batch:
#                 prog_enrollment.student_batch_name = self.new_student_batch
#             else:
#                 prog_enrollment.student_batch_name = stud.student_batch_name
#             if stud.additional_course_1:
#                 course_data  = frappe.db.get_value("Course",{'name':stud.additional_course_1},["course_name", "course_code"], as_dict=1)
#                 if course_data:
#                     course_data = course_data
#                     create_course_row(prog_enrollment,stud.additional_course_1,course_data.course_name,course_data.course_code)
#             for c in self.courses:
#                 create_course_row(prog_enrollment,c.course,c.course_name,c.course_code)
#             for pe in frappe.get_all("Program Enrollment",filters={"student":stud.student},order_by='`creation` DESC',limit=1):
#                 prog_enrollment.reference_doctype="Program Enrollment"
#                 prog_enrollment.reference_name=pe.name
#             prog_enrollment.save()
#             prog_enrollment.submit()
#             enrolled_students.append(stud.student)
#     frappe.msgprint(_("{0} Students have been enrolled").format(', '.join(map(str, enrolled_students))))
#     # frappe.publish_realtime("fee_schedule_progress", {"progress": str(int(created_records * 100/total_records)),"reload": 1}, user=frappe.session.user)