frappe.ui.form.on('Project', {
	setup: function(frm) {
		frm.set_query("project_manager", function() {
			return {
				filters: {
					"role_profile_name":frm.doc.role_profile
				}
			};
		});
	}
});