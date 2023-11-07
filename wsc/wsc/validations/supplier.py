import frappe
import re

def validate(self, method):
    
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