frappe.ui.form.on('Employee Grievance', {
    // setup: function(frm) {
    //     frm.set_query("investigation_cell", function() {
    //         return {
    //             query: "wsc.wsc.validations.employee_grievance.get_cell",
    //             filters: {
    //                 "grievance_type": frm.doc.grievance_type
    //             }
    //         };
    //     });

    //     frm.set_query("investigating_authority", function() {
    //         return {
    //             query: "wsc.wsc.validations.employee_grievance.get_cell_members",
    //             filters: {
    //                 "investigation_cell": frm.doc.investigation_cell
    //             }
    //         };
    //     });
    //     frm.set_query("resolved_by", function() {
    //         return {
    //             query: "wsc.wsc.validations.employee_grievance.get_cell_members",
    //             filters: {
    //                 "investigation_cell": frm.doc.investigation_cell
    //             }
    //         };
    //     });
    // },
    investigation_cell:function(frm){
        frm.clear_table("grievance_cell_members")
		frappe.call({
			method: 'wsc.wsc.validations.employee_grievance.get_cell_members',
			args: {
				"investigation_cell":frm.doc.investigation_cell
			},
			
            callback: function(r) {
            
                (r.message).forEach(element => {
                    var row = frm.add_child("grievance_cell_members")
                    row.employee=element.employee
                    row.employee_name=element.employee_name
                    row.user_id = element.user_id
                    row.designation= element.designation
                    row.department = element.designation
                });
                frm.refresh_field("grievance_cell_members");
                
            }

        })
    }
});
