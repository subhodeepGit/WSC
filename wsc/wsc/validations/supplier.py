import frappe
import re

def validate(self, method):
    validate_email(self)
    is_valid_pan(self)
    
    if self.gstin:
        if is_valid_field(self):
            pass
        else:
            frappe.throw("Please Enter a valid GST number")
    
    compare_pan_and_gst(self)

def is_valid_field(self):
    field_pattern = r'^[a-zA-Z0-9]{15}$'
    
    if re.match(field_pattern, self.gstin):
        return True
    else:
        return False
    
def is_valid_pan(self):
        pan_pattern = r'^[A-Z]{5}\d{4}[A-Z]$'

        if re.match(pan_pattern, self.pan):
            return True
        else:
            frappe.throw("Please enter a valid PAN number")


def compare_pan_and_gst(self):
    if self.gstin:
        gstin = self.gstin[2:12]

        if self.pan == gstin:
            return True
        else:
            frappe.throw("GSTIN number not matching with PAN number")

def validate_email(self):
    if self.supplier_email_id:
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.supplier_email_id):
            frappe.throw("<b>{0}</b> is invalid email address. Please enter a valid email address.".format(self.supplier_email_id))