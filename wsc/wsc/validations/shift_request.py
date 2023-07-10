
import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_shift_reporting_aprover
def validate(self,method):
	print("\n\n\n")
	print("Hello validate")
	if self.workflow_state=="Pending Approval from Reporting Authority":
		employee_shift_reporting_aprover(self)

def after_insert(doc,method):
	set_user_permission(doc)

def set_user_permission(doc):
	print("\n\n\n\nHELLO WORLD")
	if doc.reporting_authority:
		set_shift_request_permission_reporting_authority(doc, doc.reporting_authority)
	if doc.approver:
		set_shift_request_permission_approver(doc, doc.approver)
	
def on_trash(self):
	print("\n\non trash")
	self.delete_permission()
def delete_permission(self):
	print("\n\n\ndelete")
	for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
		frappe.delete_doc("User Permission",d.name)
def set_shift_request_permission_reporting_authority(doc,reporting_authority):
	# for i in frappe.get_all("Instructor",{"name":instructor},['employee']):
	#     if i.get('employee'):
	for emp in frappe.get_all("Employee", {'reporting_authority_email':reporting_authority}, ['reporting_authority_email']):
		if emp.get('reporting_authority_email'):
			print("\n\nUSER ID")
			print(emp.get('reporting_authority_email'))
			add_user_permission("Shift Request",doc.name, emp.get('reporting_authority_email'), doc)
		else:
			frappe.msgprint("Instructor  is not employee")


def set_shift_request_permission_approver(doc,approver):
	for emp in frappe.get_all("Employee", {'shift_request_approver':approver}, ['shift_request_approver']):
		if emp.get('shift_request_approver'):
			print("\n\nUSER ID")
			print(emp.get('shift_request_approver'))
			add_user_permission("Shift Request",doc.name, emp.get('shift_request_approver'), doc)
		else:
			frappe.msgprint("Instructor  is not employee")