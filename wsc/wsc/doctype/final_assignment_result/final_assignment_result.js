// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Assignment Result', {
	setup:function(frm){
		frm.set_df_property('participant_group', 'cannot_add_rows', true);
		frm.set_df_property('participant_group', 'cannot_delete_rows', true);
		frm.set_df_property('assessment_result_item', 'cannot_add_rows', true);
		frm.set_df_property('assessment_result_item', 'cannot_delete_rows', true);
	},
	refresh: function(frm) {
		frm.set_query("tot_participant_enrollment", function() {
            return {
                filters: {
                    'docstatus': 1,
                }
            };
        });
		frm.set_query("participant_id", function() {
			return {
				query: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.get_participant_id',
				filters: {
					"tot_participant_enrollment":frm.doc.tot_participant_enrollment,
				}
			};
		});
	},
	tot_participant_enrollment: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.participant_group',
			args: {
				tot_participant_enrollment : frm.doc.tot_participant_enrollment
			},
			callback: function(r) {
				if (r.message){
					frappe.model.clear_table(frm.doc, 'participant_group');
					(r.message).forEach(element => {
						var c = frm.add_child("participant_group")
						c.participant_group=element.name
						c.participant_group_name=element.participant_group
						c.course_type=element.course_type
						c.course=element.course
						c.module_name=element.module_name
						c.module_code=element.module_code
						c.mode=element.mode
					})
					frm.refresh_field("participant_group")
				}
			}
		}),
		frappe.call({
			method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.module',
			args: {
				course : frm.doc.programs
			},
			callback: function(r) {
				if (r.message){
					frappe.model.clear_table(frm.doc, 'modules');
					(r.message).forEach(element => {
						var c = frm.add_child("modules")
						c.course=element.course
						c.course_name=element.course_name
						c.course_code=element.course_code
						c.required=element.required
						c.modes=element.modes
						c.year_end_date=element.year_end_date
						c.is_disable=element.is_disable
					})
					frm.refresh_field("modules")
				}
			}
		})
	},
	// setup: function(frm){
	// 	frm.set_query("instructor_id", function() {
	// 		return {
	// 			query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.instructor',
	// 			filters:{"participant_group_id":frm.doc.participant_group}
				
	// 		};
	// 	});

	// 	frm.set_query("participant_id", function() {
	// 		return {
	// 			query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.participant',
	// 			filters:{"participant_group_id":frm.doc.participant_group}
				
	// 		};
	// 	});
	// },
	// participant_group: function(frm){
	// 	// based on the participant group, set the course, module, sub-module list, assignment_list, participant list
	// 	frappe.call({
	// 		method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.get_details',
	// 		args: {
	// 			participant_group_id : frm.doc.participant_group
	// 		},
	// 		callback: function(result){
	// 			frm.set_value("academic_year", result.message[0]) // academic_year
	// 			frm.set_value("academic_term", result.message[1]) // academic_term
	// 			frm.set_value("module", result.message[2]) // course
	// 			frm.set_value("course", result.message[3]) // module
	// 			// frm.set_df_property('participant_id', 'options', result.message[4]) // participants
	// 			frm.set_value("course_name", result.message[5]) // course name
	// 			frm.set_value("course_code", result.message[6]) // course code
	// 		}
	// 	})
	// },
	// participant_id: function(frm){
	// 	frappe.call({
	// 		method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.get_participant_details',
	// 		args:{
	// 			participant_group_id: frm.doc.participant_group,
	// 			participant_id: frm.doc.participant_id
	// 		},
	// 		callback: function(result){
	// 			frm.set_value("participant_name", result.message[0])
	// 			frm.set_value("attendance_percentage", result.message[1])
	// 		}
	// 	})
	// },
	get_result: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.get_assignments',
			args:{
				frm:frm.doc
				// participant_id : frm.doc.participant_id,
				// grading_scale : frm.doc.grading_scale
			},
			// callback: function(result){
			// 	if(result.message){
			// 		frappe.model.clear_table(frm.doc, 'assessment_result_item')
			// 		result.message[0].forEach(element => {
			// 			var childTable = frm.add_child('assessment_result_item')
			// 			childTable.assignment_id = element.select_assignment
			// 			childTable.assignment_name = element.assignment_name
			// 			childTable.assessment_criteria = element.assessment_criteria
			// 			childTable.earned_marks = element.marks_earned
			// 			childTable.total_marks = element.total_marks
			// 			childTable.percentage = element.percentage
			// 			childTable.grade = element.grade_code
			// 			childTable.result = element.result
			// 		})
			// 	}
			// 	frm.refresh()
			// 	frm.refresh_field('assessment_result_item')

			// 	frm.set_value("overall_percentage", result.message[1]) //overall grade
			// 	frm.set_value("overall_grade", result.message[2]) // overall percentage
			// 	frm.set_value("overall_result", result.message[3]) // overall result
			// }
		})
	}
});
