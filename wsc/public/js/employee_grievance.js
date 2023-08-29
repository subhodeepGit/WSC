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

        frm.set_query("investigating_authority", function() {
            return {
                query: "wsc.wsc.validations.employee_grievance.get_cell_members",
                filters: {
                    "investigation_cell": frm.doc.investigation_cell
                }
            };
        });
        frm.set_query("resolved_by", function() {
            return {
                query: "wsc.wsc.validations.employee_grievance.get_cell_members",
                filters: {
                    "investigation_cell": frm.doc.investigation_cell
                }
            };
        });
    },
    investigating_authority:function(frm){
		frappe.call({
			method: 'wsc.wsc.validations.employee_grievance.get_cell_member_details',
			args: {
				"investigating_authority":frm.doc.investigating_authority
			},
			callback: function(r) {
				if (r.message) {
					if (r.message[0]['employee_name']){
						frm.set_value("authority_name",r.message[0]['employee_name'])
					}
					if (r.message[0]['user_id']){
						frm.set_value("authority_user_id",r.message[0]['user_id'])
					}
                }
            }
        })
    }
});
