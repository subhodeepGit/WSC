// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Clearance', {
	setup: function (frm) {
		frm.set_query("allotment_number", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query"
			};
		});
	},
	due_status: function (frm) {
		if(frm.doc.due_status!="Dues"){
			frm.set_value("due_amount", "");
			frm.set_value("reason_of_due", "");
		}
	}
});
