import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_grievance_member,employee_grievance_employee_mail
def validate(self,method):
    if self.workflow_state=="Under Review":
        employee_grievance_member(self)
    if self.workflow_state=="Resolved" or self.workflow_state=="Rejected":
        employee_grievance_employee_mail(self)    


# @frappe.whitelist()
# def get_cell(doctype, txt, searchfield, start, page_len, filters):
#     investigation_cell = frappe.get_all(
#         "Employee Grievance Cell",
#         {"grievance_type":filters.get("grievance_type")},
#         ["name"],as_list=1
#     )

#     member_names = [member for member in investigation_cell]

#     return member_names

# @frappe.whitelist()
# def get_cell_members(doctype, txt, searchfield, start, page_len, filters):
#     investigation_cell_members = frappe.get_all(
#         "Grievance Members",
#         {"parent":filters.get("investigation_cell")},
#         ["employee","employee_name"],as_list=1
#     )
#     return investigation_cell_members

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

