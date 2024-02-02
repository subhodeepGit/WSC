import frappe
import re

def validate(self, method):
    validate_email(self)
    if self.gstin:
        if is_valid_field(self):
            pass
        else:
            frappe.throw("Please Enter a valid GST number")

def is_valid_field(self):
    field_pattern = r'^[a-zA-Z0-9]{15}$'
    
    if re.match(field_pattern, self.gstin):
        return True
    else:
        return False
    

def validate_email(self):
    if self.supplier_email_id:
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.supplier_email_id):
            frappe.throw("<b>{0}</b> is invalid email address. Please enter a valid email address.".format(self.supplier_email_id))