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

frappe.ui.form.on('Application for Residence',{
	refresh: function(frm){
		if(frm.doc.current_application_status=="Applied"|| frm.doc.current_application_status=="Pending for Approval") {
			frm.add_custom_button(__("Residence Allotment"), function() {
			frm.events.residence_allotment(frm)
		});
		}
	},
	residence_allotment: function(frm) {
		return frappe.call({
			method: "wsc.wsc.doctype.residence_allotment.residence_allotment.residence_allotments",
			args: {
				"application_number": frm.doc.application_number,
				"employee_name": frm.doc.employee_name,
				"employee_id": frm.doc.employee_id,
				"employee_email": frm.doc.employee_email,
				"designation": frm.doc.designation,
				"department": frm.doc.department,
				"type_of_residence_requested": frm.doc.type_of_residence_requested,
				"type_of_residence_name_requested": frm.doc.type_of_residence_name_requested
			},
			callback: function(r) {
				var doc = frappe.model.sync(r.message);
				frappe.set_route("Form", doc[0].doctype, doc[0].name);
			}
		});}
});

