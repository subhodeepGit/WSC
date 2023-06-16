# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe,json
from frappe import msgprint, _
from frappe.utils import comma_and, get_link_to_form,get_link_to_form, getdate, formatdate
from frappe.model.document import Document
from erpnext import get_default_company
from education.education.api import get_student_group_students
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday

class StudentsAttendanceTool(Document):
	pass


@frappe.whitelist()
def mark_attendance(students_present, students_absent, students_on_leave, course_schedule=None, student_group=None,building=None,hostel_category=None, date=None,attendance_for=None):
    """Creates Multiple Attendance Records.

    :param students_present: Students Present JSON.
    :param students_absent: Students Absent JSON.
    :param course_schedule: Course Schedule.
    :param student_group: Student Group.
    :param date: Date.
    """
    if student_group:
        academic_year = frappe.db.get_value('Student Group', student_group, 'academic_year')
        if academic_year:
            year_start_date, year_end_date = frappe.db.get_value('Academic Year', academic_year, ['year_start_date', 'year_end_date'])
            if getdate(date) < getdate(year_start_date) or getdate(date) > getdate(year_end_date):
                frappe.throw(_('Attendance cannot be marked outside of Academic Year {0}').format(academic_year))

    present = json.loads(students_present)
    absent = json.loads(students_absent)
    on_leave = json.loads(students_on_leave)

    for d in present:
        make_attendance_records(d["student"], d["student_name"], "Present", course_schedule, student_group,building,hostel_category, date,attendance_for)

    for d in absent:
        make_attendance_records(d["student"], d["student_name"], "Absent", course_schedule, student_group,building,hostel_category, date,attendance_for)

    for d in on_leave:
        make_attendance_records(d["student"], d["student_name"], "On Leave", course_schedule, student_group,building,hostel_category, date,attendance_for)

    frappe.db.commit()
    frappe.msgprint(_("Attendance has been marked successfully."))


def make_attendance_records(student, student_name, status, course_schedule=None, student_group=None,building=None,hostel_category=None, date=None,attendance_for=None):
    """Creates/Update Attendance Record.

    :param student: Student.
    :param student_name: Student Name.
    :param course_schedule: Course Schedule.
    :param status: Status (Present/Absent)
    """
    student_attendance = frappe.get_doc({
        "doctype": "Student Attendance",
        "student": student,
        "student": student_name,
        "course_schedule": course_schedule,
        "student_group": student_group,
        "date": date
    })
    if not student_attendance:
        student_attendance = frappe.new_doc("Student Attendance")
    student_attendance.student = student
    student_attendance.student_name = student_name
    student_attendance.course_schedule = course_schedule
    student_attendance.student_group = student_group
    student_attendance.date = date
    student_attendance.status = status

    if attendance_for and building:
        student_attendance.building=building
        student_attendance.hostel_room=hostel_category

    student_attendance.attendance_for=attendance_for if attendance_for else "Day Scholar"
    student_attendance.save()
    student_attendance.submit()


@frappe.whitelist()
def get_student_attendance_records(
    based_on, date=None, student_group=None, course_schedule=None
):
    student_list = []
    student_attendance_list = []

    if based_on == "Course Schedule":
        student_group = frappe.db.get_value(
            "Course Schedule", course_schedule, "student_group"
        )
        if student_group:
            student_list = frappe.get_all(
                "Student Group Student",
                fields=["student", "student_name", "group_roll_number",'roll_no'],
                filters={"parent": student_group, "active": 1},
                order_by="group_roll_number",
            )

    if not student_list:
        student_list = frappe.get_all(
            "Student Group Student",
            fields=["student", "student_name", "group_roll_number",'roll_no'],
            filters={"parent": student_group, "active": 1},
            order_by="group_roll_number",
        )

    StudentAttendance = frappe.qb.DocType("Student Attendance")

    if course_schedule:
        student_attendance_list = (
            frappe.qb.from_(StudentAttendance)
            .select(StudentAttendance.student, StudentAttendance.status)
            .where((StudentAttendance.course_schedule == course_schedule))
        ).run(as_dict=True)
    else:
        student_attendance_list = (
            frappe.qb.from_(StudentAttendance)
            .select(StudentAttendance.student, StudentAttendance.status)
            .where(
                (StudentAttendance.student_group == student_group)
                & (StudentAttendance.date == date)
                & (
                    (StudentAttendance.course_schedule == "")
                    | (StudentAttendance.course_schedule.isnull())
                )
            )
        ).run(as_dict=True)

    for attendance in student_attendance_list:
        for student in student_list:
            if student.student == attendance.student:
                student.status = attendance.status

    print("\n\n\n\n",student_list)
    if based_on=="Student Group":
        for t in student_list:
            get_leave_status = frappe.get_all("Leave Application for Student",filters=[['student',"=",t['student']], ['from_date','<=',date],['to_date','>=', date], ['leave_criteria','=','Full Day']],fields=['name','student','reason_for_leave','workflow_state'])
            if get_leave_status:
                t['leave_status']=get_leave_status[0]['workflow_state']
                t['reason_for_leave']=get_leave_status[0]['reason_for_leave']
                t['leave_app_id']=get_leave_status[0]['name']
    if based_on=="Course Schedule":
        for t in student_list:
            get_leave_status = frappe.get_all("Leave Application for Student",filters=[['student',"=",t['student']], ['from_date','<=',date],['to_date','>=', date]],fields=['name','reason_for_leave','workflow_state'])
            if get_leave_status:
                leave_course_schedule=frappe.get_all("Class Wise Leave",{"parent":get_leave_status[0]['name'],'class_schedule_id':course_schedule, 'leave_applicability_check':1})
                if leave_course_schedule:
                    t['leave_status']=get_leave_status[0]['workflow_state']
                    t['reason_for_leave']=get_leave_status[0]['reason_for_leave']
                    t['leave_app_id']=get_leave_status[0]['name']
    return student_list

