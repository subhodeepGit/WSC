import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_grievance_member,employee_grievance_employee_mail
def validate(self,method):
    if self.workflow_state=="Under Review":
        employee_grievance_member(self)
    if self.workflow_state=="Resolved" or self.workflow_state=="Rejected":
        employee_grievance_employee_mail(self)    


@frappe.whitelist()
def get_cell(doctype, txt, searchfield, start, page_len, filters):
    investigation_cell = frappe.get_all(
        "Employee Grievance Cell",
        {"grievance_type":filters.get("grievance_type")},
        ["name"],as_list=1
    )
    print("\n\n\n")
    print(investigation_cell)
    print("\n\n\n")
    member_names = [member for member in investigation_cell]

    return member_names

# @frappe.whitelist()
# def get_cell_members(investigation_cell):
#     grievance_cell_mebe