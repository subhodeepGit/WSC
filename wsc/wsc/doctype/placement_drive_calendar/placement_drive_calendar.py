# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PlacementDriveCalendar(Document):
	pass

@frappe.whitelist()
def get_round_placement_event(date, time, filters=None):
	"""Returns events for Course Schedule Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions

	conditions = get_event_conditions("Placement Tool", filters)

	data = frappe.db.sql(
		"""select company_name, round_of_placement, color,
			timestamp(schedule_date, from_time) as from_time,
			room, student_group, 0 as 'allDay'
		from `tabCourse Schedule`
		where ( schedule_date between %(start)s and %(end)s )
		{conditions}""".format(
			conditions=conditions
		),
		# {"start": start, "end": end},
		{"start": date, "end": time},
		as_dict=True,
		update={"allDay": 0},
	)

	return data