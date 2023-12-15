frappe.ui.form.on('Supplier', {
	refresh: function(frm) {
        frm.remove_custom_button("Get Supplier Group Details","Actions");
        frm.remove_custom_button("Bank Account","Create");
        frm.remove_custom_button("Pricing Rule","Create");
        frm.remove_custom_button("Accounts Payable","View");
    }
});