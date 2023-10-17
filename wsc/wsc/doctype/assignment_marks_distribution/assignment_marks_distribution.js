// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment Marks Distribution', {
	refresh: function(frm) {
		frm.set_query("course", function() {
            return {
                filters: {
                    "is_short_term_course":"Yes",
					"is_tot":1,
					"disable":0
                }
            };
        });
		frm.set_query("assessment_criteria", function() {
			return {
				query: 'wsc.wsc.doctype.assignment_marks_distribution.assignment_marks_distribution.criteria',
				filters:{"course":frm.doc.course}
				
			};
		})
	},
	assessment_criteria: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment.assignment.get_criteria_details',
			args:{
				course: frm.doc.course,
				assessment_criteria : frm.doc.assessment_criteria
			},
			callback: function(result){
				frm.set_value("total_marks", result.message[0])
				frm.set_value("passing_marks", result.message[1])
				frm.set_value("weightage", result.message[2])
			}
		})
	},
});


frappe.ui.form.on('Assignment Marks Distribution Child', {
	passing_marks: function(frm, cdt, cdn){
		var d = locals[cdt][cdn];
		if(d.passing_marks > d.total_marks){
			d.passing_marks=''
			refresh_field("passing_marks", d.name, d.parentfield);
			frappe.msgprint("Passing Marks should not be more than Total Marks");
		} else if (d.passing_marks < 0){
			d.passing_marks=''
			refresh_field("passing_marks", d.name, d.parentfield);
			frappe.msgprint("Passing Marks should not be Negative");
		}
		if(!d.total_marks){
			d.passing_marks=''
			refresh_field("passing_marks", d.name, d.parentfield);
			frappe.msgprint("Please enter Total Marks first");
		}
	},
	assignment_marks_distribution_child_add: function(frm){
		frm.fields_dict['assignment_marks_distribution_child'].grid.get_field('assignment_name').get_query = function(doc){
			var assignment_name_list = [];
			if(!doc.__islocal) assignment_name_list.push(doc.name);
			$.each(doc.assignment_marks_distribution_child, function(idx, val){
				if (val.assignment_name) assignment_name_list.push(val.assignment_name);
			});
			return { filters: [['Assignment Name', 'name', 'not in', assignment_name_list]] };
		};
	}
});
