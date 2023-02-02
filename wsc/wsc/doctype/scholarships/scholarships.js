// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter Academic Term in the link field based on selected Academic Year
frappe.ui.form.on('Scholarships', {
	setup: function(frm) {
		frm.set_query("academic_term", function() {
			return {
				filters: [
					["Academic Term","academic_year", "in", [frm.doc.academic_year]],
                    
				]
			}
		
		});
	}
});

// To filter Programs in the link field based on selected Program Grade
frappe.ui.form.on('Scholarships', {
	setup: function(frm) {
		frm.set_query("programs", function() {
			return {
				filters: [
					["Programs","program_grade", "in", [frm.doc.program_grade]],
                    
				]
			}
		
		});
	}
});

// To filter Semester in the link field based on selected Programs
frappe.ui.form.on('Scholarships', {
	setup: function(frm) {
		frm.set_query("semester", function() {
			return {
				filters: [
					["Program","programs", "in", [frm.doc.programs]],
                    
				]
			}
		
		});
	}
});