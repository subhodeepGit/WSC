import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils.data import nowdate
from wsc.wsc.utils import duplicate_row_validation
import frappe
from frappe import _
from frappe.utils import money_in_words
from frappe.utils.csvutils import getlink

import erpnext
from erpnext.accounts.doctype.payment_request.payment_request import make_payment_request
from erpnext.accounts.general_ledger import make_reverse_gl_entries
from erpnext.controllers.accounts_controller import AccountsController
from datetime import date, timedelta, datetime


class Fees(AccountsController):
	def set_indicator(self):
		"""Set indicator for portal"""
		if self.outstanding_amount > 0:
			self.indicator_color = "orange"
			self.indicator_title = _("Unpaid")
		else:
			self.indicator_color = "green"
			self.indicator_title = _("Paid")

	def validate(self):
		self.calculate_total()
		self.set_missing_accounts_and_fields()

		validate_amount(self)
		duplicate_row_validation(self, "components", ['fees_category', 'amount'])

	def set_missing_accounts_and_fields(self):
		if not self.company:
			self.company = frappe.defaults.get_defaults().company
		if not self.currency:
			self.currency = erpnext.get_company_currency(self.company)
		################################################################	
		if not (self.receivable_account and self.income_account and self.cost_center):
			accounts_details = frappe.get_all("Company",
				fields=["default_receivable_account", "default_income_account", "cost_center"],
				filters={"name": self.company})[0]

		if not self.receivable_account:
			self.receivable_account = accounts_details.default_receivable_account
		if not self.income_account:
			self.income_account = accounts_details.default_income_account
		################################################################	
		if not self.cost_center:
			self.cost_center = accounts_details.cost_center
		if not self.student_email:
			self.student_email = self.get_student_emails()

	def get_student_emails(self):
		student_emails = frappe.db.sql_list("""
			select g.email_address
			from `tabGuardian` g, `tabStudent Guardian` sg
			where g.name = sg.guardian and sg.parent = %s and sg.parenttype = 'Student'
			and ifnull(g.email_address, '')!=''
		""", self.student)

		student_email_id = frappe.db.get_value("Student", self.student, "student_email_id")
		if student_email_id:
			student_emails.append(student_email_id)
		if student_emails:
			return ", ".join(list(set(student_emails)))
		else:
			return None


	def calculate_total(self):
		"""Calculates total amount."""
		self.grand_total = 0
		for d in self.components:
			self.grand_total += d.amount
		self.outstanding_amount = self.grand_total
		self.grand_total_in_words = money_in_words(self.grand_total)

	def on_submit(self):
		if self.exam_application:
			ex=frappe.get_doc("Exam Application",self.exam_application)
			ex.status="Paid"
			ex.flags.ignore_validate_update_after_submit = True
			ex.submit()
		
		if self.program_enrollment and not self.programs:
			self.programs=frappe.db.get_value("Program Enrollment",self.program_enrollment,'programs')
		
		if self.is_return and self.return_against:
			return_against=frappe.get_doc("Fees",self.return_against)
			return_against.return_issued=1
			return_against.submit()

		self.make_gl_entries()

		if self.send_payment_request and self.student_email:
			pr = make_payment_request(party_type="Student", party=self.student, dt="Fees",
					dn=self.name, recipient_id=self.student_email,
					submit_doc=True, use_dummy_message=True)
			frappe.msgprint(_("Payment request {0} created").format(getlink("Payment Request", pr.name)))
		#############################	
		frappe.db.set_value("Fees", self.name, "outstanding_amount",self.outstanding_amount)
		####################################


	def on_cancel(self):
		if self.is_return and self.return_against:
			return_against=frappe.get_doc("Fees",self.return_against)
			return_against.return_issued=0
			return_against.submit()

		self.ignore_linked_doctypes = ('GL Entry', 'Stock Ledger Entry')
		make_reverse_gl_entries(voucher_type=self.doctype, voucher_no=self.name)
		# frappe.db.set(self, 'status', 'Cancelled')


	def make_gl_entries(self):
		if not self.grand_total:
			return
		####################################################################	completed
		data = frappe.get_all("Fee Component",{"parent":self.name},["fees_category","receivable_account","income_account","amount"])
		for fc in data:
			student_gl_entries =  self.get_gl_dict({
				"account": fc["receivable_account"],
				"party_type": "Student",
				"party": self.student,
				"against": fc["income_account"],
				"debit": fc["amount"],
				"debit_in_account_currency": fc["amount"],
				"against_voucher": self.name,
				"against_voucher_type": self.doctype
			}, item=self)

			fee_gl_entry = self.get_gl_dict({
				"account": fc["income_account"],
				"against": self.student,
				"credit": fc["amount"],
				"credit_in_account_currency": fc["amount"],
				"cost_center": self.cost_center
			}, item=self)
			from erpnext.accounts.general_ledger import make_gl_entries
			make_gl_entries([student_gl_entries, fee_gl_entry], cancel=(self.docstatus == 2),
				update_outstanding="Yes", merge_entries=False)
		###################################################################	

