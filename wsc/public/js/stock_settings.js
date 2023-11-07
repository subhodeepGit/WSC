frappe.ui.form.on('Stock Settings', {
    refresh: function(frm) {
        frm.set_df_property('valuation_method','documentation_url'," ");
    }
});