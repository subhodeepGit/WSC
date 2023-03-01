# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RolePermissionTool(Document):
	def validate(self):
		if self.role =="Administrator":
			frappe.throw("Administrator is not for User")

	def before_submit(self):
		inactive_role(self)

	def on_submit(self):
		active_role(self)
		for t_object in self.get("role_permission"):
			role_permissions_manager_cration(t_object,self.role)
	
	def on_cancel(self):
		frappe.throw("Document can not be cancel, Only New Document can be created.")
			

def role_permissions_manager_cration(t_object,role):
	role_permissions_manager_info=frappe.get_all("Custom DocPerm",{"parent":t_object.doctype_name,"role":role})
	if not role_permissions_manager_info:
		role_permissions_manager_doc = frappe.new_doc("Custom DocPerm")
		role_permissions_manager_doc.parent=t_object.doctype_name
		role_permissions_manager_doc.role=role
		role_permissions_manager_doc.permlevel=0
		role_permissions_manager_doc.select=t_object.select
		role_permissions_manager_doc.read=t_object.read
		role_permissions_manager_doc.write=t_object.write
		role_permissions_manager_doc.create=t_object.create
		role_permissions_manager_doc.delete=t_object.del_data
		role_permissions_manager_doc.submit=t_object.submittable
		role_permissions_manager_doc.cancel=t_object.can_data
		role_permissions_manager_doc.amend=t_object.amnd_data
		role_permissions_manager_doc.report=t_object.report
		role_permissions_manager_doc.export=t_object.export
		role_permissions_manager_doc.share=t_object.shr_data
		role_permissions_manager_doc.print=t_object.print
		role_permissions_manager_doc.email=t_object.eml_data
		role_permissions_manager_doc.save()
		frappe.db.sql(""" Update `tabCustom DocPerm` set import="%s" where name='%s' """%(t_object.import_data,role_permissions_manager_doc.name))
	else:
		role_permissions_manager_doc=frappe.get_doc("Custom DocPerm", role_permissions_manager_info[0]['name'])
		role_permissions_manager_doc.parent=t_object.doctype_name
		role_permissions_manager_doc.role=role
		role_permissions_manager_doc.permlevel=0
		role_permissions_manager_doc.select=t_object.select
		role_permissions_manager_doc.read=t_object.read
		role_permissions_manager_doc.write=t_object.write
		role_permissions_manager_doc.create=t_object.create
		role_permissions_manager_doc.delete=t_object.del_data
		role_permissions_manager_doc.submit=t_object.submittable
		role_permissions_manager_doc.cancel=t_object.can_data
		role_permissions_manager_doc.amend=t_object.amnd_data
		role_permissions_manager_doc.report=t_object.report
		role_permissions_manager_doc.export=t_object.export
		role_permissions_manager_doc.share=t_object.shr_data
		role_permissions_manager_doc.print=t_object.print
		role_permissions_manager_doc.email=t_object.eml_data
		role_permissions_manager_doc.save()
		frappe.db.sql(""" Update `tabCustom DocPerm` set import="%s" where name='%s' """%(t_object.import_data,role_permissions_manager_doc.name))

def inactive_role(self):
	old_data = frappe.get_all("Role Permission Tool",{"role":self.role,"module_name":self.module_name,"docstatus":1,"active_status":"Active"},["name"])
	for Nr in old_data:
		if Nr:
			frappe.db.set_value("Role Permission Tool", Nr, "active_status","Inactive")

def active_role(self):
	frappe.db.set_value("Role Permission Tool",self.name,"active_status","Active")

@frappe.whitelist()
def fetch_data(role,module_name):
	role_name=role
	module=module_name
	for t in frappe.get_all("Module",["name"]):
		final=[]
		if t.name==module:
			mod_child = frappe.get_all("Module Child",{"parent":t.name},["doctype_list"])
			for child_mod in mod_child:
				role_permission=frappe.get_all("Custom DocPerm",{"parent":child_mod['doctype_list'],"role":role_name},
							["name","select","read","write","create","submit","cancel","amend","email","delete","report","export","import","print","share"])
				if role_permission:
					mod = {}
					mod['doctype_list'] = child_mod['doctype_list']
					mod['select']=role_permission[0]["select"]
					mod['read']=role_permission[0]["read"]
					mod['write']=role_permission[0]["write"]
					mod['create']=role_permission[0]["create"]
					mod['submittable']=role_permission[0]["submit"]
					mod['can_data']=role_permission[0]["cancel"]
					mod['amnd_data']=role_permission[0]["amend"]
					mod['eml_data']=role_permission[0]["email"]
					mod['del_data']=role_permission[0]["delete"]
					mod['report']=role_permission[0]["report"]
					mod['export']=role_permission[0]["export"]
					mod['import_data']=role_permission[0]["import"]
					mod['print']=role_permission[0]["print"]
					mod['shr_data']=role_permission[0]["share"]
					final.append(mod)
				else:
					field=["name","select","read","write","create","submittable","can_data","amnd_data","eml_data","del_data","report","export","import_data","print","shr_data"]
					mod={}
					mod['doctype_list']=child_mod['doctype_list']
					for t in field:
						mod[t]=0
					final.append(mod)
			return final