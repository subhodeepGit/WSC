# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

# import frappe
from dataclasses import field
import frappe
from frappe import _
import itertools
from datetime import datetime

def execute(filters=None):
    pe_data , course_schedule_data=get_data(filters)
    get_columns_info=get_columns()
    return  get_columns_info,pe_data



def get_data(filters=None):
    pass

def get_columns():
    columns = [
        {
            "label": _("Student No"),
            "fieldname": "student",
            "fieldtype": "Link",
            "options": "Student",
            "width":180
        },
        {
            "label": _("Student Name"),
            "fieldname": "student_name",
            "fieldtype": "Data",
            "width":160
        },
    ]
    return columns