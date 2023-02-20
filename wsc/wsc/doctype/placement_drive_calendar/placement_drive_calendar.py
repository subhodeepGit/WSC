# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from time import strftime
from frappe.model.document import Document
from frappe.utils import comma_and, get_link_to_form, getdate,date_diff,add_days
class PlacementDriveCalendar(Document):
	pass

@frappe.whitelist()
def get_round_placement_event(start,end, filters=None):
# def get_round_placement_event(date, time):
	# """Returns events for Placement Drive Calendar Calendar view rendering.

	# :param start: Start date-time.
	# :param end: End date-time.
	# :param filters: Filters (JSON).
	# """
	from frappe.desk.calendar import get_event_conditions
	# print(data ,time)
	conditions = get_event_conditions("Placement Drive Calendar", filters)
	print("\n\nSTART")
	print(start)
	print("\n\nEND")
	print(end)
	data = frappe.db.sql(
			"""select placement_drive,placement_company , round_of_placement,color,location,reporting_date,
				timestamp(reporting_date, reporting_time) as from_time,
				timestamp(reporting_date, reporting_end_time) as to_time,
				0 as 'allDay'
			from `tabPlacement Drive Calendar`
			where  ( reporting_date between %(start)s and %(end)s )
			{conditions}""".format(
				conditions=conditions,
			),
			{"start": start,"end":end},
			as_dict=True,
			update={"allDay": 0},
		)

	result=[]

	for d in data:
		# from_time=d["from_time"].strftime("%H:%M:%S")
		# to_time = d["to_time"].strftime("%H:%M:%S")

		d.update({"placement_drive":d.placement_drive+"\n"+d.placement_company+"\n"+d.round_of_placement+"\n"+d.location})
		result.append(d)
	print("\n\n\n\nresult")
	print(result)
	return result

	# query = """SELECT placement_company,round_of_placement,color,placement_drive  FROM `tabPlacement Drive Calendar` WHERE reporting_date = '2023-02-23' AND reporting_time = '17:08:49'"""
	# data = frappe.db.sql(query , as_dict=True)
	# print(data)
	# return data
	