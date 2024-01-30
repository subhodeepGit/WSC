frappe.ui.form.on('Contract', {
	refresh: function(frm) {
		frm.set_df_property('party_type', 'options', ['Supplier', 'Employee']);
	}
});	

frappe.ui.form.on('Contract', {
	refresh: function(frm) {
		frm.set_df_property('document_type', 'options', ['Quotation', 'Project','Purchase Order','Purchase Invoice']);
	}
});	