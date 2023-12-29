import frappe
import re

def validate(doc, method):
    is_valid_url(doc)
    if doc.email:
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', doc.email):
            frappe.throw("<b>{0}</b> is an invalid email address. Please enter a valid email address.".format(doc.email))
    if doc.phone_no:
        if not (doc.phone_no).isdigit():
            frappe.throw("Field <b>Phone No</b> Accept Digits Only")
        if len(doc.phone_no)<10:
            frappe.throw("Field <b>Phone No</b> must be 10 Digits")
        if len(doc.phone_no)>10:
            frappe.throw("Field <b>Phone No</b> must be 10 Digits")

def is_valid_url(doc):
    if doc.website:
        if not bool(re.match(r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$', doc.website)):
            frappe.throw("<b>{0}</b> is an invalid url address. Please enter a valid url address.".format(doc.website))