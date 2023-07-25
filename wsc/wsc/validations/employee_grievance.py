import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_grievance_member,employee_grievance_employee_mail
def validate(self,method):
	if self.workflow_state=="Under Review":
		employee_grievance_member(self)
	if self.workflow_state=="Resolved" or self.workflow_state=="Rejected":
		employee_grievance_employee_mail(self)    
