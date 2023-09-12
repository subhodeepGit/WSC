// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment', {
	refresh: function(frm){
		frm.set_value('evaluate', 1)
	},
	setup: function(frm){
		frm.set_query("instructor_id", function() {
			return {
				query: 'wsc.wsc.doctype.assignment.assignment.instructor',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});

		frm.set_query("participant_id", function() {
			return {
				query: 'wsc.wsc.doctype.assignment.assignment.participant',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});

		frm.set_query("assessment_criteria", function() {
			return {
				query: 'wsc.wsc.doctype.assignment.assignment.criteria',
				filters:{"course":frm.doc.course}
				
			};
		});
	},
	participant_group: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment.assignment.get_details',
			args: {
				participant_group_id : frm.doc.participant_group
			},
			callback: function(result){
				frm.set_value("academic_year", result.message[0]) // academic year
				frm.set_value("academic_term", result.message[1]) // acadmic term
				frm.set_value("programs", result.message[2]) // course
				frm.set_value("course", result.message[3]) // module
			}
		})
	},
	instructor_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment.assignment.get_instructor_name',
			args: {
				participant_group_id: frm.doc.participant_group,
				instructor_id: frm.doc.instructor_id
			},
			callback: function(result){
				frm.set_value("instructor_name", result.message)
			}
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
	}
});
