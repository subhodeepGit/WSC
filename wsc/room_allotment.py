from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.model
import frappe.utils
import json, os
from frappe.utils import get_safe_filters
from frappe.desk.reportview import validate_args
from frappe.model.db_query import check_parent_permission
from datetime import date

from six import iteritems, string_types, integer_types

# Pop-up message Room Allotment Data in Student doctype
@frappe.whitelist()
def get(name=None, filters=None, parent=None):
    '''Returns a document by name or filters

    :param doctype: DocType of the document to be returned
    :param name: return document of this `name`
    :param filters: If name is not set, filter by these values and return the first match'''
    room_allotment_data=frappe.get_all("Room Allotment",filters=[["student","=",name],["start_date","<=",date.today()],["end_date",">=",date.today()]],
                                        fields=['name','hostel_registration_no','hostel_id','room_number','room_id','room_type','start_date','end_date'])
    if len(room_allotment_data)!=0:
       return room_allotment_data[0]
    else:
        return {}