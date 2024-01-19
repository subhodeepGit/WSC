frappe.ui.form.on('Asset', {
	refresh: function(frm) {
		frm.set_df_property('status', 'options', ['Draft', 'Submitted', 'Partially Depreciated', 'Fully Depreciated', 'Sold', 'Scrapped']);
		frm.set_df_property('asset_owner', 'options', ['Company', 'Supplier']);
		frm.remove_custom_button('Transfer Asset','Manage');
		frm.remove_custom_button('Maintain Asset','Manage');
		frm.remove_custom_button('Sell Asset','Manage');
		frm.remove_custom_button('Repair Asset','Manage');
		frm.remove_custom_button('Split Asset','Manage');
		frm.remove_custom_button('Adjust Asset Value','Manage');
	}
});