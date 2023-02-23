// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.provide("erpnext.accounts.dimensions");

frappe.ui.form.on("Hostel Fees", {
	setup: function(frm) {
		frm.add_fetch("hostel_fee_structure", "receivable_account", "receivable_account");
		frm.add_fetch("hostel_fee_structure", "income_account", "income_account");
		frm.add_fetch("hostel_fee_structure", "cost_center", "cost_center");
	},

	company: function(frm) {
		erpnext.accounts.dimensions.update_dimension(frm, frm.doctype);
	},

	onload: function(frm) {
		frm.set_query("student", function() {
			return {
				query: 'wsc.wsc.doctype.hostel_fees.hostel_fees.get_allotted_students',
			};
		});
		frm.set_query("academic_term", function() {
			return{
				"filters": {
					"academic_year": (frm.doc.academic_year)
				}
			};
		});
		frm.set_query("hostel_fee_structure", function() {
			return {
				query: 'wsc.wsc.doctype.hostel_fees.hostel_fees.get_fee_structures',
				filters: {
					"student":frm.doc.student
				}
			};
		});
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
		if (!frm.doc.posting_date) {
			frm.doc.posting_date = frappe.datetime.get_today();
		}

		erpnext.accounts.dimensions.setup_dimension_filters(frm, frm.doctype);
	},

	refresh: function(frm) {
		if(frm.doc.docstatus == 0 && frm.doc.set_posting_time) {
			frm.set_df_property('posting_date', 'read_only', 0);
			frm.set_df_property('posting_time', 'read_only', 0);
		} else {
			frm.set_df_property('posting_date', 'read_only', 1);
			frm.set_df_property('posting_time', 'read_only', 1);
		}
		if(frm.doc.docstatus > 0) {
			frm.add_custom_button(__('Accounting Ledger'), function() {
				frappe.route_options = {
					voucher_no: frm.doc.fees_id,
					from_date: frm.doc.posting_date,
					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
					company: frm.doc.company,
					group_by: '',
					show_cancelled_entries: frm.doc.docstatus === 2
				};
				frappe.set_route("query-report", "General Ledger");
			}, __("View"));
		}
	},

	student: function(frm) {
		if (frm.doc.student) {
			frappe.call({
				method:"education.education.api.get_current_enrollment",
				args: {
					"student": frm.doc.student,
					"academic_year": frm.doc.academic_year
				},
				callback: function(r) {
					if(r){
						$.each(r.message, function(i, d) {
							frm.set_value(i,d);
						});
					}
				}
			});
			frm.trigger("set_hostel_id");
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
		}
	},

	set_posting_time: function(frm) {
		frm.refresh();
	},

	academic_term: function() {
		frappe.ui.form.trigger("Fees", "program");
	},

	hostel_fee_structure: function(frm) {
		frm.set_value("components" ,"");
		if (frm.doc.hostel_fee_structure) {
			frappe.call({
				method: "wsc.wsc.doctype.hostel_fees.hostel_fees.get_fee_components",                
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

	calculate_total_amount: function(frm) {
		var grand_total = 0;
		for(var i=0;i<frm.doc.components.length;i++) {
			grand_total += frm.doc.components[i].amount;
		}
		frm.set_value("grand_total", grand_total);
	},
    
	set_hostel_id(frm){
		frappe.call({
			method: "wsc.wsc.doctype.hostel_fees.hostel_fees.hostel_admission",
			args: {
				student: frm.doc.student,
			},
			callback: function(r) { 
				if (r.message){
					frm.set_value("hostel_admission",r.message['name'])
					frappe.call({
						method: "wsc.wsc.doctype.hostel_fees.hostel_fees.room_allotment",
						args:{
							hostel_admission_id: frm.doc.hostel_admission,
						},
						callback: function(r) { 
							if (r.message){
								frm.set_value("allotment_number",r.message['name'])
								frm.set_value("hostel",r.message['hostel_id'])
								frm.set_value("room_number",r.message['room_number'])
								frm.set_value("room_type",r.message['room_type'])
							}
						} 						
					}); 
				}
			} 
		});  
	},

    set_program_enrollment(frm) {
        frappe.call({
            method: "wsc.wsc.validations.program_enrollment.get_program_enrollment",
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
});

frappe.ui.form.on("Fee Component", {
	amount: function(frm) {
		frm.trigger("calculate_total_amount");
	}
});
