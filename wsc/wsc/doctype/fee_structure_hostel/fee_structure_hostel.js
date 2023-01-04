frappe.ui.form.on('Fee Structure Hostel', {
	program(frm) {
        frm.clear_table("course_wise_fees");
        if (frm.doc.program){
                frappe.call({
                    method: "kp_edtec.kp_edtec.doctype.fee_structure.get_courses",
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
		frm.add_fetch('company', 'cost_center', 'cost_center');
        frm.set_query("program",function(){
            return{
                filters:{
                    "programs":frm.doc.programs
                }
            }
        });
		frm.set_query("academic_term",function(){
            return{
                filters:{
                    "academic_year":frm.doc.academic_year
                }
            }
        });
        frm.set_query("fee_type",function(){
            return{
                filters:{
                    "is_hostel":1
                }
            }
        });
    },
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


// filter income account receivable account
frappe.ui.form.on('Fee Structure Hostel', {
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