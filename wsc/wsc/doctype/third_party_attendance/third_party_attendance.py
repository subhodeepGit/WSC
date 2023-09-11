# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import formatdate, get_link_to_form, getdate
from frappe.model.document import Document

class ThirdPartyAttendance(Document):
	def validate(self):
		attendance_record = None
		attendance_record = frappe.db.exists(
			"Third Party Attendance",
			{
				"third_party_attendance_contract": self.third_party_attendance_contract,
				"date": self.date,
				"docstatus": ("!=", 2),
				"name": ("!=", self.name),
			},
		)
		if attendance_record:
			record = get_link_to_form("Student Attendance", attendance_record)
			frappe.throw(
				_("Attendance record {0} already exists against the Date {1}").format(
					record, frappe.bold(self.date)
				),
				title=_("Duplicate Entry"),
			)
		self.validate_date()

	def validate_date(self):
		if getdate(self.date) > getdate():
			frappe.throw(_("Attendance cannot be marked for future dates."))
