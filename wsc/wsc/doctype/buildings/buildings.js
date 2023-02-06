// Copyright (c) 2022, SOUL Limited and contributors
// For license information, please see license.txt

////To filter districts based on the selected state link field
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

//To fetch only those buildings which are between start and end date of the Land with respect to today’s date
frappe.ui.form.on("Buildings", {
	setup: function(frm) {
		frm.set_query("plot_number", function() {
			return {
                query: "wsc.wsc.doctype.buildings.buildings.room_type_query",
			}
		});
	}
});

// To validate end date is not before start date
frappe.ui.form.on("Buildings", {
    start_date: function(frm) {
        frm.fields_dict.end_date.datepicker.update({
            minDate: frm.doc.start_date ? new Date(frm.doc.start_date) : null
        });
    },

    end_date: function(frm) {
        frm.fields_dict.start_date.datepicker.update({
            maxDate: frm.doc.end_date ? new Date(frm.doc.end_date) : null
        });
    },
});

