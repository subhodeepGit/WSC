// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter residence type name in the link field based on selected type of residence
frappe.ui.form.on('Application for Residence', {
	setup: function(frm) {
		frm.set_query("type_of_residence_name_requested", function() {
			return {
				filters: [
					["Residence Type","type_of_residence", "in", [frm.doc.type_of_residence_requested]],
                    
				]
			}
		
		});
	}
});