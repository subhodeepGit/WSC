frappe.ui.form.on('Warehouse', {
    refresh:function(frm) {
		frm.remove_custom_button('Disable');
		frm.remove_custom_button('Stock Balance');
		frm.remove_custom_button('Convert to Group');
		frm.remove_custom_button('General Ledger');
	}
});