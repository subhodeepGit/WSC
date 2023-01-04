frappe.ui.form.on('Fees', {
    // setup(frm){
    //     frm.set_query("fee_structure", function() {
    //         return {
    //             query: 'wsc.wsc.doctype.fees.get_fee_structures',
    //             filters: {
    //                 "exam_application":frm.doc.exam_application
    //             }
    //         };
    //     });
    // },
    refresh(frm){
        if(frm.doc.docstatus===1 && frm.doc.outstanding_amount==0) {
			frm.add_custom_button(__("Return/Refund"), function() {
                frappe.model.open_mapped_doc({
					method: "wsc.wsc.doctype.fees.make_refund_fees",
					frm: frm,
				});
			});
		}
    },
    amount(frm){
            if(frm.doc.amount){
                // frm.doc.outstanding_amount = frm.doc.grand_total - frm.doc.amount;
                // frm.doc.waiver_amount = frm.doc.amount
                frm.set_value("outstanding_amount",frm.doc.grand_total - frm.doc.amount);
                frm.set_value("waiver_amount",frm.doc.amount);

            }
     },
    percentage(frm){
        if(frm.doc.percentage){
            // outstanding_amount = frm.doc.grand_total - (frm.doc.grand_total*(frm.doc.percentage/100));
            // waiver_amount = (frm.doc.grand_total*(frm.doc.percentage/100))
            frm.set_value("outstanding_amount",frm.doc.grand_total - (frm.doc.grand_total*(frm.doc.percentage/100)));
            frm.set_value("waiver_amount",(frm.doc.grand_total*(frm.doc.percentage/100)));
        }
    },
    student(frm){
        if (frm.doc.student){
            frm.trigger("set_program_enrollment");
            frm.set_query("programs", function() {
                return {
                    query: 'wsc.wsc.doctype.fees.get_progarms',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
            frm.set_query("program", function() {
                return {
                    query: 'wsc.wsc.doctype.fees.get_sem',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
            frm.set_query("academic_term", function() {
                return {
                    query: 'wsc.wsc.doctype.fees.get_term',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
            frm.set_query("academic_year", function() {
                return {
                    query: 'wsc.wsc.doctype.fees.get_year',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
            frm.set_query("student_category", function() {
                return {
                    query: 'wsc.wsc.doctype.fees.get_student_category',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
            frm.set_query("student_batch", function() {
                return {
                    query: 'wsc.wsc.doctype.fees.get_batch',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
            frm.set_query("fee_structure", function() {
                return {
                    query: 'wsc.wsc.doctype.fees.get_fee_structures',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
            
        }
    },
	set_program_enrollment(frm) {
        frappe.call({
            method: "wsc.wsc.doctype.program_enrollment.get_program_enrollment",
            args: {
                student: frm.doc.student,
            },
            callback: function(r) { 
                if (r.message){
                    frm.set_value("program_enrollment",r.message['name'])
                }
            } 
            
        });    
        
	},
    setup(frm){
        frm.set_query("fees_category","components", function() {
            return {
                query: 'wsc.wsc.doctype.fees.get_fees_category',
                filters: {
                    "fee_structure":frm.doc.fee_structure
                }
            };
        });

    }
})
frappe.ui.form.on("Fee Component", "amount", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];

    if(d.amount){
        d.waiver_on_amount = d.amount 
        refresh_field("waiver_on_amount", d.name, d.parentfield);
    }
})
frappe.ui.form.on("Fee Component", "waiver_amount", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if(d.waiver_amount && d.amount){
        d.amount =  d.amount -d.waiver_amount
       d.total_waiver_amount  = d.waiver_amount
        refresh_field("amount", d.name, d.parentfield);
        refresh_field("total_waiver_amount", d.name, d.parentfield);
  
    }
    if(!d.amount){
        frappe.throw("Please add Amount first");
    }
});


frappe.ui.form.on("Fee Component", "percentage", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if(d.percentage && d.amount){
        d.amount =  d.amount - ((d.percentage/100) * d.amount)
       d.total_waiver_amount  = ((d.percentage/100) * d.amount)
        refresh_field("amount", d.name, d.parentfield);
        refresh_field("total_waiver_amount", d.name, d.parentfield);
  
    }
    if(!d.amount){
        frappe.throw("Please add Amount first");
    }
});

frappe.ui.form.on('Fees', {
    setup: function (frm) {
		frm.set_query("hostel_fee_structure", function () {
			return {
				filters: [
					["Fee Structure Hostel", "programs", "=", frm.doc.programs],
					["Fee Structure Hostel", "academic_year", "=", frm.doc.academic_year],
				]
			}
		});
	},
    hostel_fee_structure: function(frm) {
		frm.set_value("components" ,"");
		if (frm.doc.hostel_fee_structure) {
			frappe.call({
				method: "wsc.wsc.validations.fees.get_fee_components",              
				args: {
					"hostel_fee_structure": frm.doc.hostel_fee_structure
				},
				callback: function(r) {
					if (r.message) {
						$.each(r.message, function(i, d) {
							var row = frappe.model.add_child(frm.doc, "Fee Component", "components");
							row.fees_category = d.fees_category;
							row.receivable_account=d.receivable_account;
							row.income_account = d.income_account;
							row.description = d.description;
							row.amount = d.amount;
							row.receivable_account=d.receivable_account;
                            row.grand_fee_amount=d.grand_fee_amount;
                            row.outstanding_fees=d.outstanding_fees;
						});
					}
					refresh_field("components");
					frm.trigger("calculate_total_amount");
				}
			});
		}
	},
});