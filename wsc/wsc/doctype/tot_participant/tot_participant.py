# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import comma_and, get_link_to_form,get_link_to_form, getdate, formatdate
from frappe import msgprint, _
from datetime import datetime, timedelta
from frappe.utils import getdate, today

class ToTParticipant(Document):
    def validate(self):
        validate_participant_job_date(self)
        validate_date(self)
        aadhar_number_validation(self)
        pin_code_validation(self)
        phone_no_vlaidation(self)    
        validate_name(self)
        self.participant_name = " ".join(
        filter(None, [self.first_name, self.middle_name, self.last_name])
        )
        if self.pincode:
            if len(self.pincode)<6:
                frappe.throw("<b>Pincode</b> must be 6 Digits")


def validate_name(doc):
    if doc.date_of_birth and getdate(doc.date_of_birth) >= getdate(today()):
        frappe.throw(_("Date of Birth cannot be greater than today."))

    if doc.date_of_birth and getdate(doc.date_of_birth) >= getdate(doc.joining_date):
        frappe.throw(_("Date of Birth cannot be greater than Joining Date."))
    if doc.first_name:
        if not contains_only_characters(doc.first_name):
            frappe.throw("First Name should be only characters")
    if doc.middle_name:
        if not contains_only_characters(doc.middle_name):
            frappe.throw("Middle Name should be only characters")
    if doc.last_name:
        if not contains_only_characters(doc.last_name):
            frappe.throw("Last Name should be only characters")

def contains_only_characters(first_name):
	return all(char.isalpha() or char.isspace() or char == '.' for char in first_name)     


def phone_no_vlaidation(self):
    if self.participant_mobile_number:
        data=frappe.get_all("ToT Participant",{"participant_mobile_number":self.participant_mobile_number},['name'])
        if data:
            flag="No"
            for t in data:
                if self.name==t['name']:
                    flag="Yes"
            if flag=="No":        
                frappe.throw("Participant Mobile Number should be Unique")


def aadhar_number_validation(self):

    if self.adhaar_number:
        if not (self.adhaar_number).isdigit():
            frappe.throw("Field <b>Adhaar Number</b> Accept Digits Only")
        if len(self.adhaar_number)>12:
            frappe.throw("Field <b>Adhaar Number</b> must be 12 Digits")
        if len(self.adhaar_number)<12:
            frappe.throw("Field <b>Adhaar Number</b> must be 12 Digits")   

def pin_code_validation(self):

    if self.pincode:
        if not (self.pincode).isdigit():
            frappe.throw("Field <b>Pincode</b> Accept Digits Only")
        if len(self.pincode)>6:
            frappe.throw("Field <b>Pincode</b> must be 6 Digits")
        if len(self.pincode)<6:
            frappe.throw("Field <b>Pincode</b> must be 6 Digits")  

def validate_date(self):
    if getdate(self.date_of_birth) > getdate():
        frappe.throw(_('Date of Birth cannot be a future date'))

def validate_participant_job_date(self):
    for t in self.get('participant_experience_details'):
        if t.job_start_date and t.job_end_date:
            job_start_date = datetime.strptime(t.job_start_date , '%Y-%m-%d').date()
            job_end_date = datetime.strptime(t.job_end_date , '%Y-%m-%d').date()
            if job_start_date > job_end_date:
                frappe.throw("Job Start Date cannot be greater than Job End Date in Row %s of Participant Experience Details table"%(t.idx))