# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UserPermissionformultipleEmployee(Document):
	def validate(self):
		if self.is_new():
			data=frappe.get_all("User Permission for multiple Employee",{"employee":self.employee})
			if data:
				frappe.throw("Already Record is Present For The Employee")

		# validation_child(self)

		if self.disable==0:
			permission_given(self)
		else:
			permission_withdrawal(self)
	def on_trash(self):
		deletion_permission(self)

def permission_given(self):
	############ del of user permission
	deletion_permission(self)
	################
	doctype="Employee"
	user=self.user_id
	ignore_permissions=False
	applicable_for=None
	is_default=0
	hide_descendants=0
	apply_to_all_doctypes=1
	for t in self.get("employees"):
		name=t.employee
		frappe.get_doc(dict(
			doctype='User Permission',
			user=user,
			allow=doctype,
			for_value=name,
			is_default=is_default,
			applicable_for=applicable_for,
			hide_descendants=hide_descendants,
			apply_to_all_doctypes = apply_to_all_doctypes
		)).insert(ignore_permissions=ignore_permissions)

def permission_withdrawal(self):
	deletion_permission(self)


def deletion_permission(self):
	doctype="Employee"
	user_permission_data=frappe.get_all("User Permission",filters=[["allow",'=',doctype],["user",'=',self.user_id]],fields=['name','allow','for_value'])
	if user_permission_data:
		for t in user_permission_data:
			if t['for_value']!=self.employee:
				frappe.delete_doc("User Permission",t['name'])

def validation_child(self):
	emp=self.employee
	for t in self.get("employees"):
		if t.employee==emp:
			frappe.throw("Repoting Employee Can't be Assigning Employee")			

