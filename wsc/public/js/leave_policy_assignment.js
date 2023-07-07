frappe.ui.form.on('Leave Policy Assignment', {
	onload: function(frm) {
		frm.ignore_doctypes_on_cancel_all = ["Leave Ledger Entry"];

		frm.set_query('leave_policy', function() {
			return {
				filters: {
					"workflow_state": "Approved"
				}
			};
		});
    }
})