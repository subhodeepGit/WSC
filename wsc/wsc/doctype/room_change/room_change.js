// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Change', {
	setup: function (frm) {
		frm.set_query("preferred_room", function () {
			return {
				filters: [
					["Room Masters", "hostel_id", "=", frm.doc.preferred_hostel],
					["Room Masters", "validity", "=", "Functional"],
					["Room Masters", "status", "=", "Functional"],
					["Room Masters", "vacancy", ">", 0],
					["Room Masters", "room_number", "!=", frm.doc.room_no]
				]
			}
		});
		frm.set_query("allotment_number", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query"
			};
		});
		frm.set_query("preferred_hostel", function() {
			return {
				query: "wsc.wsc.doctype.room_allotment.room_allotment.test_query"
			};
		});
	},
	preferred_hostel:function(frm){
		frm.set_value('preferred_room','')
		frm.set_value('preferred_room_type','')
		frm.set_value('preferred_room_number','')
	}
})

