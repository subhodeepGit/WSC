// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on("Withdrawal of Inward Suspension Letter", "inward_suspension_letter_id", function(frm){
	frappe.model.with_doc("Inward Suspension Letter", frm.doc.inward_suspension_letter_id, function(){
		var tabletransfer = frappe.model.get_doc("Inward Suspension Letter", frm.doc.inward_suspension_letter_id);
		cur_frm.doc.student_fetch = "";
		cur_frm.refresh_field("student_fetch");
		$.each(tabletransfer.student, function(index, row){
			var d = frappe.model.add_child(cur_frm.doc, "Inward Suspension Letter Student", "student_fetch");
			d.allotment_number = row.allotment_number;
			d.student = row.student;
			d.student_name = row.student_name;
			d.hostel = row.hostel;
			cur_frm.refresh_field("student_fetch");
		});
	});
});