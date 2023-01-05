frappe.ui.form.on('Fee Structure', {
	program(frm) {
        frm.clear_table("course_wise_fees");
        if (frm.doc.program){
                frappe.call({
                    method: "wsc.wsc.doctype.fee_structure.get_courses",
                    args: {
                        program: frm.doc.program,
                    },
                    callback: function(r) { 
                        (r.message).forEach(element => {
                            var c = frm.add_child("course_wise_fees")
                            c.course=element.course
                        });
                        frm.refresh_field("course_wise_fees")
                    } 
                    
                });    
        }
	},
    setup(frm){
        frm.set_query("programs", function () {
			return {
				filters: [
					["Programs", "program_grade", "=", frm.doc.program_grade],
				]
			}
		});
        frm.set_query("program",function(){
            return{
                filters:{
                    "programs":frm.doc.programs
                }
            }
        })
    },
  //   refresh(frm){
  //       frappe.call({
		// 	method: "wsc.wsc.doctype.fee_structure.get_fee_types",
		// 	callback: function(r) {
		// 		frm.set_df_property("fee_type", "options", r.message);
		// 	}
		// });
  //   }
});

frappe.ui.form.on("Fee Component", "fees_category", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.fees_category){
        var total_amount=0;
        (cur_frm.doc.course_wise_fees).forEach(e=>{
            total_amount+=(e.amount ? e.amount:0)
        })
        d.amount=total_amount;
        refresh_field("amount", d.name, d.parentfield);
    }
});

frappe.ui.form.on('Fee Structure', {
	onload: function(frm) {
		frm.set_query("receivable_account","components", function(_doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					'company': d.company,
					'account_type': d.account_type = 'Receivable',
					'is_group': d.is_group = 0
				}
			};
		});
		frm.set_query("income_account","components", function(_doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					'company': d.company,
					'account_type': d.account_type = 'Income Account',
					'is_group': d.is_group = 0
				}
			};
		});
		erpnext.accounts.dimensions.setup_dimension_filters(frm, frm.doctype);
	}
	

});

frappe.ui.form.on('Fee Structure', {
    onload:function(frm) {
		if(frappe.user.has_role(["Accounts User","Student","Education Administrator"]) && !frappe.user.has_role(["Administrator"])){
  			frm.remove_custom_button('Create Fee Schedule');
        }
	}
}
);
