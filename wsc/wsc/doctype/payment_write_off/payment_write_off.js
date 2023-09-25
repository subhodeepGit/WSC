// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Write Off', {

	get_outstanding_fees: function(frm) {
		const today = frappe.datetime.get_today();
		const fields = [
			{fieldtype:"Section Break", label: __("Posting Date")},
			{fieldtype:"Date", label: __("From Date"),
				fieldname:"from_posting_date", default:frappe.datetime.add_days(today, -30)},
			{fieldtype:"Column Break"},
			{fieldtype:"Date", label: __("To Date"), fieldname:"to_posting_date", default:today},
			{fieldtype:"Section Break", label: __("Due Date")},
			{fieldtype:"Date", label: __("From Date"), fieldname:"from_due_date"},
			{fieldtype:"Column Break"},
			{fieldtype:"Date", label: __("To Date"), fieldname:"to_due_date"},
			{fieldtype:"Section Break", label: __("Outstanding Amount")},
			{fieldtype:"Float", label: __("Greater Than Amount"),
				fieldname:"outstanding_amt_greater_than", default: 0},
			{fieldtype:"Column Break"},
			{fieldtype:"Float", label: __("Less Than Amount"), fieldname:"outstanding_amt_less_than"},
			{fieldtype:"Section Break"},
			// {fieldtype:"Link", label:__("Cost Center"), fieldname:"cost_center", options:"Cost Center",
			// default:frm.doc.cost_center,
			// 	"get_query": function() {
			// 		return {
			// 			"filters": {"company": frm.doc.company}
			// 		}
			// 	}
			// },
			// {fieldtype:"Column Break"},
			// {fieldtype:"Section Break"},
			{fieldtype:"Check", label: __("Allocate Payment Amount"), fieldname:"allocate_payment_amount", default:1},
		];
		frappe.prompt(fields, function(filters){
			frappe.flags.allocate_payment_amount = true;
			frm.events.validate_filters_data(frm, filters);
			// frm.doc.cost_center = filters.cost_center;
			frm.events.get_outstanding_documents_fee(frm, filters);
		}, __("Filters"), __("Get Outstanding Documents"));
	},

	validate_filters_data: function(frm, filters) {
		const fields = {
			'Posting Date': ['from_posting_date', 'to_posting_date'],
			'Due Date': ['from_posting_date', 'to_posting_date'],
			'Advance Amount': ['from_posting_date', 'to_posting_date'],
		};

		for (let key in fields) {
			let from_field = fields[key][0];
			let to_field = fields[key][1];

			if (filters[from_field] && !filters[to_field]) {
				frappe.throw(
					__("Error: {0} is mandatory field", [to_field.replace(/_/g, " ")])
				);
			} else if (filters[from_field] && filters[from_field] > filters[to_field]) {
				frappe.throw(
					__("{0}: {1} must be less than {2}", [key, from_field.replace(/_/g, " "), to_field.replace(/_/g, " ")])
				);
			}
		}
	},

	get_outstanding_documents_fee: function(frm, filters) {
		frm.clear_table("references");

		// if(!frm.doc.student) {
		// 	return;
		// }

		// frm.events.check_mandatory_to_fetch(frm);
		// var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;

		var args = {
			// "posting_date": frm.doc.posting_date,
			// "company": frm.doc.company,
			// "party_type": frm.doc.party_type,
			// "payment_type": frm.doc.payment_type,
			"student": frm.doc.student,
			// "party_account": frm.doc.payment_type=="Receive" ? frm.doc.paid_from : frm.doc.paid_to,
			// "cost_center": frm.doc.cost_center
		}

		for (let key in filters) {
			args[key] = filters[key];
		}
		// console.log(args);
		frappe.flags.allocate_payment_amount = filters['allocate_payment_amount'];

		return  frappe.call({
			method: 'wsc.wsc.doctype.payment_write_off.payment_write_off.get_outstanding_fees', 
			args: {
				args:args
			},
			callback: function(r, rt) {
				if(r.message) {
					// alert(JSON.stringify(r.message))
					var total_positive_outstanding = 0;
					var total_negative_outstanding = 0;
					var amount=0;

					// $.each(r.message, function(i, d) {
					// 	alert(JSON.stringify(d))
					// 	var c = frm.add_child("references");
					// 	c.fees_category=d.fees_category;
					(r.message).forEach(element => {
                        var c = frm.add_child("references")
                        c.fees_category = element.fees_category
						c.program=element.program
						c.reference_doctype=element.Type
						c.reference_name=element.reference_name
						c.due_date=element.posting_date
						c.allocated_amount=element.outstanding_fees
						amount=amount+c.allocated_amount
						c.total_amount=element.outstanding_fees
						c.outstanding_amount=element.outstanding_fees
						c.account_paid_from=element.receivable_account
						c.exchange_rate=element.exchange_rate
                    });
					frm.set_value("total_allocated_amount",amount)
					// frm.set_value("paid_amount",amount)						
                    frm.refresh_field("references")
				}

			}
		});
	},
});




// frappe.ui.form.on('Payment Write Off', {
// 	student(frm){
// 		if (frm.doc.student) {
// 			// console.log('aaaaaaaa');
// 			// console.log(args);
// 			frappe.call({
// 				method: 'wsc.wsc.doctype.payment_write_off.get_student_details',
// 				args: {
// 					args:args
// 				},
// 				callback: function(r) {
// 					if (r.message) {
// 						(r.message).forEach(function (element) {
// 								var c = frm.add_child("references");
// 								c.semesters = element.program;
// 							});
// 					}
// 					frm.refresh();
// 					refresh_field('references');
// 				}
// 			});
// 		}
// 	}
// });