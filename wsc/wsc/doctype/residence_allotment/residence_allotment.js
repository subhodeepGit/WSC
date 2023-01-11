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





