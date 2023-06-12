
import frappe

@frappe.whitelist()
def isrfp(docname):
	# if frappe.db.exists(docname):

	doc = frappe.get_doc("Shift Request",docname)
	emp_user_id = frappe.get_all("Employee",{"name":doc.employee},["user_id"])
	if emp_user_id:
		employee_user_id = emp_user_id[0]["user_id"]
	reporting_auth = doc.reporting_authority
	reporting_auth_id = frappe.get_all("Employee",{"name":reporting_auth},["user_id"])
	# print("reporting_auth_id",reporting_auth_id)
	if reporting_auth_id:
		reporting_auth_id=reporting_auth_id[0]["user_id"]
	roles = frappe.get_roles(frappe.session.user)
	if "HR Manager/CS Officer" in roles  or "HR Admin" in roles or "Director" in roles:
		return True
	if "Employee" in roles and doc.workflow_state=="Draft" and frappe.session.user==employee_user_id:
		return True
	if reporting_auth_id==frappe.session.user and doc.workflow_state=="Pending Approval from Reporting Authority":
		return True
	if frappe.session.user == doc.approver and doc.workflow_state=="Pending Approval" :
		return True
	else :
		return False
	# else :
	# 	pass