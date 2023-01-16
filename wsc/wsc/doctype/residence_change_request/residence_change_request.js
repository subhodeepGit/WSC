// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt


// To filter Alloted Residence Serial Number in the link field based on selected Employee
frappe.ui.form.on('Residence Change Request', {
	setup: function(frm) {
		frm.set_query("alloted_residence_serial_number", function() {
			return {
				filters: [
					["Residence Allotment","employee", "in", [frm.doc.employee]],
					["Residence Allotment","docstatus", '=', 1]
                    
				]
			}
		
		});
	}
});

// To filter residence type name in the link field based on selected type of residence
frappe.ui.form.on('Residence Change Request', {
	setup: function(frm) {
		frm.set_query("residence_type_name", function() {
			return {
				filters: [
					["Residence Type","type_of_residence", "in", [frm.doc.residence_type_requested]],
                    
				]
			}
		
		});
	}
});

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