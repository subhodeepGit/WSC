from frappe import _
import frappe
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_grievance_member,employee_grievance_employee_mail,employee_grievance_hr_mail
from datetime import datetime

def validate(self,method):
	current_date = datetime.today().date()
	if self.workflow_state == "Forwarded to HR":
		employee_grievance_hr_mail(self)
	if self.workflow_state=="Forwarded to Grievance Cell":
		employee_grievance_member(self)
	if self.workflow_state=="Resolved" or self.workflow_state=="Rejected":
		employee_grievance_employee_mail(self)    
	if self.date:
		if isinstance(self.date,str):
			datee = datetime.strptime(self.date, "%Y-%m-%d").date()
			if datee>current_date:
				frappe.throw("Date cannot be greater than the current date")
		else :


			if self.date > current_date:
				frappe.throw("Date cannot be greater than the current date")
# @frappe.whitelist()
# def get_cell(doctype, txt, searchfield, start, page_len, filters):
#     investigation_cell = frappe.get_all(
#         "Employee Grievance Cell",
#         {"grievance_type":filters.get("grievance_type")},
#         ["name"],as_list=1
#     )

#     member_names = [member for member in investigation_cell]

#     return member_names


@frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
def test_query(doctype, txt, searchfield, start, page_len, filters):
	User=frappe.session.user
	if frappe.session.user=="Administrator" or "HR Admin" or "Grievance Cell Member" or "Director" in frappe.get_roles(frappe.session.user):
		return frappe.db.sql("""
					SELECT `name` from `tabEmployee` WHERE `user_id`="%s" """ %(User))
	
@frappe.whitelist()
def get_cell_members(investigation_cell):
	investigation_cell_members = frappe.get_all(
		"Grievance Members",
		{"parent":investigation_cell},
		["employee","employee_name","user_id","designation","department"]
	)
	print("\n\n\n\n")
	print(investigation_cell_members)
	print("\n\n\n")
	return investigation_cell_members

# @frappe.whitelist()
# def get_cell_member_details(investigating_authority):
#     cell_member_details = frappe.get_all(
#         "Employee",
#         {"name":investigating_authority},
#         ["employee_name","user_id"]
#     )
#     print("\n\n\n\n\nCell Members Details")
#     print(cell_member_details)
#     return cell_member_details

