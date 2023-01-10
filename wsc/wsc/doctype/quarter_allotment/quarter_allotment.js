// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt



// To filter quarter number in the link field based on selected building
frappe.ui.form.on("Quarter Allotment", {
	setup: function(frm) {
		frm.set_query("quarter_number", function() {
			return {
				filters: [
					["Building Room","building_name", "in", [frm.doc.building]],
                    
				]
			}
		
		});
	}
});

// To filter Buiuldings which are residential
frappe.ui.form.on("Quarter Allotment", {
	setup: function(frm) {
		frm.set_query("building", function() {
			return {
				filters: [
					["Buildings","building_type" , '=' ,"Residential"],
                    
				]
			}
		
		});
	}
});
