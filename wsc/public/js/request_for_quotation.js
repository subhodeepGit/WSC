frappe.ui.form.on('Request for Quotation', {
	refresh: function(frm) {
        frm.remove_custom_button("Send Emails to Suppliers","Tools");
        frm.remove_custom_button("Download PDF","Tools");
    }
});