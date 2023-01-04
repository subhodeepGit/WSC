# -*- coding: utf-8 -*-
# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
# import frappe
from frappe.model.document import Document

class AcademicCalender(Document):
	pass

@frappe.whitelist()
def get_academic_events_table(academic_calendar_template):
	doc=frappe.get_doc("Academic Calendar Template",academic_calendar_template)
	return doc.get("academic_events_table") or []