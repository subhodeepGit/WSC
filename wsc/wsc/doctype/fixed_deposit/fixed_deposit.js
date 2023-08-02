// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fixed Deposit', {
	refresh: function(frm){
		frm.set_df_property('interest_calculation', 'cannot_add_rows', true);
		frm.set_df_property('interest_calculation', 'cannot_delete_rows', true);

		if (frm.doc.matured_posting_journal_entry){
			frm.set_df_property('final_maturity_amount', 'read_only', 1);
			frm.set_df_property('matured', 'read_only', 1);
			frm.set_df_property('final_maturity_date', 'read_only', 1);
		}
		

		frm.set_query("fd_account", function () {
			return {
				filters:{
					"is_group":0,
					"company":frm.doc.company,
					"account_type":"Fixed Asset"
				}
			};
		}),
		frm.set_query("bank_account", function () {
			return {
				filters:{
					"is_group":0,
					"company":frm.doc.company,
					"account_type":"Bank"
				}
			};
		}),
		frm.set_query("interest_account", function () {
			return {
				filters:{
					"is_group":0,
					"company":frm.doc.company,
					"account_type":"Fixed Asset"
				}
			};
		})
	},
	get_amount:function(frm) {
		frappe.call({
			"method": "wsc.wsc.doctype.fixed_deposit.fixed_deposit.calculate_fd",
			args:{
				fd_amount:frm.doc.fd_amount,
				interest_payable:frm.doc.interest_payable,
				interest_type:frm.doc.interest_type,
				interest_rate:frm.doc.interest_percentage,
				days:frm.doc.tenure_days,
				weeks:frm.doc.tenurein_weeks,
				months:frm.doc.tenurein_months,
				quarterly:frm.doc.tenurein_quarter,
				semi_annually:frm.doc.tenuresemi_annually,
				annually:frm.doc.tenurein_annually

			},
			callback: function(r) {
				if (r.message){
					frm.refresh_field("maturity_amount")
					frm.set_value("maturity_amount",r.message['grand_maturity_amount'])
					frappe.model.clear_table(frm.doc, 'interest_calculation');
					(r.message['maturity_amount']).forEach(element => {
						var c = frm.add_child("interest_calculation")
						c.term=element.term
						c.principal_amount=element.principal_amount
						c.interest=element.interest
						c.total=element.total
					});
					frm.refresh_field("interest_calculation");
					frm.save();
				}
			}
		})
	},
	matured:function(frm){
		if(frm.doc.matured==1){
			frm.set_value("final_maturity_amount",frm.doc.maturity_amount)
			var intr=frm.doc.maturity_amount-frm.doc.fd_amount 
			frm.set_value("final_maturity_interest_amount",intr)
			frm.set_value("final_maturity_date",frm.doc.maturity_date)
		}
	},
	final_maturity_amount:function(frm){
		var intr=frm.doc.final_maturity_amount-frm.doc.fd_amount
		frm.set_value("final_maturity_interest_amount",intr)
	}
});


