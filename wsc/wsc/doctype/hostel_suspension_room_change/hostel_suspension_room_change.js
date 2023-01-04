// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Suspension Room Change', {
	setup: function (frm) {
		frm.set_query("preferred_room", function () {
			return {
				filters: [
					["Room Masters", "hostel_id", "=", frm.doc.preferred_hostel],
					["Room Masters", "validity", "=", "Approved"],
					["Room Masters", "status", "=", "Allotted"],
					["Room Masters", "vacancy", ">", 0]
				]
			}
		});
		frm.set_query("allotment_number", function() {
			return {
				query: "wsc.wsc.doctype.hostel_suspension_room_change.hostel_suspension_room_change.ra_query"
			};
		});
		frm.set_query("preferred_hostel", function() {
			return {
				query: "wsc.wsc.doctype.room_allotment.room_allotment.test_query"
			};
		});
	}
})