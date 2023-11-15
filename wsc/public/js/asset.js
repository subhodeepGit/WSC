frappe.ui.form.on('Asset', {
	refresh: function(frm) {
		frm.set_df_property('status', 'options', ['Draft', 'Submitted', 'Partially Depreciated', 'Fully Depreciated', 'Sold', 'Scrapped']);
	}
});