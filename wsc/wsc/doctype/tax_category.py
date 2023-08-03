import frappe
from frappe.utils.nestedset import NestedSet, get_root_of
from frappe.query_builder.terms import SubQuery
from frappe.query_builder.utils import DocType

def on_doctype_update():
	frappe.db.add_index("Tax Category", ["lft", "rgt"])
	
@frappe.whitelist()
def get_children(doctype, parent=None, title=None, is_root=False):
	fields = ["name as value", "is_group as expandable"]
	filters = {}
	filters["parent_tax_category"] = parent
	return frappe.get_all("Tax Category", fields=fields, filters=filters, order_by="name")

@frappe.whitelist()
def add_node():
	from frappe.desk.treeview import make_tree_args

	args = frappe.form_dict
	args = make_tree_args(**args)

	frappe.get_doc(args).insert()