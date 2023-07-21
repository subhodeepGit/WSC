import frappe
import os
import json
import sys

#   bench execute wsc.patches.migrate_patch.get_custom_role_permission
def get_custom_role_permission(site=None):
    if sys.argv[2]=='--site':
        os.system("bench --site {0} export-fixtures".format(sys.argv[3]))
    else:
        os.system("bench export-fixtures")

#   bench execute wsc.patches.migrate_patch.set_custom_role_permission
def set_custom_role_permission():
    with open(frappe.get_app_path("wsc","fixtures","custom_docperm.json")) as f:
        for d in json.load(f):
            if len(frappe.get_all('Custom DocPerm',{'parent':d.get('parent'),'role':d.get('role')}))==0:
                role=frappe.new_doc('Custom DocPerm')
                for k in d.keys():
                    role.set(k,d.get(k))
                role.save()


#   bench execute wsc.patches.migrate_patch.set_custom_role_permission_remove_duplicate
def set_custom_role_permission_remove_duplicate():
    role_list=[]
    doctype=[]
    # perm_level=[0,1,2,3,4,5,6,7,8,9,10]
    perm_level=[0,1,2,3]
    custom_docperm_data=frappe.get_all('Custom DocPerm',fields=["amend","cancel","create","delete","docstatus","email","export",
                                                         "if_owner","import","modified","name","parent","permlevel","print","read",
                                                         "report","role","select","set_user_permissions","share","submit","write"])   
    if custom_docperm_data:
        for t in custom_docperm_data:
            role_list.append(t['role'])
            doctype.append(t['parent'])

        role_list=list(set(role_list))
        doctype=list(set(doctype))

        for i in role_list:
            for j in doctype:
                for k in perm_level:
                    data=[]
                    data=list(filter(lambda person: person['parent'] == j and person['role'] == i and person['permlevel']==k, custom_docperm_data))
                    if data:
                        if len(data)==1:
                            pass
                        else:
                            data.sort(key = lambda x: x['modified'], reverse=True)
                            for t in data:
                                index = data.index(t)
                                if index!=0:
                                    try:
                                        frappe.delete_doc("Custom DocPerm", t['name'])
                                        frappe.db.commit()
                                    except Exception as e:
                                        frappe.db.rollback()
                                        print(f"Error deleting Custom DocPerm: {e}")



def get_translation(site=None):
    if sys.argv[2]=='--site':
        os.system("bench --site {0} export-fixtures".format(sys.argv[3]))
    else:
        os.system("bench export-fixtures")

#   bench execute wsc.patches.migrate_patch.set_custom_role_permission
def set_translation():
    with open(frappe.get_app_path("wsc","fixtures","translation.json")) as f:
        for d in json.load(f):
            if len(frappe.get_all('Translation',{'source_text':d.get('source_text')}))==0:
                trans=frappe.new_doc('Translation')
                for k in d.keys():
                    trans.set(k,d.get(k))
                trans.save()


#   bench execute wsc.patches.migrate_patch.add_roles
def add_roles():
    with open(frappe.get_app_path("wsc","fixtures","role.json")) as f:
        for d in json.load(f):
            if len(frappe.get_all('Role',{'role_name':d.get('role_name')}))==0:
                role=frappe.new_doc('Role')
                for k in d.keys():
                    role.set(k,d.get(k))
                role.save()

#   bench execute wsc.patches.migrate_patch.add_roles
def add_module_profile():
    with open(frappe.get_app_path("wsc","fixtures","module_profile.json")) as f:
        for d in json.load(f):
            if len(frappe.get_all('Module Profile',{'name':d.get('name')}))==0:
                mp=frappe.new_doc('Module Profile')
                for k in d.keys():
                    mp.set(k,d.get(k))
                mp.save()
