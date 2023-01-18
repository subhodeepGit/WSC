// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt


// To filter residence serial number in the link field based on selected Residence Type name
frappe.ui.form.on('Residence Change Request', {
	setup: function(frm) {
		frm.set_query("residence_serial_number", function() {
			return {
				filters: [
					["Building Room","residence_type_name", "in", [frm.doc.residence_type_name]],
					["Building Room","employee_allotment_status", '=', "Not Alloted"]
                    
				]
			}
		
		});
	}
});