# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt


from dataclasses import field
import frappe
from frappe import _
import itertools
from datetime import datetime

def execute(filters=None):
    data = get_data(filters)
    columns = get_columns(filters)
    return columns,data


def get_data(filters=None):
    to_date=filters.get('to_date')
    from_date=filters.get('from_date')
    third_party_contract=filters.get('third_party')

    try:
        if from_date > to_date:
            frappe.throw("From Date cannot be greater than To Date")
    except TypeError:
        pass

    filter=[]
    if from_date and to_date==None:
        filter.append(["date", ">=", from_date])
    elif to_date and from_date==None:
        filter.append(["date", "<=", to_date])
    elif from_date and to_date:
        filter.append(["date", "between", [from_date,to_date]])
    if third_party_contract:
        filter.append(["third_party_attendance_contract","=",third_party_contract])

    attendance_data = frappe.get_all("Third Party Attendance", filters=filter, fields=['name','third_party_attendance_contract','date','total_number_of_staff','total_number_of_staff_present','total_number_of_staff_absent'])



    return attendance_data

    
def get_columns(filters=None):
    columns = [
        {
            "label": _("Third Party Attendance Contract"),
            "fieldname": "third_party_attendance_contract",
            "fieldtype": "Data",
            "width":250
        },
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width":200
        },
        {
            "label": _("Total Number of Staff"),
            "fieldname": "total_number_of_staff",
            "fieldtype": "Data",
            "width":200
        },
        {
            "label": _("Total Number of Staff Present"),
            "fieldname": "total_number_of_staff_present",
            "fieldtype": "Int",
            "width":250
        },
        {
            "label": _("Total Number of Staff Absent"),
            "fieldname": "total_number_of_staff_absent",
            "fieldtype": "Int",
            "width":250
        },
    ]

    return columns
