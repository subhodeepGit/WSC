// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// To filter Academic Term in the link field based on selected Academic Year
frappe.ui.form.on('Rewards and Achievements', {
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
frappe.ui.form.on('Rewards and Achievements', {
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
frappe.ui.form.on('Rewards and Achievements', {
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

frappe.ui.form.on('Rewards and Achievements', {
	"get_students": function(frm) {
		cur_frm.clear_table("topper_scholarship_table")
		frappe.call({
			method: "wsc.wsc.doctype.rewards_and_achievements.rewards_and_achievements.get_students",
			args:{
				programs:frm.doc.programs,
				semester:frm.doc.semester,
				academic_year:frm.doc.academic_year,
				academic_term:frm.doc.academic_term,
				no_of_merit_student:frm.doc.no_of_merit_student
			},
			callback: function(r) {
				if(r.message) {
					r.message.forEach(element => {
						var c = frm.add_child("topper_scholarship_table")
						c.student_id = element.student,
						c.student_name = element.student_name,
						c.percentage= element.percentage,
						c.rank= element.rank

					});
				}
				frm.refresh();
				frm.refresh_field("topper_scholarship_table")
			}
		});
	}
});

frappe.ui.form.on('Rewards and Achievements', {
	"get_cutoff_students": function(frm) {
		cur_frm.clear_table("cutoff_scholarship_table");
		frappe.call({
			method: "wsc.wsc.doctype.rewards_and_achievements.rewards_and_achievements.get_cutoffStudents",
			args:{
				programs:frm.doc.programs,
				semester:frm.doc.semester,
				academic_year:frm.doc.academic_year,
				academic_term:frm.doc.academic_term,
				lower_cutoff_percentage:frm.doc.lower_cutoff_percentage,
				upper_cutoff_percentage:frm.doc.upper_cutoff_percentage
			},
			callback: function(r) {
				if(r.message) {
					r.message.forEach(element => {
						var c = frm.add_child("cutoff_scholarship_table")
						c.student_id = element.student,
						c.student_name = element.student_name,
						c.percentage= element.percentage

					});
				}
				frm.refresh();
				frm.refresh_field("cutoff_scholarship_table")
			}
		});
	}
});

frappe.ui.form.on('Rewards and Achievements', {
	semester: function(frm) {
		cur_frm.clear_table("topper_scholarship_table");
		frm.set_value("upper_cutoff_percentage", "");
		frm.set_value("lower_cutoff_percentage", "");
		cur_frm.clear_table("cutoff_scholarship_table");
		refresh_field("topper_scholarship_table");
		refresh_field("upper_cutoff_percentage");
		refresh_field("lower_cutoff_percentage");
		refresh_field("cutoff_scholarship_table");
					}
				}
			);
		

frappe.ui.form.on('Rewards and Achievements', {
	onload: function(frm) {

		frm.get_field('topper_scholarship_table').grid.cannot_add_rows = true;
	}
});

frappe.ui.form.on('Rewards and Achievements', {
	onload: function(frm) {

		frm.get_field('cutoff_scholarship_table').grid.cannot_add_rows = true;
	}
});

frappe.ui.form.on('Rewards and Achievements', {
	type_of_scholarship: function(frm) {
		cur_frm.clear_table("topper_scholarship_table");
		frm.set_value("upper_cutoff_percentage", "");
		frm.set_value("no_of_merit_student", "");
		frm.set_value("lower_cutoff_percentage", "");
		cur_frm.clear_table("cutoff_scholarship_table");
		refresh_field("topper_scholarship_table");
		refresh_field("no_of_merit_student");
		refresh_field("upper_cutoff_percentage");
		refresh_field("lower_cutoff_percentage");
		refresh_field("cutoff_scholarship_table");
					}
				}
			);
