// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Withdrawal of Suspension', {
	setup: function (frm) {
		frm.set_query("indisciplinary_action_id", function() {
			return {
				query: "wsc.wsc.doctype.withdrawal_of_suspension.withdrawal_of_suspension.type_query"
			};
		});
	}
})
frappe.ui.form.on("Withdrawal of Suspension", "indisciplinary_action_id", function(frm){
	if (frm.doc.indisciplinary_action_id == undefined || frm.doc.indisciplinary_action_id == "" || frm.doc.indisciplinary_action_id == null) {

	} else {
	frappe.model.with_doc("Indisciplinary Actions", frm.doc.indisciplinary_action_id, function(){
		var tabletransfer = frappe.model.get_doc("Indisciplinary Actions", frm.doc.indisciplinary_action_id);
		cur_frm.doc.student_fetch = "";
		cur_frm.refresh_field("student_fetch");
		$.each(tabletransfer.student_fetch, function(index, row){
			var d = frappe.model.add_child(cur_frm.doc, "Indisciplinary Complaint Registration Student", "student_fetch");
			d.allotment_number = row.allotment_number;
			d.student = row.student;
			d.student_name = row.student_name;
			d.allotment_type = row.allotment_type;
			d.room_number = row.room_number;
			d.room_type = row.room_type;
			cur_frm.refresh_field("student_fetch");
		});
	});
}
});