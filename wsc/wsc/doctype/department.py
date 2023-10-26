import frappe
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions

def validate(self, method):
    print("\n\nHELLO")
    print(self.name)
    create_permissions(self)


def create_permissions(doc):
    for instr in frappe.get_all("Instructor",{"department":doc.name},['employee']):
        for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id','department']):
            if emp.user_id:
                add_user_permission(doc.doctype,doc.name,emp.user_id,doc)	
