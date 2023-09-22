// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fees Waiver', {
	onload: function(frm) {
        frm.set_query("academic_term",function(){
            return{
                filters:{
                    "academic_year":frm.doc.academic_year
                }
            }
        });
        frm.set_query("semester",function(){
            return{
                filters:{
                    "programs":frm.doc.programs
                },
            }
        });
		if (frm.doc.student_category){
			frm.set_query("fee_structure",function(){
				return{
					filters:{
						"programs":frm.doc.programs,
						"program":frm.doc.semester,
						"academic_year":frm.doc.academic_year,
						"academic_term":frm.doc.academic_term,
						"student_category":frm.doc.student_category,
						"fee_type":frm.doc.fee_type,
						"docstatus":1
					}
				}
			});
		}else{
			frm.set_query("fee_structure",function(){
				return{
					filters:{
						"programs":frm.doc.programs,
						"program":frm.doc.semester,
						"academic_year":frm.doc.academic_year,
						"academic_term":frm.doc.academic_term,
						// "student_category":frm.doc.student_category,
						"fee_type":frm.doc.fee_type,
						"docstatus":1
					}
				}
			});
		}

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
					'is_group': d.is_group = 0,
                    'liability':0
				}
			};
		});
		erpnext.accounts.dimensions.setup_dimension_filters(frm, frm.doctype);
	},

	programs(frm){
		frm.set_value("fee_structure",'')
	},
	semester(frm){
		frm.set_value("fee_structure",'')
	},
	academic_year(frm){
		frm.set_value("fee_structure",'')
	},
	academic_term(frm){
		frm.set_value("fee_structure",'')
	},
	fee_type(frm){
		frm.set_value("fee_structure",'')
	},

	student(frm){
        if (frm.doc.student){
				frappe.call({
					method: "wsc.wsc.validations.program_enrollment.get_program_enrollment",
					args: {
						student: frm.doc.student,
					},
					callback: function(r) { 
						if (r.message){
							frm.set_value("programs",r.message['programs'])
							frm.set_value("semester",r.message['program'])
							frm.set_value("academic_year",r.message['academic_year'])
							frm.set_value("academic_term",r.message['academic_term'])
						}
						else{
							frm.set_value("programs",'')
							frm.set_df_property("programs", "reqd", 1);
							frm.set_value("semester",'')
							frm.set_df_property("semester", "reqd", 1);
							frm.set_value("academic_year",'')
							frm.set_df_property("academic_year", "reqd", 1);
							frm.set_value("academic_term",'')
							frm.set_df_property("academic_term", "reqd", 1);
						}
					}   
				});       
        }
    },
});

frappe.ui.form.on("Fee Component", "amount", function(frm, cdt, cdn) {
	frm.set_df_property("receivable_account", "read_only", 1);
    var ed_details = frm.doc.components;
    for(var i in ed_details) {            
    if (ed_details[i].amount) {
        ed_details[i].grand_fee_amount=ed_details[i].amount;
		ed_details[i].outstanding_fees=ed_details[i].amount;
    } 
   }
        cur_frm.refresh_field ("components");    
});

frappe.ui.form.on("Fee Component", "waiver_amount", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if(d.waiver_amount && d.amount ){
		
        d.amount =  d.grand_fee_amount -d.waiver_amount
        d.total_waiver_amount  = d.waiver_amount
        refresh_field("amount", d.name, d.parentfield);
        refresh_field("total_waiver_amount", d.name, d.parentfield);
		
    }
	else{
		d.amount=d.grand_fee_amount
		d.total_waiver_amount=null
		d.outstanding_fees=d.grand_fee_amount
	}
    if(!d.amount){
        frappe.throw("Please add Amount first");
    }
});

