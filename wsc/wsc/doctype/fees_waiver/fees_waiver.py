# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class FeesWaiver(Document):
	def validate(self):
		existing_data=frappe.get_all("Fees Waiver",filters={"student":self.student,"fee_type":self.fee_type,"programs":self.programs,"semester":self.semester,"academic_year":self.academic_year,"academic_term":self.academic_term,"docstatus":1},fields=["name"])
		if existing_data:
			frappe.throw(_("Fees Waiver already exists {0}").format(frappe.bold(existing_data[0]["name"])))


@frappe.whitelist()
def get_fee_components(fee_structure=None):
	fees=[]
	if fee_structure:
		if frappe.get_all("Fee Structure",{"name":fee_structure, "docstatus":1}):
			fees = frappe.get_all("Fee Component", fields=["fees_category", "description", "amount","receivable_account",
														"income_account","grand_fee_amount","outstanding_fees","waiver_type","percentage","waiver_amount",
														"total_waiver_amount"] , 
													filters={"parent": fee_structure}, order_by= "idx asc")

	return fees
