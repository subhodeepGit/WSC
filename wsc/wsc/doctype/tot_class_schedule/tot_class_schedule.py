# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from frappe import _

class ToTClassSchedule(Document):
	def validate(self):
		data=frappe.get_all("ToT Class Schedule",{"name":self.name})
		if data:
			doc_before_save = self.get_doc_before_save()
			old_object=doc_before_save.is_canceled
			if old_object!=0 and self.attendance_taken!=1:
				frappe.throw("<b>Attendance is already taken! Classes cannot be rescheduled or cancelled.</b>")
			elif self.attendance_taken==1:
				frappe.throw("<b>Attendance is already taken! Classes cannot be rescheduled or cancelled.</b>")
		if self.re_scheduled==1 and self.is_canceled==0:
			frappe.msgprint("Class:-%s is Re Scheduled "%(self.name))
		elif self.is_canceled==1:
			frappe.msgprint("Class:-%s is canceled"%(self.name))


		data=frappe.get_all("ToT Class Schedule",{"name":self.name})
		if data:
			doc_before_save = self.get_doc_before_save()
			old_object=doc_before_save.is_canceled
			if old_object==1:
				frappe.throw("Class Is Already Cancelled.Please Create New Class.")



		if self.is_canceled==0:
			validate_overlap(self)

		self.validate_date()

	def validate_date(self):
		academic_year, academic_term = frappe.db.get_value("Participant Group", self.participant_group_id, ["academic_year", "academic_term"])
		self.scheduled_date = frappe.utils.getdate(self.scheduled_date)

		if academic_term:
			start_date, end_date = frappe.db.get_value("Academic Term", academic_term, ["term_start_date", "term_end_date"])
			if start_date and end_date and (self.scheduled_date < start_date or self.scheduled_date > end_date):
				frappe.throw(_("Schedule date selected does not lie within the Academic Term of the Student Group {0}.").format(self.participant_group_id))

		elif academic_year:
			start_date, end_date = frappe.db.get_value("Academic Year", academic_year, ["year_start_date", "year_end_date"])
			if self.scheduled_date < start_date or self.scheduled_date > end_date:
				frappe.throw(_("Schedule date selected does not lie within the Academic Year of the Student Group {0}.").format(self.participant_group_id))
			

def validate_overlap(self):
	# Validate overlapping course schedules.
	if self.participant_group_id :
		# validate_overlap_for(self, "Course Schedule", "student_group")
		validate_overlap_for(self, "ToT Class Schedule", "participant_group_id")
		

	# validate_overlap_for(self, "Course Schedule", "instructor")
	validate_overlap_for(self, "ToT Class Schedule", "trainers")
	validate_overlap_for(self, "ToT Class Schedule", "room_name")



def validate_overlap_for(doc, doctype, fieldname, value=None):
	"""Checks overlap for specified field.

	:param fieldname: Checks Overlap for this field
	"""
	existing = get_overlap_for(doc, doctype, fieldname, value)
	if existing:
		frappe.throw(
			("This {0} conflicts with {1} for {2} {3}").format(
				doc.doctype,
				existing.name,
				doc.meta.get_label(fieldname) if not value else fieldname,
				value or doc.get(fieldname),
			),
		)	



def get_overlap_for(doc, doctype, fieldname, value=None):
	"""Returns overlaping document for specified field.

	:param fieldname: Checks Overlap for this field
	"""
	existing = frappe.db.sql(
		"""select name, from_time, to_time from `tab{0}`
		where `{1}`=%(val)s and scheduled_date = %(scheduled_date)s and
		(
			(from_time > %(from_time)s and from_time < %(to_time)s) or
			(to_time > %(from_time)s and to_time < %(to_time)s) or
			(%(from_time)s > from_time and %(from_time)s < to_time) or
			(%(from_time)s = from_time and %(to_time)s = to_time))
		and name!=%(name)s and docstatus!=2 and is_canceled!=1 """.format(
			doctype, fieldname
		),
		{
			"scheduled_date": doc.scheduled_date,
			"val": value or doc.get(fieldname),
			"from_time": doc.from_time,
			"to_time": doc.to_time,
			"name": doc.name or "No Name",
		},
		as_dict=True,
	)
	return existing[0] if existing else None

@frappe.whitelist()
def get_instructor(doctype, txt, searchfield, start, page_len, filters):
	instructor=[]
	lst = []
	fltr={"academic_year":filters["academic_year"],"programs":filters["course"],"program":filters['semester']}
	instructor_data=frappe.get_all("Instructor Log",filters=fltr,fields=['parent'],order_by="parent")
	for t in instructor_data:
		a=[]
		a.append(t['parent'])
		a=tuple(a)
		lst.append(a)
	lst=tuple(lst)
	instructor=lst
	return instructor

@frappe.whitelist()
def get_class_schedule_calendar(start, end, filters=None):
	from frappe.desk.calendar import get_event_conditions

	conditions = get_event_conditions("ToT Class Schedule", filters)

	data = frappe.db.sql(
		"""select name, participant_group_id,
			timestamp(scheduled_date, from_time) as from_time,
			timestamp(scheduled_date, to_time) as to_time,
			CONCAT(course_name, ' (', course_id, ')') as course,
			is_canceled, participant_group_name, 0 as 'allDay'
		from `tabToT Class Schedule`
		where ( scheduled_date between %(start)s and %(end)s )
		AND is_canceled = 0
		{conditions}""".format(
			conditions=conditions
		),
		{"start": start, "end": end},
		as_dict=True,
		update={"allDay": 0},
	)

	return data