def get_fee_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified"):
	user = frappe.session.user
	student = frappe.db.sql("select name from `tabStudent` where student_email_id= %s", user)
	if student:
		return frappe. db.sql('''
			select name, program, due_date, grand_total - outstanding_amount as paid_amount,
			outstanding_amount, grand_total, currency
			from `tabFees`
			where student= %s and docstatus=1
			order by due_date asc limit {0} , {1}'''
			.format(limit_start, limit_page_length), student, as_dict = True)

def get_list_context(context=None):
	return {
		"show_sidebar": True,
		"show_search": True,
		'no_breadcrumbs': True,
		"title": _("Fees"),
		"get_list": get_fee_list,
		"row_template": "templates/includes/fee/fee_row.html"
	}

def validate_amount(doc):
	if doc.is_return:
		for cmp in doc.components:
			if cmp.amount>0:
				frappe.throw("Component <b>{0}</b> amount Must be <b>-ve</b> value".format(cmp.fees_category))
		if doc.grand_total>0:
			frappe.throw("Grand Total Must be <b>-ve</b> value")

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_fee_structures(doctype, txt, searchfield, start, page_len, filters):
	program=""
	for d in frappe.get_all("Current Educational Details",{"parent":filters.get("student")},['semesters']):
		program+=d.semesters
	return frappe.db.sql("""select name,program,student_category,academic_year from `tabFee Structure` where program IN ('{0}') and (name like '%{1}%' or program like '%{1}%' or student_category like '%{1}%' or academic_year like '%{1}%')""".format(program,txt))

@frappe.whitelist()
def get_progarms(doctype, txt, searchfield, start, page_len, filters):
	fltr = {'docstatus':1}
	if txt:
		fltr.update({"programs":txt})

	fltr.update({"student":filters.get("student")})
	data = frappe.get_all("Program Enrollment",fltr,['programs'],as_list=1)
	return data

@frappe.whitelist()
def get_sem(doctype, txt, searchfield, start, page_len, filters):
	fltr = {'docstatus':1}
	if txt:
		fltr.update({"program":txt})

	fltr.update({"student":filters.get("student")})
	data = frappe.get_all("Program Enrollment",fltr,['program'],as_list=1)
	return data 


@frappe.whitelist()
def get_term(doctype, txt, searchfield, start, page_len, filters):
	fltr = {'docstatus':1}
	if txt:
		fltr.update({"academic_term":txt})

	fltr.update({"student":filters.get("student")})
	data = frappe.get_all("Program Enrollment",fltr,['academic_term'],as_list=1)
	return data
	
