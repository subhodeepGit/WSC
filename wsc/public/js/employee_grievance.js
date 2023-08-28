frappe.ui.form.on('Employee Grievance', {
    setup: function(frm) {
        frm.set_query("investigation_cell", function() {
            return {
                query: "wsc.wsc.validations.employee_grievance.get_cell",
                filters: {
                    "grievance_type": frm.doc.grievance_type
                }
            };
        });
    }
});
