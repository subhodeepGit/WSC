import frappe
from frappe import _

def validate(doc,method):
	validate_room_capacity(doc)
	
def validate_room_capacity(doc):
	
	if doc.seating_capacity:
		if len(doc.seating_capacity)>=5 :
			frappe.throw("Invalid Input for <b>Seating Capacity</b>")

	if not check_int(doc.seating_capacity):
		frappe.throw("Seating Capacity Must be an Integer.")
	
def check_int(seating_capacity):
	import re
	return re.match(r"[-+]?\d+(\.0*)?$", seating_capacity) is not None