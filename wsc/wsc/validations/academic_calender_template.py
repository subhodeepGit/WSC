import frappe
from wsc.wsc.validations.course import validate_semester

def validate(doc, method):
	validate_semester(doc)


