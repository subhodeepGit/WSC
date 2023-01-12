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
	}
});

// To filter out buildings which are currently between start and end date
frappe.ui.form.on("Building Room", {
	setup: function(frm) {
		frm.set_query("building_name", function() {
			return {
                query: "wsc.wsc.doctype.building_room.building_room.room_type_query",
			}
		});
	}
});



