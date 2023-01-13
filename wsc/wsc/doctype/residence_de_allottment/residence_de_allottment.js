// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter alloted residence serial number in the link field based on vacancy status and employee allotment status
frappe.ui.form.on("Residence De-Allottment", {
	setup: function(frm) {
		frm.set_query("allotted_residence_serial_number", function() {
			return {
				filters: [
					["Building Room","vacancy_status", '=' , "Not Vacant"],
					["Building Room", "employee_allotment_status", '=' , "Alloted"]

                    
				]
			}
		
		});
	}
});
