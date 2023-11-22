# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	columns, data = [], []
	hostel_data=get_data(filters)
	columns=get_columns()
	return columns, data


def get_data(filters):
	print("\n\n\n")
	print("ok")
	return []

def get_columns():
	columns = [
		{
			"label": _("Course"),
			"fieldname": "course",
			"fieldtype": "Data",
			"width":200
		},
		
	]
	return columns
