frappe.treeview_settings["Tax Category"] = {
	ignore_fields:["parent_tax_category"],
	get_tree_nodes: 'wsc.wsc.doctype.tax_category.get_children',
	add_tree_node: 'wsc.wsc.doctype.tax_category.add_node',
    breadcrumb: "WSC",
	root_label: "All Tax Category",
	get_tree_root: false,
	menu_items: [
		{
			label: __("New Tax Category"),
			action: function() {
				frappe.new_doc("Tax Category", true);
			},
			condition: 'frappe.boot.user.can_create.indexOf("Tax Category") !== -1'
		}
	],
	onload: function(treeview) {
		treeview.make_tree();
	}
}
