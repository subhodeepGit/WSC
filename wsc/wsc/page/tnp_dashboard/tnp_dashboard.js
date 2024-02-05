frappe.pages['tnp-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Training and Placement Dashboard',
		single_column: true
	});

	const container_list = document.querySelectorAll('.container')
	container_list[1].remove()
	
	$(frappe.render_template("tnp_dashboard" , {
		font_awesome_link:"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
	})).appendTo(page.body)
}