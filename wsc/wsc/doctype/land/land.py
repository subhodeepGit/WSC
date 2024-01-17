# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe, json,re
from frappe.model.document import Document


class Land(Document):
    def validate(self):
        dateValidate(self)
        phone(self)
        pincode(self)
        plot_number(self)
        # land_valuation(self)
        self.enabled_land()

        if self.land_size < 0:
            frappe.throw("<B>Land size</b> cannot be negative value")

        if self.land_valuation < 0:
            frappe.throw("<B> Land valuation</b> cannot be negative")

        # phone(self)

    def enabled_land(self):
        if  self.enabled==0:
            today = frappe.utils.nowdate()
            if self.end_date > today:
                frappe.throw("<b>Disabling Land in can't be in Future date</b>")
                
        land_details_info=frappe.get_all("Land Details",{"land_plot_number":self.name},["parent","parenttype","name"])
        for t in land_details_info:
            doc=frappe.get_doc(t['parenttype'],t['parent'])
            for j in doc.get("land_details"):
                if j.name==t['name']:
                    j.enabled=self.enabled
            doc.save()

# To validate if the start date is not after the end date
def dateValidate(self):
    if self.start_date > self.end_date:
        frappe.throw("Start date cannot be greater than End date")
        
# Validation for pincode length	
def pincode(self):
    if self.pin_code:	
        if  not (self.pin_code).isdigit():
            frappe.throw("Field <b>Pin Code</b> Accept Digits Only")

        if len(self.pin_code)>6:
            frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

        if len(self.pin_code)<6:	
            frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

#plot number validation
def plot_number(self):
    if self.plot_number:	
        if  not (self.plot_number).isdigit():
            frappe.throw("Field <b>Plot number</b> Accept Digits Only")

#plot phone_number validation
def phone(self):
    if self.phone:
        if  not (self.phone).isdigit():
            frappe.throw("Field <b>Phone</b> Accept Digits Only")
    
        if len(self.phone)>10:
            frappe.throw("Field <b>Phone number</b> must be 10 Digits")
        
        if len(self.phone)<10:
            frappe.throw("Field <b>Phone number</b> must be 10 Digits")

# def land_valuation(self):
#     if self.land_valuation:
#         if  not (self.land_valuation).isdigit():
#             frappe.throw("Field <b>Land Valuation</b> Accept Digits Only") 