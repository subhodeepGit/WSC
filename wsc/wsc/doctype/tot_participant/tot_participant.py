# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import comma_and, get_link_to_form,get_link_to_form, getdate, formatdate
from frappe import msgprint, _
from datetime import datetime, timedelta
from frappe.utils import getdate, today
from frappe.desk.form.linked_with import get_linked_doctypes

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
        earned_marks_percentage_cal(self)
        participant = frappe.get_all("ToT Participant",{"name":self.name},{"participant_name","hrms_id"})
        if participant:
            if self.participant_name!=participant[0]['participant_name']:
                update_participant_in_linked_doctype(self)
                if self.student_no:
                    update_student_name_in_linked_doctype(self)
            if self.hrms_id!=participant[0]['hrms_id']:
                update_participant_hrms_id_in_linked_doctype(self)       

def update_student_name_in_linked_doctype(self):
    doc=frappe.get_doc("Student",self.student_no)
    doc.first_name=self.first_name 
    doc.middle_name=self.middle_name 
    doc.last_name=self.last_name
    doc.save()



def update_participant_hrms_id_in_linked_doctype(self):
    linked_doctypes = get_linked_doctypes("ToT Participant")
    for d in linked_doctypes:
        meta = frappe.get_meta(d)
        if not meta.issingle:
            if "hrms_id" in [f.fieldname for f in meta.fields]:
                if d != "ToT Participant":
                    frappe.db.sql(
                        """UPDATE `tab{0}` set hrms_id = %s where {1} = %s""".format(
                            d, linked_doctypes[d]["fieldname"][0]
                        ),
                        (self.hrms_id, self.name),
                    )

            if "child_doctype" in linked_doctypes[d].keys() and "hrms_id" in [
                f.fieldname for f in frappe.get_meta(linked_doctypes[d]["child_doctype"]).fields
            ]:
                frappe.db.sql(
                    """UPDATE `tab{0}` set hrms_id = %s where {1} = %s""".format(
                        linked_doctypes[d]["child_doctype"], linked_doctypes[d]["fieldname"][0]
                    ),
                    (self.hrms_id, self.name),
                )

def update_participant_in_linked_doctype(self):
    linked_doctypes = get_linked_doctypes("ToT Participant")
    for d in linked_doctypes:
        meta = frappe.get_meta(d)
        if not meta.issingle:
            if "participant_name" in [f.fieldname for f in meta.fields]:
                if d != "ToT Participant":
                    frappe.db.sql(
                        """UPDATE `tab{0}` set participant_name = %s where {1} = %s""".format(
                            d, linked_doctypes[d]["fieldname"][0]
                        ),
                        (self.participant_name, self.name),
                    )

            if "child_doctype" in linked_doctypes[d].keys() and "participant_name" in [
                f.fieldname for f in frappe.get_meta(linked_doctypes[d]["child_doctype"]).fields
            ]:
                frappe.db.sql(
                    """UPDATE `tab{0}` set participant_name = %s where {1} = %s""".format(
                        linked_doctypes[d]["child_doctype"], linked_doctypes[d]["fieldname"][0]
                    ),
                    (self.participant_name, self.name),
                )



def earned_marks_percentage_cal(self):
    for t in self.get("participant_education_details"):
        if t.total_marks<t.earned_marks:
            frappe.throw("Earned Marks can't greater than total marks")
        if t.total_marks and t.earned_marks:
            if t.total_marks==0:
                frappe.throw("Total Marks can't be zero")
            percentage=(t.earned_marks/t.total_marks)*100
            t.percentage=percentage


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
    today=frappe.utils.nowdate()
    for t in self.get('participant_experience_details'):
        if t.job_start_date and t.job_end_date:
            # job_start_date = datetime.strptime(t.job_start_date , '%Y-%m-%d').date()
            # job_end_date = datetime.strptime(t.job_end_date , '%Y-%m-%d').date()    
            job_start_date = t.job_start_date
            job_end_date = t.job_end_date
            if job_start_date > job_end_date:
                frappe.throw("Job Start Date cannot be greater than Job End Date in Row %s of Participant Experience Details table"%(t.idx))
            if job_end_date > today:
                frappe.throw("Job End Date cannot be greater than Present Date in Row %s of Participant Experience Details table"%(t.idx))  
