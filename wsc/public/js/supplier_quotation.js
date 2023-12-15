frappe.ui.form.on('Supplier Quotation', {
    refresh:function(frm) {
		frm.disable_('Get Items From');
	}
});