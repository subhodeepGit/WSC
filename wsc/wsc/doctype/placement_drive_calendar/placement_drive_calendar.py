# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PlacementDriveCalendar(Document):
	pass

@frappe.whitelist()
def get_round_placement_event(start, end,filters=None):
# def get_round_placement_event(date, time):
	"""Returns events for Placement Drive Calendar Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	# print(data ,time)
	conditions = get_event_conditions("Placement Drive Calendar", filters)
	data = frappe.db.sql(
			"""select name, placement_drive, 
				timestamp(reporting_date, reporting_time) as from_time,
				timestamp(reporting_date, reporting_end_time) as to_time,
				0 as 'allDay'
			from `tabPlacement Drive Calendar`
			where ( reporting_date between %(start)s and %(end)s )
			{conditions}""".format(
				conditions=conditions
			),
			{"start": start, "end": end},
			as_dict=True,
			update={"allDay": 0},
		)

	return data

	# query = """SELECT placement_company,round_of_placement,color,placement_drive  FROM `tabPlacement Drive Calendar` WHERE reporting_date = '2023-02-23' AND reporting_time = '17:08:49'"""
	# data = frappe.db.sql(query , as_dict=True)
	# print(data)
	# return data
	