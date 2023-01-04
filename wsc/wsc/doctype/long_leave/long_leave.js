// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Long Leave', {
	setup: function (frm) {
		frm.set_query("allotment_number", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query"
			};
		});
		// frm.set_value('data_11', 'Problem not Resolved')
	}
});
