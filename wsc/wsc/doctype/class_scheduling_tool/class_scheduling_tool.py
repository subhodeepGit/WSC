# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import calendar
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, getdate
from education.education.utils import OverlapError
from dateutil import parser
from wsc.wsc.utils import duplicate_row_validation

class ClassSchedulingTool(Document):
	def validate(self):
		duplicate_row_validation(self, "additional_trainer", ['instructor'])

	@frappe.whitelist()
	def schedule_course(self, days):
		"""Creates course schedules as per specified parameters"""

		course_schedules = []
		course_schedules_errors = []
		rescheduled = []
		reschedule_errors = []

		self.validate_mandatory(days)
		self.validate_date()
		self.instructor_name = frappe.db.get_value(
			"Instructor", self.instructor, "instructor_name"
		)

		group_based_on, course = frappe.db.get_value(
			"Student Group", self.student_group, ["group_based_on", "course"]
		)

		if group_based_on == "Course":
			self.course = course

		if self.reschedule:
			rescheduled, reschedule_errors = self.delete_course_schedule(
				rescheduled, reschedule_errors, days
			)

		date = self.course_start_date
		while date < self.course_end_date:
			if calendar.day_name[getdate(date).weekday()] in days:
				course_schedule = self.make_course_schedule(date)
				try:
					course_schedule.save()
				except OverlapError:
					course_schedules_errors.append(date)
				else:
					course_schedules.append(course_schedule)

			date = add_days(date, 1)
	   
		return dict(
			course_schedules=course_schedules,
			course_schedules_errors=course_schedules_errors,
			rescheduled=rescheduled,
			reschedule_errors=reschedule_errors,
		)
		
	def validate_mandatory(self, days):
		"""Validates all mandatory fields"""
		if not days:
			frappe.throw(_("Please select at least one day to schedule the course."))
		fields = [
			"course",
			"room",
			"instructor",
			"from_time",
			"to_time",
			"course_start_date",
			"course_end_date",
		]
		if not self.student_group:
			frappe.throw("Student Group is Mandatory") 

		for d in fields:
			if not self.get(d):
				frappe.throw(_("{0} is mandatory").format(self.meta.get_label(d)))

	def validate_date(self):
		duplicate_row_validation(self, "additional_trainer", ['instructor'])
		"""Validates if Course Start Date is greater than Course End Date"""
		if self.course_start_date > self.course_end_date:
			frappe.throw(_("Course Start Date cannot be greater than Course End Date."))
		if self.course_start_date == self.course_end_date:
			frappe.throw(_("If you are scheduling the class for only one day then please do it through Class Schedule Screen"))
			"""Validates if from_time is greater than to_time"""
		if	parser.parse(str(self.from_time)) >= parser.parse(str(self.to_time)):
					frappe.throw(_("From Time cannot be greater than or equal to To Time."))

	def delete_course_schedule(self, rescheduled, reschedule_errors, days):
		"""Delete all class schedule within the Date range and specified filters"""
		schedules = frappe.get_list(
			"Course Schedule",
			fields=["name", "schedule_date"],
			filters=[
				["student_group", "=", self.student_group],
				["course", "=", self.course],
				["schedule_date", ">=", self.course_start_date],
				["schedule_date", "<=", self.course_end_date],
			],
		)

		for d in schedules:
			try:
				if calendar.day_name[getdate(d.schedule_date).weekday()] in days:
					frappe.delete_doc("Course Schedule", d.name)
					rescheduled.append(d.name)
			except Exception:
				reschedule_errors.append(d.name)
		return rescheduled, reschedule_errors

	def make_course_schedule(self, date):
		"""Makes a new Course Schedule.
		:param date: Date on which Course Schedule will be created."""
		course_schedule = frappe.new_doc("Course Schedule")
		course_schedule.student_group = self.student_group
		course_schedule.course = self.course
		course_schedule.instructor = self.instructor
		course_schedule.instructor_name = self.instructor_name
		course_schedule.additional_trainer_1 = self.additional_trainer_1
		course_schedule.additional_trainer_1_name = self.additional_trainer_1_name
		course_schedule.additional_trainer_2 = self.additional_trainer_2
		course_schedule.additional_trainer_2_name = self.additional_trainer_2_name
		course_schedule.room = self.room
		course_schedule.academic_year=self.academic_year
		course_schedule.academic_term=self.academic_term
		course_schedule.school_house = self.school_house
		course_schedule.schedule_date = date
		course_schedule.from_time = self.from_time
		course_schedule.to_time = self.to_time
		##previous code for additional instructor##
		# if self.get("additional_instructor"):
		#     for ai in (self.get("additional_instructor")):
		#         course_schedule.append("additional_instructor",ai)
		# return course_schedule
		##end##
		for c in self.additional_trainer:
				create_course_row(course_schedule,c.instructor,c.instructor_name)
		return course_schedule
		  
def create_course_row(course_schedule,instructor,instructor_name):
	course_schedule.append("additional_instructor",{
		"instructor":instructor,
		"instructor_name":instructor_name
	})

@frappe.whitelist()
def get_instructor(doctype, txt, searchfield, start, page_len, filters):
	fltr={"course":filters.get("course"),"school_house":filters.get("school_house")}
	lst = []
	if txt:
		fltr.update({"parent":['like', '%{}%'.format(txt)]})
	for i in frappe.get_all("Instructor Log",fltr,['parent']):
		if i.parent not in lst :
			lst.append(i.parent)
	return [(d, ) for d in lst]


@frappe.whitelist()
def get_course(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
							Select 
									enroll_cr.course,
									enroll_cr.course_name
							from `tabProgram Enrollment` enroll
							left join `tabProgram Enrollment Course` enroll_cr on enroll.name=enroll_cr.parent 
							where enroll.program='{0}' and enroll.docstatus=1  and (enroll_cr.course LIKE %(txt)s or enroll_cr.course_name LIKE %(txt)s) 
							GROUP BY enroll_cr.course
						""".format(filters.get("program")),dict(txt="%{}%".format(txt)))    
@ frappe.whitelist()
def get_trainer_list(instructor):
	for d in frappe.get_all("Instructor",{"name":instructor},['name','instructor_name']):
		return d
	return {"no_record_found":1}

@ frappe.whitelist()
def get_student_group(doctype, txt, searchfield, start, page_len,filters):
	# searchfields = frappe.get_meta(doctype).get_search_fields()
	# searchfields = " or ".join("STU."+field + " like %(txt)s" for field in searchfields)
	program=filters.get('program')
	course=filters.get('course')
	academic_term=filters.get('academic_term')
	school_house=filters.get('school_house')
 

	student_details = frappe.db.sql("""SELECT name FROM 
				 			`tabStudent Group`   WHERE group_based_on="Course" and 
				 			school_house='{school_house}' and academic_term='{academic_term}' and program='{program}' and course='{course}'
				 							""".format(
												**{
												# "key": searchfield,
												# "scond": searchfields,
												"program":program,
												"course":course,
												"academic_term":academic_term,
												"school_house":school_house,
											}))
	
	return student_details