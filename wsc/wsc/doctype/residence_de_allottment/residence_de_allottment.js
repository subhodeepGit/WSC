// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter applications in the link field based on ithe application status
frappe.ui.form.on("Residence De-Allottment", {
	setup: function(frm) {
		frm.set_query("residence_de_allotment_application_number", function() {
			return {
				filters: [
					["Application for Residence De-Allottment","current_application_status", "=", "Applied"]
                    
				]
			}
		
		});
	}
});

frappe.ui.form.on("Residence De-Allottment", {
	setup: function(frm) {
		frm.set_query("allotted_residence_serial_number", function() {
			return {
				filters: [
					["Residence Allotment","vacancy_status" , '=' ,"Not Vacant"],
					["Residence Allotment","employee_allotment_status" , '=' ,"Alloted"]

                    
				]
			}
		
		});
	}
});