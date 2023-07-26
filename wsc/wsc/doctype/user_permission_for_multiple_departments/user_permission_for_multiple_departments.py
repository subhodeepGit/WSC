# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.permissions import (
	add_user_permission,
	remove_user_permission,
)

class UserPermissionformultipleDepartments(Document):
	def validate(self):
		emp_email = self.user_id
		if self.disable==1:
			filter=[]
			filter.append(["user","=",emp_email])
			filter.append(["allow","=","Department"])
			dep_info=frappe.get_all("User Permission",filters=filter,fields=["name"])
			for t in dep_info:
				frappe.delete_doc("User Permission", t['name'])
		if emp_email :
			if self.disable==0:

				filter=[]
				filter.append(["user","=",emp_email])
				filter.append(["allow","=","Department"])
				dep_info=frappe.get_all("User Permission",filters=filter,fields=["name"])
				for t in dep_info:
					frappe.delete_doc("User Permission", t['name'])
				parent_dept=[]
				dept_info=[]

				for t in self.get("departments"):
					parent_dept.append(t.parent_department)
					dept_info.append(t.department)
				parent_dept=list(set(parent_dept))
				dept_info=list(set(dept_info))
				###### for parent dept
				for t in parent_dept:
					frappe.get_doc(
						dict(
							doctype="User Permission",
							user=emp_email,
							allow="Department",
							for_value=t,
							apply_to_all_doctypes=1,
							hide_descendants=1,
						)
					).insert(ignore_permissions=False)
				######## for clild
				for t in dept_info:
					frappe.get_doc(
									dict(
										doctype="User Permission",
										user=emp_email,
										allow="Department",
										for_value=t,
										apply_to_all_doctypes=1,
										hide_descendants=0,
									)
								).insert(ignore_permissions=False)
		else:
			frappe.throw("Email id not found")