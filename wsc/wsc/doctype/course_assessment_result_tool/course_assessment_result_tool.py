# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

# import frappe

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, cstr, getdate
from frappe.email.doctype.email_group.email_group import add_subscribers
from frappe.model.document import Document
from wsc.wsc.utils import get_courses_by_semester
class CourseAssessmentResultTool(Document):
	pass

# @frappe.whitelist()
# def get_enroll_students(academic_year,academic_term,programs,semesters,course,criteria):
# 	student_list=[]
# 	course_assessment={}
# 	count=0
# 	for pr_enroll in frappe.get_all("Program Enrollment",{"academic_year":academic_year,"programs":programs,"program":semesters,"docstatus":1,"academic_term":academic_term},order_by="roll_no asc"):
# 		for cr_enroll in frappe.get_all("Course Enrollment",{"course":course,"program_enrollment":pr_enroll.name},["student","student_name","roll_no","registration_number","semester","programs"]):
# 			count+=1
# 			cr_enroll.update({"id":count})
# 			for cr_asmt in frappe.get_all("Course Assessment",{"docstatus":("!=",2),"student":cr_enroll.student,"academic_year":academic_year,"academic_term":academic_term,'course':course,'programs':programs,"assessment_criteria":criteria},['earned_marks','total_marks',"name","programs"]):
# 				course_assessment[cr_enroll.student]={"earned_marks":cr_asmt.earned_marks,"total_marks":cr_asmt.total_marks}
# 			student_list.append(cr_enroll.update(get_total_marks(course,criteria)))
# 	return student_list,course_assessment

@frappe.whitelist()
def get_enroll_students(course,criteria,exam_declaration):
	student_list=[]
	course_assessment={}
	if exam_declaration and course:
		count=0
		exam_group_data=frappe.get_all("Module Wise Exam Group",{"docstatus":1,"exam_declaration_id":exam_declaration,"modules_id":course},['name'])
		credit_distribution_list=frappe.get_all("Credit distribution List",{"parent":course,"assessment_criteria":criteria},["credits","total_marks"])
		if credit_distribution_list:
			for t in exam_group_data:
				student_list=frappe.db.sql(""" Select MWES.student_no,MWES.student_name,MWES.roll_no,MWES.student_no,MWES.permanent_registration_no,MWEG.semester,MWEG.course_type	
									from `tabModule Wise Exam Student` MWES
									JOIN `tabStudent` S ON S.name=MWES.student_no
									JOIN `tabModule Wise Exam Group` MWEG ON MWEG.name=MWES.parent
									where MWES.parent='%s' and MWES.examination_qualification_approval=1 and S.enabled=1 
									ORDER BY MWES.roll_no ASC """%(t['name']),as_dict=1)
				for t in student_list:
					count+=1
					t.update({"id":count,'credits':credit_distribution_list[0]['credits'],'total_marks':credit_distribution_list[0]['total_marks']})

	return student_list,course_assessment



def get_course(program):
	'''Return list of courses for a particular program
	:param program: Program
	'''
	courses = frappe.db.sql('''select course, course_name from `tabProgram Course` where parent=%s''',
			(program), as_dict=1)
	return courses

@frappe.whitelist()
def enroll_student(source_name):
	"""Creates a Student Record and returns a Program Enrollment.

	:param source_name: Student Applicant.
	"""
	frappe.publish_realtime('enroll_student_progress', {"progress": [1, 4]}, user=frappe.session.user)
	student = get_mapped_doc("Student Applicant", source_name,
		{"Student Applicant": {
			"doctype": "Student",
			"field_map": {
				"name": "student_applicant"
			}
		}}, ignore_permissions=True)
	student.save()
	program_enrollment = frappe.new_doc("Program Enrollment")
	program_enrollment.student = student.name
	program_enrollment.student_category = student.student_category
	program_enrollment.student_name = student.student_name
	program_enrollment.roll_no=student.roll_no
	program_enrollment.program = frappe.db.get_value("Student Applicant", source_name, "program")
	frappe.publish_realtime('enroll_student_progress', {"progress": [2, 4]}, user=frappe.session.user)
	return program_enrollment