@frappe.whitelist()
def get_fee_components(fee_structure):
    if fee_structure:
        fees = frappe.get_all("Fee Component", fields=["fees_category", "description", "amount","receivable_account",
                                                    "income_account","grand_fee_amount","outstanding_fees","waiver_type","percentage","waiver_amount",
                                                    "total_waiver_amount"] , 
                                                filters={"parent": fee_structure}, order_by= "idx asc")
        return fees

@frappe.whitelist()
def get_year(doctype, txt, searchfield, start, page_len, filters):
	fltr = {'docstatus':1}
	if txt:
		fltr.update({"academic_year":txt})

	fltr.update({"student":filters.get("student")})
	data = frappe.get_all("Program Enrollment",fltr,['academic_year'],as_list=1)
	return data 

@frappe.whitelist()
def get_batch(doctype, txt, searchfield, start, page_len, filters):
	fltr = {'docstatus':1}
	if txt:
		fltr.update({"student_batch_name":txt})

	fltr.update({"student":filters.get("student")})
	data = frappe.get_all("Program Enrollment",fltr,['student_batch_name'],as_list=1)
	return data 


@frappe.whitelist()
def get_student_category(doctype, txt, searchfield, start, page_len, filters):
	fltr = {}
	lst = []
	if txt:
		fltr.update({"student_category":txt})
	fltr.update({"student":filters.get("student")})
	for i in frappe.get_all("Program Enrollment",fltr,['student_category']):
		if i.student_category not in lst:
			lst.append(i.student_category)
	return [(d,) for d in lst]

@frappe.whitelist()
def get_fees_category(doctype, txt, searchfield, start, page_len, filters):
	fltr = {}
	lst = []
	if txt:
		fltr.update({"fees_category":txt})
	
	fltr.update({"parent":filters.get("fee_structure"),"parenttype":"Fee Structure"})
	for i in frappe.get_all("Fee Component",fltr,['fees_category']):
		if i.fees_category not in lst:
			lst.append(i.fees_category)
	return [(d,) for d in lst]

# @frappe.whitelist()
# def make_refund_fees(source_name, target_doc=None):
# 	def set_missing_values(source, target):
# 		target.set("components",[])
# 		for d in source.get("components"):
# 			target.append("components",{
# 					"fees_category":d.fees_category,
# 					"amount":-d.amount,
# 					"description":d.description
# 				})
# 		target.grand_total=(-source.grand_total)
# 		target.is_return=1
# 		target.return_against=source.name
# 		target.outstanding_amount=(-source.outstanding_amount)

# 	doclist = get_mapped_doc("Fees", source_name, 	{
# 		"Fees": {
# 			"doctype": "Fees",
# 		},
# 	}, target_doc, set_missing_values)

# 	return doclist

@frappe.whitelist()
def make_refund_fees(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.set("components",[])
        for d in source.get("components"):
            target.append("components",{
					"fees_category":d.fees_category,
					"amount":-d.amount,
					"description":d.description,
                    "income_account":d.income_account,
                    "receivable_account":d.receivable_account
				})
        target.grand_total=(-source.grand_total)
        target.is_return=1
        target.return_against=source.name
        target.outstanding_amount=(-source.outstanding_amount)

    doclist = get_mapped_doc("Fees", source_name, 	{
        "Fees": {
            "doctype": "Fees",
        },
    }, target_doc, set_missing_values)

    return doclist

@frappe.whitelist()
def get_fees_entry(dt,dn):
	doc = frappe.get_doc(dt, dn)
	educationdoc =frappe.get_all("Current Educational Details",
						  {"parent":dn},
						  ['programs','semesters'])
	feesEntry = frappe.new_doc("Fees")
	feesEntry.student=doc.get("student_id")
	feesEntry.posting_date = nowdate()
	feesEntry.student_name=doc.get("student_name")
	feesEntry.student_name=doc.get("student_name")
	feesEntry.programs=educationdoc[0]['programs']
	feesEntry.program=educationdoc[0]['semesters']
	feesEntry.append("components", {
		"amount":doc.get("total_dues")
	})
	return feesEntry