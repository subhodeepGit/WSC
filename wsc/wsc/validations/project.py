import frappe

def after_insert(self):
    email = frappe.get_all('Project' , {'name':self.name},['project_manager'])
    user_perm = frappe.new_doc("User Permission")
    user_perm.user = email[0]['project_manager']
    user_perm.allow = self.doctype
    user_perm.for_value = self.name
    user_perm.save()