@frappe.whitelist()
def check_attendance_records_exist(course_schedule=None, student_group=None, date=None):
	"""Check if Attendance Records are made against the specified Course Schedule or Student Group for given date.

	:param course_schedule: Course Schedule.
	:param student_group: Student Group.
	:param date: Date.
	"""
	if course_schedule:
		return frappe.get_list("Student Attendance", filters={"course_schedule": course_schedule})
	else:
		return frappe.get_list("Student Attendance", filters={"student_group": student_group, "date": date})


@frappe.whitelist()
def mark_attendance(students_present, students_absent, course_schedule=None, student_group=None, date=None):
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

	for d in present:
		make_attendance_records(d["student"], d["student_name"], "Present", course_schedule, student_group, date)

	for d in absent:
		make_attendance_records(d["student"], d["student_name"], "Absent", course_schedule, student_group, date)

	frappe.db.commit()
	frappe.msgprint(_("Attendance has been marked successfully."))


def make_attendance_records(student, student_name, status, course_schedule=None, student_group=None, date=None):
	"""Creates/Update Attendance Record.

	:param student: Student.
	:param student_name: Student Name.
	:param course_schedule: Course Schedule.
	:param status: Status (Present/Absent)
	"""
	student_attendance = frappe.get_doc({
		"doctype": "Student Attendance",
		"student": student,
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
	student_attendance.save()
	student_attendance.submit()


@frappe.whitelist()
def get_student_guardians(student):
	"""Returns List of Guardians of a Student.

	:param student: Student.
	"""
	guardians = frappe.get_list("Student Guardian", fields=["guardian"] ,
		filters={"parent": student})
	return guardians


@frappe.whitelist()
def get_student_group_students(student_group, include_inactive=0):
	"""Returns List of student, student_name in Student Group.

	:param student_group: Student Group.
	"""
	if include_inactive:
		students = frappe.get_list("Student Group Student", fields=["student", "student_name", "roll_no"] ,
			filters={"parent": student_group}, order_by= "group_roll_number")
	else:
		students = frappe.get_list("Student Group Student", fields=["student", "student_name", "roll_no"] ,
			filters={"parent": student_group, "active": 1}, order_by= "group_roll_number")
	return students


@frappe.whitelist()
def get_fee_structure(program, academic_term=None):
	"""Returns Fee Structure.

	:param program: Program.
	:param academic_term: Academic Term.
	"""
	fee_structure = frappe.db.get_values("Fee Structure", {"program": program,
		"academic_term": academic_term, "docstatus":1}, 'name', as_dict=True)
	return fee_structure[0].name if fee_structure else None


@frappe.whitelist()
def get_fee_components(fee_structure):
	"""Returns Fee Components.

	:param fee_structure: Fee Structure.
	"""
	if fee_structure:
		fs = frappe.get_list("Fee Component", fields=["fees_category", "description", "amount"] , filters={"parent": fee_structure}, order_by= "idx")
		return fs


@frappe.whitelist()
def get_fee_schedule(program, student_category=None):
	"""Returns Fee Schedule.

	:param program: Program.
	:param student_category: Student Category
	"""
	fs = frappe.get_list("Program Fee", fields=["academic_term", "fee_structure", "due_date", "amount"] ,
		filters={"parent": program, "student_category": student_category }, order_by= "idx")
	return fs


@frappe.whitelist()
def collect_fees(fees, amt):
	paid_amount = flt(amt) + flt(frappe.db.get_value("Fees", fees, "paid_amount"))
	total_amount = flt(frappe.db.get_value("Fees", fees, "total_amount"))
	frappe.db.set_value("Fees", fees, "paid_amount", paid_amount)
	frappe.db.set_value("Fees", fees, "outstanding_amount", (total_amount - paid_amount))
	return paid_amount


@frappe.whitelist()
def get_course_schedule_events(start, end, filters=None):
	"""Returns events for Course Schedule Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Course Schedule", filters)

	data = frappe.db.sql("""select name, course, color,
			timestamp(schedule_date, from_time) as from_datetime,
			timestamp(schedule_date, to_time) as to_datetime,
			room, student_group, 0 as 'allDay'
		from `tabCourse Schedule`
		where ( schedule_date between %(start)s and %(end)s )
		{conditions}""".format(conditions=conditions), {
			"start": start,
			"end": end
			}, as_dict=True, update={"allDay": 0})

	return data


@frappe.whitelist()
def get_assessment_criteria(course):
	"""Returns Assessmemt Criteria and their Weightage from Course Master.

	:param Course: Course
	"""
	return frappe.get_list("Course Assessment Criteria", \
		fields=["assessment_criteria", "weightage"], filters={"parent": course}, order_by= "idx")




@frappe.whitelist()
def get_assessment_details(course_assessment_plan):
	"""Returns Assessment Criteria  and Maximum Score from Assessment Plan Master.

	:param Assessment Plan: Assessment Plan
	"""
	return frappe.get_list("Course Assessment Credit", \
		fields=["course", "theory", "practical","credit","maximum_score"], filters={"parent": course_assessment_plan}, order_by= "idx")


@frappe.whitelist()
def get_result(student, course_assessment_plan):
	"""Returns Submitted Result of given student for specified Assessment Plan

	:param Student: Student
	:param Assessment Plan: Assessment Plan
	"""
	results = frappe.get_all("Course Assessment Result", filters={"student": student,
		"course_assessment_plan": course_assessment_plan, "docstatus": ("!=", 2)})
	if results:
		return frappe.get_doc("Course Assessment Result", results[0])
	else:
		return None


@frappe.whitelist()
def get_grade(grading_scale, percentage):
	"""Returns Grade based on the Grading Scale and Score.

	:param Grading Scale: Grading Scale
	:param Percentage: Score Percentage Percentage
	"""
	grading_scale_intervals = {}
	if not hasattr(frappe.local, 'grading_scale'):
		grading_scale = frappe.get_all("Grading Scale Interval", fields=["grade_code", "threshold"], filters={"parent": grading_scale})
		frappe.local.grading_scale = grading_scale
	for d in frappe.local.grading_scale:
		grading_scale_intervals.update({d.threshold:d.grade_code})
	intervals = sorted(grading_scale_intervals.keys(), key=float, reverse=True)
	for interval in intervals:
		if flt(percentage) >= interval:
			grade = grading_scale_intervals.get(interval)
			break
		else:
			grade = ""
	return grade


@frappe.whitelist()
def mark_assessment_result(course_assessment_plan, scores):
	student_score = json.loads(scores)
	assessment_details = []
	assessment_result = get_assessment_result_doc(student_score["student"], course_assessment_plan)
	for criteria in student_score.get("assessment_details"):
		row={
			"course": criteria,
			"theory_obtained_marks": flt(student_score["assessment_details"][criteria][criteria+"-theory"]),
			"practical_obtained_marks":flt(student_score["assessment_details"][criteria][criteria+"-practical"]),
			"score":flt(student_score["assessment_details"][criteria][criteria+"-theory"])+flt(student_score["assessment_details"][criteria][criteria+"-practical"])
		}
		for itm in assessment_result.get("assessment_result_item"):
			if itm.course==criteria:
				row.update({
					"credit":itm.credit,
					"theory":itm.theory,
					"practical":itm.practical,
					"maximum_score":itm.maximum_score,
					"credit_score":row['score']*itm.credit,

				})
		assessment_details.append(row)
	
	assessment_result.update({
		"student": student_score.get("student"),
		"course_assessment_plan": course_assessment_plan,
		"comment": student_score.get("comment"),
		"total_score":student_score.get("total_score"),
		"assessment_result_item": assessment_details,
		"exam_declaration":student_score.get("exam_declaration"),
		"assessment_plan":student_score.get("exam_assessment_plan")
	})
	assessment_result.save()
	assessment_result_item = {}
	# for d in assessment_result.assessment_result_item:
	# 	assessment_result_item.update({d.assessment_criteria: d.grade})
	assessment_result_dict = {
		"name": assessment_result.name,
		"student": assessment_result.student,
		"total_score": assessment_result.total_score,
		"grade": assessment_result.grade,
		"assessment_result_item": assessment_result_item
	}
	return assessment_result_dict

@frappe.whitelist()
def submit_assessment_results(course_assessment_plan, student_group):
	total_result = 0
	student_list = get_student_group_students(student_group)
	for i, student in enumerate(student_list):
		doc = get_result(student.student, course_assessment_plan)
		if doc and doc.docstatus==0:
			total_result += 1
			doc.submit()
	return total_result

def get_assessment_result_doc(student, course_assessment_plan):
	assessment_result = frappe.get_all("Course Assessment Result", filters={"student": student,
			"course_assessment_plan": course_assessment_plan, "docstatus": ("!=", 2)})
	if assessment_result:
		doc = frappe.get_doc("Course Assessment Result", assessment_result[0])
		if doc.docstatus == 0:
			return doc
		elif doc.docstatus == 1:
			frappe.msgprint(_("Result already Submitted"))
			return None
	else:
		return frappe.new_doc("Course Assessment Result")


@frappe.whitelist()
def update_email_group(doctype, name):
	if not frappe.db.exists("Email Group", name):
		email_group = frappe.new_doc("Email Group")
		email_group.title = name
		email_group.save()
	email_list = []
	students = []
	if doctype == "Student Group":
		students = get_student_group_students(name)
	for stud in students:
		for guard in get_student_guardians(stud.student):
			email = frappe.db.get_value("Guardian", guard.guardian, "email_address")
			if email:
				email_list.append(email)
	add_subscribers(name, email_list)

@frappe.whitelist()
def get_current_enrollment(student, academic_year=None):
	current_academic_year = academic_year or frappe.defaults.get_defaults().academic_year
	program_enrollment_list = frappe.db.sql('''
		select
			name as program_enrollment, student_name, program, student_batch_name as student_batch,
			student_category, academic_term, academic_year
		from
			`tabProgram Enrollment`
		where
			dostatus =1 and student = %s and academic_year = %s
		order by creation''', (student, current_academic_year), as_dict=1)

	if program_enrollment_list:
		return program_enrollment_list[0]
	else:
		return None

def get_total_marks(course,criteria):
	for data in frappe.get_all("Credit distribution List",{"parent":course,"assessment_criteria":criteria},["credits","total_marks"]):
		return data


@frappe.whitelist()
def make_course_assessment(course_assessment):
	result=json.loads(course_assessment)
	if result.get('rows'):
		list_student=[]
		already_record=[]
		for d in result.get('rows'):
			if not frappe.db.count("Course Assessment",{"docstatus":("!=",2),"student":result.get('rows')[d].get("student_no"),"academic_year":result.get("academic_year"),"academic_term":result.get("academic_term"),'course':result.get("course"),"assessment_criteria":result.get("criteria")}):
				doc=frappe.new_doc("Course Assessment")
				doc.student=result.get('rows')[d].get("student_no")
				doc.roll_no=result.get('rows')[d].get("roll_no")
				doc.registration_number=result.get('rows')[d].get("registration_number")
				doc.student_name=result.get('rows')[d].get("student_name")
				doc.academic_year=result.get("academic_year")
				doc.academic_term=result.get("academic_term")
				doc.program_grade=result.get("program_grade")
				doc.programs=result.get('rows')[d].get("programs")
				doc.semester=result.get('rows')[d].get("semester")
				doc.assessment_criteria=result.get("criteria")
				doc.course=result.get("course")
				doc.exam_declaration=result.get("exam_declaration")
				doc.assessment_plan=result.get("exam_assessment_plan")
				doc.earned_marks=result.get('rows')[d].get("earned_marks")
				doc.total_marks=result.get('rows')[d].get("total_marks")
				doc.attendence_status=result.get('rows')[d].get("attendance")
				doc.save()
				list_student.append(result.get('rows')[d].get("student_no"))
			else:
				already_record.append(result.get('rows')[d].get("student_no"))	
		if 	list_student:	
			frappe.msgprint("Records Created <b><i>%s</i></b>"%(list_student))
		if 	already_record:
			frappe.msgprint("Already Records Created <b><i>%s</i></b>"%(already_record))

@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
	courses=get_courses_by_semester(filters.get("semester"))
	if courses:
		return frappe.db.sql("""select name,course_name,course_code from tabCourse
		where year_end_date>=now() and name in ({0}) and (name LIKE %s or course_name LIKE %s or course_code LIKE %s)
		limit %s, %s""".format(", ".join(['%s']*len(courses))),
		tuple(courses + ["%%%s%%" % txt, "%%%s%%" % txt,"%%%s%%" % txt, start, page_len]))
	return []
		
@frappe.whitelist()
def get_assessment_criteria_list(doctype, txt, searchfield, start, page_len, filters):
	return frappe.get_all("Credit distribution List",{"parent":filters.get("course")},['assessment_criteria'],as_list = 1)


@frappe.whitelist()
def get_semester_and_exam_assessment_plan(declaration_id=None):
	result={}
	if declaration_id:
		sem_date=frappe.get_all("Examination Semester",{"parent":declaration_id},['semester'])
		result['semester']=sem_date[0]['semester']
	return result
