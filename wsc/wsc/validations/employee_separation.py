
import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_separation_reporting_authority_mail,employee_separation_department_head_mail,employee_separation_director_mail,employee_separation_hr_mail

def validate(self,method):
	if self.workflow_state=="Pending Approval from Reporting Authority":
		employee_separation_reporting_authority_mail(self)
	if self.workflow_state=="Pending Approval from Department Head":
		employee_separation_department_head_mail(self)
	if self.workflow_state=="Approved":
		employee_separation_hr_mail(self)
	if self.workflow_state=="Sent For Approval":
		employee_separation_director_mail(self)

@frappe.whitelist()
def is_verified_user(docname):
	doc = frappe.get_doc("Employee Separation",docname)
	reporting_auth_id = doc.reporting_authority
	department_head=doc.department_head
	roles = frappe.get_roles(frappe.session.user)
	if "HR Manager/CS Officer" in roles or "HR Admin" in roles or "Director" in roles or "Admin" in roles or "Administrator" in roles or "Department Head" in roles:
		return True
	if doc.workflow_state=="Draft" and roles=="HR Admin":
		return True
	if doc.workflow_state == "Pending Approval from Reporting Authority" and frappe.session.user ==reporting_auth_id:
		return True
	if doc.workflow_state == "Pending Approval from Department Head" and frappe.session.user ==department_head:
		return True	
	if doc.workflow_state == "Sent For Approval" and roles=="Director":
		return True	    
	else :
		return False	

@frappe.whitelist()
def depart_head(department):
	dept = frappe.get_all('Department', {'name': department}, ['department_head'])
	if dept:
		department_head = dept[0].get('department_head')
		return department_head
	else:
		return None
