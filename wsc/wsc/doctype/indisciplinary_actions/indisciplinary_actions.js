// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Indisciplinary Actions', {
	setup: function (frm) {
		frm.set_query("indisciplinary_complaint_registration_id", function () {
			return {
				query: "wsc.wsc.doctype.indisciplinary_actions.indisciplinary_actions.status_query"
			};
		});
	}
})



frappe.ui.form.on("Indisciplinary Actions", "indisciplinary_complaint_registration_id", function (frm) {
	if (frm.doc.indisciplinary_complaint_registration_id == undefined || frm.doc.indisciplinary_complaint_registration_id == "" || frm.doc.indisciplinary_complaint_registration_id == null) {

	} else {
		frappe.model.with_doc("Indisciplinary Complaint Registration", frm.doc.indisciplinary_complaint_registration_id, function () {
			var tabletransfer = frappe.model.get_doc("Indisciplinary Complaint Registration", frm.doc.indisciplinary_complaint_registration_id);
			cur_frm.doc.student_fetch = "";
			cur_frm.refresh_field("student_fetch");
			$.each(tabletransfer.student, function (index, row) {
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

// Checking duplicate 
// frappe.ui.form.on("DC Members", "emp_id", function (frm, cdt, cdn) {
// 	var emp_id = frm.doc.dc_member;
// 	var arr = [];
// 	for (var i in emp_id) {
// 		arr.push(emp_id[i].emp_id);

// 	}
// 	for (var j = 0; j < arr.length - 1; j++) {
// 		for (var k = j + 1; k < arr.length; k++) {
// 			if (arr[j] == arr[k]) {
// 				frappe.msgprint("Duplicate entry " + arr[k])
// 			}
// 		}
// 	}
// })




