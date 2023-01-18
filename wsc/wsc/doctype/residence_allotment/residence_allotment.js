// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter applications in the link field based on ithe application status
frappe.ui.form.on("Residence Allotment", {
	setup: function(frm) {
		frm.set_query("application_number", function() {
			return {
				filters: [
					["Application for Residence","current_application_status", "!=", "Rejected"],
					["Application for Residence","current_application_status", "!=", "Alloted"],
					["Application for Residence","current_application_status", "!=", "Cancelled by Applicant"]
					
                    
				]
			}
		
		});
	}
});

// To filter residence type name in the link field based on selected residence type
frappe.ui.form.on("Residence Allotment", {
	setup: function(frm) {
		frm.set_query("residence_type_name", function() {
			return {
				filters: [
					["Residence Type","type_of_residence", "in", [frm.doc.residence_type]],
                    
				]
			}
		
		});
	}
});



// To filter building in the link field based on building type
frappe.ui.form.on("Residence Allotment", {
	setup: function(frm) {
		frm.set_query("building", function() {
			return {
				filters: [
					["Buildings","building_type", "=", "Residential"]
                    
				]
			}
		
		});
	}
});

// To filter residence serial number in the link field based on selected building and residence type name and also which are allottable & vacant
frappe.ui.form.on("Residence Allotment", {
	setup: function(frm) {
		frm.set_query("residence_serial_number", function() {
			return {
				filters: {
					"building_name": frm.doc.building,
					"allotment_status" :"Allottable",
					"vacancy_status":"Vacant",
					"residence_type_name" :frm.doc.residence_type_name

                    
				}
			}
		
		});
	}
});


// To validate end date is not before start date
frappe.ui.form.on("Residence Allotment", {
    start_date: function(frm) {
        frm.fields_dict.end_date.datepicker.update({
            minDate: frm.doc.start_date ? new Date(frm.doc.start_date) : null
        });
    },

    end_date: function(frm) {
        frm.fields_dict.start_date.datepicker.update({
            maxDate: frm.doc.end_date ? new Date(frm.doc.end_date) : null
        });
    },
});








