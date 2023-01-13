// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt


frappe.ui.form.on("allotted_residence_serial_number", {
	setup: function(frm) {
		frm.set_query("residence_serial_number", function() {
			return {
				filters: [
					["Building Room","vacancy_status" , '=' ,"Not Vacant"]

                    
				]
			}
		
		});
	}
});
