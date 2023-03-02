// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter applications in the link field based on employee allotment status
frappe.ui.form.on("Application for Residence De-Allotment", {
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

frappe.ui.form.on('Application for Residence De-Allotment',{
	refresh: function(frm){
		if(frm.doc.current_application_status=="Applied"){
			frm.add_custom_button(__("Residence De-Allotment"), function() {
			frm.events.residence_deallotments(frm)
		});
		}
	},
	residence_deallotments: function(frm) {
		return frappe.call({
			method: "wsc.wsc.doctype.residence_de_allotment.residence_de_allotment.residence_deallotments",
			args: {
				"residence_de_allotment_application_number": frm.doc.residence_de_allotment_application_number,
				"reason_for_de_allotment": frm.doc.reason_for_de_allotment,
				"residence_allotment_number": frm.doc.residence_allotment_number,
				"application_number": frm.doc.application_number,
				"start_date": frm.doc.start_date,
				"changed_residence_serial_number": frm.doc.changed_residence_serial_number,
				"changed_residence_number": frm.doc.changed_residence_number,
				"employee_name": frm.doc.employee_name,
				"employee_id": frm.doc.employee_id,
				"changed_building_name": frm.doc.changed_building_name,
				"changed_residence_type": frm.doc.changed_residence_type,
				"changed_residence_type_name": frm.doc.changed_residence_type_name
			},
			callback: function(r) {
				var doc = frappe.model.sync(r.message);
				frappe.set_route("Form", doc[0].doctype, doc[0].name);
			}
		});}
});
