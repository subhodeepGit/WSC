frappe.ui.form.on('Bank Guarantee', {
    onload: function(frm) {
        frm.set_query('reference_document', function() {
            return {
                filters: {
                    'name': 'Purchase Order'
                }
            };
        });
    }
}
);