import frappe

def validate(self, method):
      check_phone(self)
      check_pin(self)

def check_phone(self):
    if self.contact_number:
        if not (self.contact_number).isdigit():
            frappe.throw("Field <b>Phone Number</b> Accept Digits Only")
    if len(self.contact_number)>11:
            frappe.throw("Field <b>Phone Number</b> must be 10 Digits")
    if len(self.contact_number)<11:
            frappe.throw("Field <b>Phone Number</b> must be 10 Digits")

def check_pin(self):
    if self.pin:
        if not (self.pin).isdigit():
            frappe.throw("Field <b>Pin code</b> Accept Digits Only")
    if len(self.pin)>6:
            frappe.throw("Field <b>Pin code</b> must be 10 Digits")
    if len(self.pin)<6:
            frappe.throw("Field <b>Pin code</b> must be 10 Digits")

