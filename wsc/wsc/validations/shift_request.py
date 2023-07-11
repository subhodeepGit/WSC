
import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_shift_reporting_aprover,employee_shift_approver,shift_req_hr
def validate(self,method):
	if self.workflow_state=="Pending Approval from Reporting Authority":
		employee_shift_reporting_aprover(self)
	if self.workflow_state=="Sent For Approval":
		employee_shift_approver(self)	
	if self.workflow_state=="Approved" or self.workflow_state=="Rejected":
		shift_req_hr(self)

def after_insert(doc,method):
	set_user_permission(doc)

def set_user_permission(doc):
	if doc.reporting_authority:
		set_shift_request_permission_reporting_authority(doc, doc.reporting_authority)
	if doc.approver:
		set_shift_request_permission_approver(doc, doc.approver)
	
def on_trash(self):
	self.delete_permission()
	
def delete_permission(self):
	for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
		frappe.delete_doc("User Permission",d.name)

def set_shift_request_permission_reporting_authority(doc,reporting_authority):
	for emp in frappe.get_all("Employee", {'reporting_authority_email':reporting_authority}, ['reporting_authority_email']):
		if emp.get('reporting_authority_email'):
			print(emp.get('reporting_authority_email'))
			add_user_permission("Shift Request",doc.name, emp.get('reporting_authority_email'), doc)
		else:
			frappe.msgprint("Reporting Authority Not Found")


def set_shift_request_permission_approver(doc,approver):
	for emp in frappe.get_all("Employee", {'shift_request_approver':approver}, ['shift_request_approver']):
		if emp.get('shift_request_approver'):
			print(emp.get('shift_request_approver'))
			add_user_permission("Shift Request",doc.name, emp.get('shift_request_approver'), doc)
		else:
			frappe.msgprint("Shift Request Not Found")

@frappe.whitelist()
def get_hr_mail():
	hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
	if hr_mail:
		hr_mail = hr_mail[0]
		print(hr_mail)
		return hr_mail			