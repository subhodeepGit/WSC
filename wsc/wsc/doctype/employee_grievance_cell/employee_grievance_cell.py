# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeGrievanceCell(Document):
    def validate(self):
        self.get_employees()
    def get_employees(self):
        for member in self.grievance_committee:
            user_id = member.user_id
            if not has_role(user_id, "Grievance Cell Member"):
                frappe.throw(("User {0} does not have the role Grievance Cell Member.").format(user_id))


def has_role(user_id,role):
    roles = frappe.get_roles(user_id)
    return role in roles
