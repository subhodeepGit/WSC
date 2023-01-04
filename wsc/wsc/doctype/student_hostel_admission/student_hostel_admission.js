// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Hostel Admission', {
	setup: function (frm) {
		frm.set_query("hostel", function () {
			return {
				query: "wsc.wsc.doctype.student_hostel_admission.student_hostel_admission.hostel_query"
			};
		});
		frm.set_query("room_type", function () {
			return {
				query: "wsc.wsc.doctype.student_hostel_admission.student_hostel_admission.room_query"
			};
		});
	},
	hostel_fee_applicable: function(frm) {
		frappe.call({
			method: "wsc.wsc.doctype.student_hostel_admission.student_hostel_admission.fst_query",                
			args: {
				"doc": frm.doc,
				"room_type": frm.doc.room_type
			},
			callback: function(r) {
				if(r.message){
					var utr=r.message;
					frm.set_query("hostel_fee_structure", function () {
						return {
							filters: [
								["Fee Structure Hostel", "programs", "=", utr['programs']],
								["Fee Structure Hostel", "program", "=", utr['semesters']],
								["Fee Structure Hostel", "academic_year", "=", utr['academic_year']],
								["Fee Structure Hostel", "academic_term", "=", utr['academic_term']],
								["Fee Structure Hostel", "room_type", "=", utr['room_type']],
							]
						}
						});
				}
			}
		});
	},
	refresh: function (frm) {
		if (frm.doc.docstatus > 0 && frm.doc.hostel_fee_applicable == "YES") {
			frm.add_custom_button(__('Accounting Ledger'), function () {
				frappe.route_options = {
					voucher_no: frm.doc.hostel_fees,
					from_date: frm.doc.posting_date,
					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
					company: frm.doc.company,
					group_by: '',
					show_cancelled_entries: frm.doc.docstatus === 2
				};
				frappe.set_route("query-report", "General Ledger");
			}, __("View"));
		}
	}
})

frappe.ui.form.on("Student Hostel Admission", "student", function (frm) {
	if (frm.doc.student == undefined || frm.doc.student == "" || frm.doc.student == null){

	}else{
	frappe.model.with_doc("Student", frm.doc.student, function () {
		frm.clear_table("current_education_fetch");
		var tabletransfer = frappe.model.get_doc("Student", frm.doc.student);
		cur_frm.doc.current_education = "";
		cur_frm.refresh_field("current_education");
		$.each(tabletransfer.current_education, function (index, row) {
			var d = frappe.model.add_child(cur_frm.doc, "Current Educational Details", "current_education_fetch");
			d.programs = row.programs;
			d.semesters = row.semesters;
			d.academic_year = row.academic_year;
			d.academic_term = row.academic_term;
			cur_frm.refresh_field("current_education_fetch");
		});
	});
}

});

frappe.ui.form.on("Student Hostel Admission", "hostel_fee_structure", function (frm) {
	if (frm.doc.hostel_fee_structure == undefined || frm.doc.hostel_fee_structure == "" || frm.doc.hostel_fee_structure == null){

	}else{
	frappe.model.with_doc("Fee Structure Hostel", frm.doc.hostel_fee_structure, function () {
		var tabletransfer = frappe.model.get_doc("Fee Structure Hostel", frm.doc.hostel_fee_structure)
		frm.clear_table("hostel_fee_components");
		$.each(tabletransfer.components, function (index, row) {
			var d = frappe.model.add_child(cur_frm.doc, "Fee Component", "hostel_fee_components");
			d.fees_category = row.fees_category;
			d.description = row.description;
			d.amount = row.amount;
			d.waiver_type = row.waiver_type;
			d.percentage = row.percentage;
			d.waiver_amount = row.waiver_amount;
			d.total_waiver_amount = row.total_waiver_amount;
			d.receivable_account = row.receivable_account;
			d.income_account = row.income_account;
			d.company = row.company;
			d.grand_fee_amount = row.grand_fee_amount;
			d.outstanding_fees = row.outstanding_fees;
			cur_frm.refresh_field("hostel_fee_components");
		})
	});
}
});
