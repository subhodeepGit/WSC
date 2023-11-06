import frappe
import re

def validate(self, method):
    if is_valid_field(self):
        pass
    else:
        frappe.throw("Supplier email can only contain Alphabets and Numbers")

def is_valid_field(self):
    field_pattern = r'^[a-zA-Z0-9]{15}$'
    
    if re.match(field_pattern, self.gstin):
        return True
    else:
        return False