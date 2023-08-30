import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_grievance_member,employee_grievance_employee_mail,employee_grievance_hr_mail
def validate(self,method):
    # set_user_permission(self)
    if self.workflow_state == "Forwarded to HR":
        employee_grievance_hr_mail(self)
    if self.workflow_state=="Forwarded to Grievance Cell":
        employee_grievance_member(self)
    if self.workflow_state=="Resolved" or self.workflow_state=="Rejected":
        employee_grievance_employee_mail(self)    


# def set_user_permission(self):
#     user = frappe.session.user
#     if len(frappe.get_roles(user)) == 1 and "Employee" in frappe.get_roles(user):
#         # Implement logic to add user permission for the session user
#         # ...
#         add_user_permission(self.doctype,self.name,self.employee_email,self)
#         print("\n\n\n")
#         print("user permission set sucessfully")

#     # Check if the user has any of the specified roles
#     elif any(role in frappe.get_roles(user) for role in ["HR Admin", "Director", "Grievance Cell Member"]):
#         print("No user permission.....")
#         pass
		
		
# def on_trash(self):
#     self.delete_permission()
    
# def delete_permission(self):
#     for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
#         frappe.delete_doc("User Permission",d.name)

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

