// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Death Deallotment', {
	setup: function (frm) {
		frm.set_query("student", function() {
			return {
				query: "wsc.wsc.doctype.death_deallotment.death_deallotment.ra_query"
			};
		});
	}
});

frappe.ui.form.on("Death Deallotment", "student", function(frm){
	frappe.model.with_doc("Room Allotment", frm.doc.student, function(){
		var tabletransfer = frappe.model.get_doc("Room Allotment", frm.doc.student);
		cur_frm.doc.guardians = "";
		cur_frm.refresh_field("guardians");
		$.each(tabletransfer.guardians, function(index, row){
			var d = frappe.model.add_child(cur_frm.doc, "Student Guardian", "guardians");
			d.guardian = row.guardian;
			d.guardian_name = row.guardian_name;
			d.relation = row.relation;
			cur_frm.refresh_field("guardians");
		});
	});
});
