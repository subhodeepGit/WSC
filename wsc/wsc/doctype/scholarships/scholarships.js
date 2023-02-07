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

frappe.ui.form.on('Scholarships', {
	"get_students": function(frm) {
		// frm.set_value("topper_scholarship_table",[]);
		frappe.call({
			method: "get_students",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					r.message.forEach(element => {
						var c = frm.add_child("topper_scholarship_table")
						c.student_id = element.student,
						c.student_name = element.student_name,
						c.sgpa= element.sgpa

					});
				}
				frm.refresh();
				frm.refresh_field("topper_scholarship_table")
			}
		});
	}
});

frappe.ui.form.on('Scholarships', {
	"get_cutoff_students": function(frm) {
		// frm.set_value("topper_scholarship_table",[]);
		frappe.call({
			method: "get_cutoffStudents",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					r.message.forEach(element => {
						var c = frm.add_child("cutoff_scholarship_table")
						c.student_id = element.student,
						c.student_name = element.student_name,
						c.sgpa= element.sgpa

					});
				}
				frm.refresh();
				frm.refresh_field("cutoff_scholarship_table")
			}
		});
	}
});