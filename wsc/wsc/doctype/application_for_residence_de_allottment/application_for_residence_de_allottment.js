// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter applications in the link field based on employee allotment status
frappe.ui.form.on("Application for Residence De-Allottment", {
	setup: function(frm) {
		frm.set_query("residence_allotment_number", function() {
			return {
				filters: [
					["Residence Allotment","current_employee_allotment_status", "=", "Alloted"]
				]
			}
		
		});
	}
});
