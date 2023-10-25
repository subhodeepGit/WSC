# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
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
    student_id=filters.get('student_id')

    filter=[]
    if student_id:
        filter.append(["student_no", "=", student_id])

    data = frappe.get_all("Selection Round", filters=filter, fields=['name','student_no', 'student_name', 'company_name', 'round_of_placement'])
    
    return data


def get_columns(filters=None):
    columns = [
        {
            "label": _("Student No"),
            "fieldname": "student_no",
            "fieldtype": "Link",
            "options": "Student",
            "width":180
        },
        {
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width":160
        },
        {
            "label": _("Student Name"),
            "fieldname": "student_name",
            "fieldtype": "Data",
            "width":160 
        },
         {
            "label": _("Company Name"),
            "fieldname": "company_name",
            "fieldtype": "Data",
            "width":160 
        },
         {
            "label": _("Placement Round"),
            "fieldname": "round_of_placement",
            "fieldtype": "Data",
            "width":160 
        }
    ]
    return columns