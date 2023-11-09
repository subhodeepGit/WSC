import frappe

def validate(self, method):
      check_phone(self)
      check_pin(self)

def check_phone(self):
    if self.phone_no:
        if not (self.phone_no).isdigit():
            frappe.throw("Field <b>Phone Number</b> Accept Digits Only")
        if len(self.phone_no)>10:
                frappe.throw("Field <b>Phone Number</b> must be 10 Digits")
        if len(self.phone_no)<10:
                frappe.throw("Field <b>Phone Number</b> must be 10 Digits")
    
    if self.mobile_no:
        if not (self.mobile_no).isdigit():
            frappe.throw("Field <b>Mobile Number</b> Accept Digits Only")
        if len(self.mobile_no)>10:
                frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")
        if len(self.mobile_no)<10:
                frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")

def check_pin(self):
    if self.pin:
        if not (self.pin).isdigit():
            frappe.throw("Field <b>Pin code</b> Accept Digits Only")
        if len(self.pin)>6:
                frappe.throw("Field <b>Pin code</b> must be 10 Digits")
        if len(self.pin)<6:
                frappe.throw("Field <b>Pin code</b> must be 10 Digits")

