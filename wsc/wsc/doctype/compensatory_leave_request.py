import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_comp_reporting_authority_email,employee_comp_leave_approver_email,employee_comp_hr_email,employee_comp_employee_email
def validate(self,method):	
	if self.workflow_state=="Pending Approval from Reporting Authority":
		employee_comp_reporting_authority_email(self)
	if self.workflow_state=="Sent For Approval":
		employee_comp_leave_approver_email(self)	
	if self.workflow_state=="Approved" or self.workflow_state=="Rejected":
		employee_comp_hr_email(self)
		employee_comp_employee_email(self)

def on_change(doc,method):
	set_user_permission(doc)

def set_user_permission(doc):
	if doc.reporting_authority_email:
		set_shift_request_permission_reporting_authority(doc, doc.reporting_authority_email)
	if doc.leave_approver:
		set_shift_request_permission_approver(doc, doc.leave_approver)
	
def on_trash(self):
	self.delete_permission()
	
def delete_permission(self):
	for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
		frappe.delete_doc("User Permission",d.name)

def set_shift_request_permission_reporting_authority(doc,reporting_authority_email):
	for emp in frappe.get_all("Employee", {'reporting_authority_email':reporting_authority_email}, ['reporting_authority_email']):
		if emp.get('reporting_authority_email'):
			print(emp.get('reporting_authority_email'))
			add_user_permission("Compensatory Leave Request",doc.name, emp.get('reporting_authority_email'), doc)
		else:
			frappe.msgprint("Reporting Authority Not Found")


def set_shift_request_permission_approver(doc,leave_approver):
	for emp in frappe.get_all("Employee", {'leave_approver':leave_approver}, ['leave_approver']):
		if emp.get('leave_approver'):
			print(emp.get('leave_approver'))
			add_user_permission("Compensatory Leave Request",doc.name, emp.get('leave_approver'), doc)
		else:
			frappe.msgprint("Leave Approver Not Found")
@frappe.whitelist()
def is_verified_user(docname):
	doc = frappe.get_doc("Compensatory Leave Request",docname)
	reporting_auth_id = doc.reporting_authority_email
	leave_approver=doc.leave_approver
	roles = frappe.get_roles(frappe.session.user)
	if "HR Manager/CS Officer" in roles or "HR Admin" in roles or "Director" in roles or "Admin" in roles or "Administrator" in roles:
		return True
	if doc.workflow_state == "Draft": 
		return True	
	if doc.workflow_state == "Pending Approval from Reporting Authority" and frappe.session.user == reporting_auth_id:
		print("\n\n\nIM REPROTING AUTHO")
		return True
	if doc.workflow_state == "Sent For Approval" and frappe.session.user == leave_approver:
		return True	
	else :
		return False		