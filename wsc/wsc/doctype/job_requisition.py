import frappe
from frappe import _
from frappe.utils import getdate, today

def validate(self,method):
	if self.no_of_positions:
		if self.no_of_positions<0:
			print("Heloo")
			frappe.throw("Enter valid value for No.of Positions")
	if self.expected_compensation:
		if self.expected_compensation<=0:
			frappe.throw("Enter valid value for Expected Compensation")
	if self.expected_by < self.posting_date:
		frappe.throw("Expected date cannot be earlier than the posting date.")
	# if self.completed_on < self.posting_date:
	# 	frappe.throw("Completed On cannot be earlier than the posting date.")
	if self.posting_date:
		if (self.posting_date) < today():
			frappe.throw("Posting Date cannot be a past date.")