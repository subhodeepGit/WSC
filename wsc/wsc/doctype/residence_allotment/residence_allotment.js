// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter building in the link field based on building type
frappe.ui.form.on("Residence Allotment", {
	setup: function(frm) {
		frm.set_query("building", function() {
			return {
				filters: [
					["Buildings","building_type", "=", "Residential"],
                    
				]
			}
		
		});
	}
});

// To filter residence serial number in the link field based on selected building and which are allottable
frappe.ui.form.on("Residence Allotment", {
	setup: function(frm) {
		frm.set_query("residence_serial_number", function() {
			return {
				filters: [
					["Building Room","building_name", "in", [frm.doc.building]],
					["Building Room","allotment_status" , '=' ,"Allottable"],
					["Building Room","vacancy_status" , '=' ,"Vacant"]

                    
				]
			}
		
		});
	}
});

// // To validate if start date is not past dated
// frappe.ui.form.on("Residence Allotment", {
//     validate: function(frm) {
//         if (frm.doc.start_date < get_today()) {
//             frappe.throw(__("Please select a start date from the present or future."));
//         }
//     },
// });

// To validate end date is not before start date
frappe.ui.form.on("Residence Allotment", {
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