frappe.ui.form.on("Fee Component", "percentage", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	// var amount=parseInt(d.percentage)
    // if(amount!=0 && percentage<=100){
	// 	d.total_waiver_amount  = ((d.percentage/100) * d.grand_fee_amount)
    //     d.amount =  d.grand_fee_amount - ((d.percentage/100) * d.grand_fee_amount)
	// 	d.total_waiver_amount  = d.grand_fee_amount-d.amount
    //     refresh_field("amount", d.name, d.parentfield);
    //     refresh_field("total_waiver_amount", d.name, d.parentfield);
    // }
	if(d.percentage && d.amount ){
		d.total_waiver_amount  = ((d.percentage/100) * d.grand_fee_amount)
        d.amount =  d.grand_fee_amount - ((d.percentage/100) * d.grand_fee_amount)
		d.total_waiver_amount  = d.grand_fee_amount-d.amount
        refresh_field("amount", d.name, d.parentfield);
        refresh_field("total_waiver_amount", d.name, d.parentfield);
    }
	else{
		d.amount=d.grand_fee_amount
		d.total_waiver_amount=null
		d.outstanding_fees=d.grand_fee_amount
		refresh_field("percentage", d.name, d.parentfield);
	}
    if(!d.amount){
        frappe.throw("Please add Amount first");
    }
});

frappe.ui.form.on("Fee Component", "waiver_type", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	if(d.waiver_type=="Percentage"||"Amount"){
		d.percentage=null
		d.waiver_amount=null
		d.total_waiver_amount=null
		d.amount=d.grand_fee_amount
        d.outstanding_fees=d.grand_fee_amount
		refresh_field("total_waiver_amount", d.name, d.parentfield);
		refresh_field("percentage", d.name, d.parentfield);
		refresh_field("waiver_amount", d.name, d.parentfield);
		refresh_field("amount", d.name, d.parentfield);
	}
	frappe.ui.form.on("Fee Component", "waiver_amount", function(frm, cdt, cdn) {
		var cal=locals[cdt][cdn];
		if (cal.total_waiver_amount) {
			cal.outstanding_fees=cal.amount;
		}	 
		cur_frm.refresh_field ("components");
	});
	frappe.ui.form.on("Fee Component", "percentage", function(frm, cdt, cdn) {
		var cal=locals[cdt][cdn];
		if (cal.total_waiver_amount) {
			cal.outstanding_fees=cal.amount;
		}	 
		cur_frm.refresh_field ("components");
	});
});


frappe.ui.form.on('Fees Waiver', {
    setup(frm){
        frm.set_query("fee_structure", function() {
				frm.set_value("components" ,"");
				if (frm.doc.fee_structure) {
					frappe.call({
						method: "wsc.wsc.doctype.fees_waiver.fees_waiver.get_fee_components",
						args: {
							"fee_structure": frm.doc.fee_structure
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
									row.grand_fee_amount=d.grand_fee_amount;
									row.outstanding_fees=d.outstanding_fees;
									row.waiver_type=d.waiver_type;
									row.percentage=d.percentage;
									row.waiver_amount=d.waiver_amount;
									row.total_waiver_amount=d.total_waiver_amount; 
								});
							}
							refresh_field("components");
						}
					});
					var df_amount = frappe.meta.get_docfield("Fee Component","amount", frm.doc.name);
					df_amount.read_only = 1;
					var df_receivable_account = frappe.meta.get_docfield("Fee Component","receivable_account", frm.doc.name);
					df_receivable_account.read_only = 1;
					var df_income_account = frappe.meta.get_docfield("Fee Component","income_account", frm.doc.name);
					df_income_account.read_only = 1;
					var df_company = frappe.meta.get_docfield("Fee Component","company", frm.doc.name);
					df_company.read_only = 1;
					var df_total_waiver_amount = frappe.meta.get_docfield("Fee Component","total_waiver_amount", frm.doc.name);
					df_total_waiver_amount.read_only = 1;
					frm.clear_table("components");
					frm.refresh_field('components');
					frm.refresh_field('amount');
					frm.refresh_field('receivable_account');
					frm.refresh_field('income_account');
					frm.refresh_field('company');
				}
        });
    },
})

