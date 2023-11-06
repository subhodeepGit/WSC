frappe.ui.form.on('Price List', {
	refresh: function(frm) {
        frm.remove_custom_button("Add / Edit Prices");
    }
});