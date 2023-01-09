// Copyright (c) 2022, SOUL Limited and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Buildings', {
// 	 function(frm) {
// 		frm.set_query("districts", function() {
// 			return {
// 				 filters: {
// 				   "state":frm.doc.state
// 				 }
// 			 };
// 		 });
// 	}
// });


frappe.ui.form.on("Buildings", {
	setup: function(frm) {
		frm.set_query("plot_number", function() {
			return {
                query: "wsc.wsc.doctype.buildings.buildings.room_type_query",
			}
		});
	}
});
