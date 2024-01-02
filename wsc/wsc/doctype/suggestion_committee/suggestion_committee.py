# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SuggestionCommittee(Document):
    def validate(self):
        frappe.msgprint(" Please Give the Suggestion Committee Member Role to the users to Access Employee Suggestion. ")









