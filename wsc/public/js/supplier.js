frappe.ui.form.on('Supplier', {
	refresh: function(frm) {
        frm.remove_custom_button("Get Supplier Group Details","Actions");
    }
});