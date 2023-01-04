// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Deallotment Process', {
	setup: function (frm) {
		frm.set_query("allotment_number", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query"
			};
		});
	},

	refresh: function(frm){
		if(frm.doc.workflow_state == 'Approved'){
			frm.trigger("fee_components");
		}
	},

	fee_components(frm){
		frappe.call({
			method: "wsc.wsc.doctype.deallotment_process.deallotment_process.fee_waiver",
			args: {
				allotment_number: frm.doc.allotment_number,
			},
			callback: function(r) { 
				if (r.message){
					frm.set_value("hostel_fees",r.message['name'])
					frm.set_value("fees",r.message['fees_id'])
					frm.set_value("hostel_fee_structure",r.message['hostel_fee_structure'])
				}
			} 
		});  
	},

});

frappe.ui.form.on("Deallotment Process", "hostel_fees", function(frm){
	frappe.model.with_doc("Hostel Fees", frm.doc.hostel_fees, function(){
		var tabletransfer = frappe.model.get_doc("Hostel Fees", frm.doc.hostel_fees);
		cur_frm.doc.components = "";
		cur_frm.refresh_field("components");
		$.each(tabletransfer.components, function(index, row){
			var d = frappe.model.add_child(cur_frm.doc, "Deallotment Fee Waiver Components", "components");
			d.fees_category = row.fees_category;
			d.amount = row.amount;
			d.waiver_type = row.waiver_type;
			d.percentage = row.percentage;
			d.waiver_amount = row.waiver_amount;
			d.total_waiver_amount = row.total_waiver_amount;
			d.receivable_account = row.receivable_account;
			d.income_account = row.income_account;
			d.company = row.company;
			d.amount = row.amount;
			d.grand_fee_amount = row.grand_fee_amount;
			d.outstanding_fees = row.outstanding_fees;
			d.outstanding_fees_ref = row.outstanding_fees;
			cur_frm.refresh_field("components");
		});
	});

});


frappe.ui.form.on("Deallotment Fee Waiver Components", "waiver_amount", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if(d.waiver_amount){
        d.amount = d.outstanding_fees_ref - d.waiver_amount
		if(d.amount < 0){
			d.amount = 0
			d.outstanding_fees = 0
			d.total_waiver_amount  = d.waiver_amount
		}
		else{
			d.total_waiver_amount  = d.waiver_amount
		}
        refresh_field("amount", d.name, d.parentfield);
        refresh_field("total_waiver_amount", d.name, d.parentfield);
		if(d.waiver_amount > d.outstanding_fees_ref){
			d.waiver_amount=0
			d.total_waiver_amount=0
			d.outstanding_fees=0
			d.amount=d.outstanding_fees_ref
			refresh_field("waiver_amount", d.name, d.parentfield);
			refresh_field("total_waiver_amount", d.name, d.parentfield);
			refresh_field("outstanding_fees", d.name, d.parentfield);
			refresh_field("amount", d.name, d.parentfield);
			frappe.msgprint("Waiver Amount should not be more than Outstanding Fees");
		}
    }
	else{
		d.amount=0
		d.total_waiver_amount=0
		d.outstanding_fees=d.outstanding_fees_ref
		refresh_field("amount", d.name, d.parentfield);
		refresh_field("total_waiver_amount", d.name, d.parentfield);
		refresh_field("outstanding_fees", d.name, d.parentfield);
	}
    // if(!d.amount){
    //     frappe.throw("Please add Amount first");
    // }
});

frappe.ui.form.on("Deallotment Fee Waiver Components", "percentage", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if(d.percentage){
        d.amount = d.outstanding_fees_ref - ((d.percentage/100)*d.grand_fee_amount)
		if(d.amount < 0){
			d.amount = 0
			d.outstanding_fees = 0
			d.total_waiver_amount  = (d.percentage/100)*d.grand_fee_amount
		}
		else{
			d.total_waiver_amount  = (d.percentage/100)*d.grand_fee_amount
		}
        refresh_field("amount", d.name, d.parentfield);
        refresh_field("total_waiver_amount", d.name, d.parentfield);
		if(d.percentage > 100){
			d.percentage=0
			d.total_waiver_amount=0
			d.outstanding_fees=0
			d.amount=d.outstanding_fees_ref
			refresh_field("waiver_amount", d.name, d.parentfield);
			refresh_field("total_waiver_amount", d.name, d.parentfield);
			refresh_field("outstanding_fees", d.name, d.parentfield);
			refresh_field("amount", d.name, d.parentfield);
			frappe.msgprint("Waiver Percentage should not be more than 100");
		}
    }
	else{
		d.amount=0
		d.total_waiver_amount=0
		d.outstanding_fees=d.outstanding_fees_ref
		refresh_field("amount", d.name, d.parentfield);
		refresh_field("total_waiver_amount", d.name, d.parentfield);
		refresh_field("outstanding_fees", d.name, d.parentfield);
	}
    // if(!d.amount){
    //     frappe.throw("Please add Amount first");
    // }
});

frappe.ui.form.on("Deallotment Fee Waiver Components", "waiver_type", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	if(d.waiver_type=="Percentage"||"Amount"){
		d.percentage=null
		d.waiver_amount=0
		d.total_waiver_amount=0
		d.amount=d.outstanding_fees_ref
		d.outstanding_fees=d.outstanding_fees_ref
		refresh_field("percentage", d.name, d.parentfield);
		refresh_field("waiver_amount", d.name, d.parentfield);
		refresh_field("amount", d.name, d.parentfield);
		refresh_field("outstanding_fees", d.name, d.parentfield);
		refresh_field("total_waiver_amount", d.name, d.parentfield);
	}});

frappe.ui.form.on("Deallotment Fee Waiver Components", "waiver_amount", function(frm, cdt, cdn) {
    var cal=locals[cdt][cdn];
    if (cal.total_waiver_amount) {
        cal.outstanding_fees=cal.amount;
    }	 
    cur_frm.refresh_field ("components");
});
frappe.ui.form.on("Deallotment Fee Waiver Components", "percentage", function(frm, cdt, cdn) {
    var cal=locals[cdt][cdn];
    if (cal.total_waiver_amount) {
        cal.outstanding_fees=cal.amount;
    }	 
    cur_frm.refresh_field ("components");
});


