# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

# from typing_extensions import Self
# from warnings import filters
import frappe
from frappe.utils import money_in_words
from frappe.model.document import Document
from erpnext.accounts.general_ledger import make_reverse_gl_entries
class HostelFees(Document):
	def validate(self):
		student=self.student
		hostel_admission_id = self.hostel_admission
		self.calculate_total()

	def set_indicator(self):
		"""Set indicator for portal"""
		if self.outstanding_amount > 0:
			self.indicator_color = "orange"
			self.indicator_title = ("Unpaid")
		else:
			self.indicator_color = "green"
			self.indicator_title = ("Paid")

	def on_submit(self):
		self.create_fees()

	def on_cancel(self):
		self.cancel_fees()
		
	def calculate_total(self):
		"""Calculates total amount."""
		self.grand_total = 0
		for d in self.components:
			self.grand_total += d.amount
		self.outstanding_amount = self.grand_total
		self.grand_total_in_words = money_in_words(self.grand_total)

	def create_fees(self):
		fees = frappe.new_doc("Fees")
		fees.student = self.student
		fees.valid_from = self.valid_from
		fees.valid_to = self.valid_to
		fees.due_date = self.due_date
		fees.program_enrollment = self.program_enrollment
		fees.programs = self.programs
		fees.program = self.program
		fees.student_batch = self.student_batch
		fees.academic_year = self.academic_year
		fees.academic_term = self.academic_term
		fees.hostel_fee_structure = self.hostel_fee_structure
		# fees.fee_structure = self.hostel_fee_structure
		ref_details = frappe.get_all("Fee Component",{"parent":self.hostel_fee_structure},['fees_category','amount','receivable_account','income_account','company','grand_fee_amount','outstanding_fees'],order_by="idx asc")
		for i in ref_details:
			fees.append("components",{
				'fees_category' : i['fees_category'],
				'amount' : i['amount'],
				'receivable_account' : i['receivable_account'],
				'income_account' : i['income_account'],
				'company' : i['company'],
				'grand_fee_amount' : i['grand_fee_amount'],
				'outstanding_fees' : i['outstanding_fees'],
			})
		fees.save()
		fees.submit()	
		self.fees_id = fees.name
		frappe.db.set_value("Hostel Fees",self.name,"fees_id",fees.name)

	def cancel_fees(self):
		cancel_doc = frappe.get_doc("Fees",self.fees_id)
		cancel_doc.cancel()


@frappe.whitelist()
def get_fee_components(hostel_fee_structure):
	"""Returns Fee Components.

	:param fee_structure_hostel: Fee Structure Hostel.
	"""
	if hostel_fee_structure:
		fs = frappe.get_all("Fee Component", fields=["fees_category", "description", "amount", "receivable_account", "income_account", "waiver_type", "waiver_amount", "grand_fee_amount", "outstanding_fees"] , filters={"parent": hostel_fee_structure}, order_by= "idx asc")
		return fs

@frappe.whitelist()
def hostel_admission(student):
	data=frappe.get_all("Student Hostel Admission",fields=[["student","=",student],["allotment_status","=","Allotted"],["docstatus","=",1]])
	if len(data)>0:
		return data[0]

@frappe.whitelist()
def room_allotment(hostel_admission_id):
	data=frappe.get_all("Room Allotment",fields=["name","hostel_id","room_number","room_type"],filters=[["hostel_registration_no","=",hostel_admission_id],["docstatus","=",1]])
	if len(data)>0:
		return data[0]

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_fee_structures(doctype, txt, searchfield, start, page_len, filters):
    program=""
    for d in frappe.get_all("Current Educational Details",{"parent":filters.get("student")},['semesters']):
        program+=d.semesters
    return frappe.db.sql("""select name,program,academic_year from `tabFee Structure Hostel` where program IN ('{0}') and (name like '%{1}%' or program like '%{1}%' or  academic_year like '%{1}%')""".format(program,txt))

@frappe.whitelist()
def get_allotted_students(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(" select student, name, roll_no from `tabRoom Allotment` where allotment_type='Allotted' ")
