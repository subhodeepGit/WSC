# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Module(Document):
	def validate(self):
		if frappe.session.user !="Administrator":
			frappe.throw("Only Developer can able to do the changes")
		duplicate_row_validation(self, "doc_type",['doctype_list'])
		duplicate_data(self)
	
	def on_trash(self):
		if frappe.session.user !="Administrator":
			frappe.throw("Only Developer can able to delete the changes")

def duplicate_row_validation(doc,table_field_name,comapre_fields):
    row_names=[]
    for row in doc.get(table_field_name):
        row_names.append(row.name)

    for row in doc.get(table_field_name):
        filters={"parent":row.parent,"idx":("!=",row.idx)}
        for field in comapre_fields:
            filters[field]=row.get(field)
        for duplicate in frappe.get_all(row.doctype,filters,['idx','name']):
            if duplicate.name in row_names:
                frappe.throw("#Row {0} Duplicate values in <b>Doctype list</b> Not Allowed".format(duplicate.idx))

def duplicate_data(self):
	for data in self.get("doc_type"):
		for t in frappe.get_all("Module",["name"]):
			if t.name==self.name:
				pass
			else:
				for x in frappe.get_all("Module Child",{"parent":t.name},["doctype_list"]):
					if x.doctype_list==data.doctype_list:
						frappe.throw("<b>{0}</b> already present in <b>{1}</b> data".format(data.doctype_list,t.name))