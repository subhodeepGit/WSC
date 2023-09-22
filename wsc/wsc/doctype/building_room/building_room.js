// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt




// To filter residence type name in the link field based on selected type of residence
frappe.ui.form.on("Building Room", {
	setup: function(frm) {
		frm.set_query("residence_type_name", function() {
			return {
				filters: [
					["Residence Type","type_of_residence", "in", [frm.doc.type_of_residence]],
                    
				]
			}
		
		});
		frm.set_query("floor" , function() {
			return {
				filters:{
					"building_name":frm.doc.building_name
				}
			}
		})
	}
});

// To filter buildings which are currently between start and end date
frappe.ui.form.on("Building Room", {
	setup: function(frm) {
		frm.set_query("building_name", function() {
			return {
                query: "wsc.wsc.doctype.building_room.building_room.room_type_query",
			}
		});
	}
});

// To validate end date is not before start date
frappe.ui.form.on("Building Room", {
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

// To clear the values of Seationg Capacity and Room name once "Is scheduled" check is clicked
frappe.ui.form.on('Building Room', {
	is_scheduled: function(frm) {
		frm.set_value("seating_capacity", "");
		frm.set_value("room_name", "");
					}
				}
			);
