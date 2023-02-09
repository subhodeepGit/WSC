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

frappe.ui.form.on('Application for Residence', {
	go_to_residence_allotment: function(frm) {
		frappe.set_route('List',"Residence Allotment")
	}
});

frappe.ui.form.on('Application for Residence', {
	refresh: function(frm) {
		frm.add_custom_button(__("Residence Allotment"), function() {
			frm.events.make_residence_allotment(frm);
		}, __('Action'));
		frm.page.set_inner_btn_group_as_primary(__('Action'))
		frm.set_value("Residence Allotment","application_number","application_number", frm.doc.application_number);
	}
});

