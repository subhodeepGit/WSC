frappe.pages['tnp-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Training and Placement Dashboard',
		single_column: true
	});
}