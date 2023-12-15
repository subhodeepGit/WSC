frappe.ui.form.on('Request for Quotation', {
	refresh: function(frm) {
        frm.remove_custom_button("Send Emails to Suppliers","Tools");
        frm.remove_custom_button("Download PDF","Tools");
        // frm.remove_custom_button('Material Request','Get Items From');
        // frm.remove_custom_button('Opportunity','Get Items From');
        // frm.remove_custom_button('Possible Supplier','Get Items From');
        frm.remove_custom_button('Link to Material Requests','Tools');
        frm.remove_custom_button('Get Suppliers','Tools');
    }
});

frappe.ui.form.on('Request for Quotation', {
	refresh: function(frm) {
        frm.disable_('Tools');
    }
});