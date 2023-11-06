# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ToTParticipant(Document):
    def validate(self):
        aadhar_number_validation(self)
        pin_code_validation(self)
        phone_no_vlaidation(self)    
        self.participant_name = " ".join(
        filter(None, [self.first_name, self.middle_name, self.last_name])
        )
        if self.pincode:
            if len(self.pincode)<6:
                frappe.throw("<b>Pincode</b> must be 6 Digits")
            
        
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
        if len(self.adhaar_number)>16:
            frappe.throw("Field <b>Adhaar Number</b> must be 16 Digits")
        if len(self.adhaar_number)<16:
            frappe.throw("Field <b>Adhaar Number</b> must be 16 Digits")   

def pin_code_validation(self):

    if self.pincode:
        if not (self.pincode).isdigit():
            frappe.throw("Field <b>Pincode</b> Accept Digits Only")
        if len(self.pincode)>6:
            frappe.throw("Field <b>Pincode</b> must be 6 Digits")
        if len(self.pincode)<6:
            frappe.throw("Field <b>Pincode</b> must be 6 Digits")  