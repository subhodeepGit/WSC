// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Assignment Result', {
	refresh: function(frm) {

	},
	participant_group: function(frm){
		// based on the participant group, set the course, module, sub-module list, assignment_list, participant list
		frappe.call({
			method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.get_details',
			args: {
				participant_group_id : frm.doc.participant_group
			},
			callback: function(result){
				frm.set_value("academic_year", result.message[0]) // academic_year
				frm.set_value("academic_term", result.message[1]) // academic_term
				frm.set_value("module", result.message[2]) // course
				frm.set_value("course", result.message[3]) // module
				frm.set_df_property('participant_id', 'options', result.message[4]) // participants
				frm.set_value("course_name", result.message[5]) // course name
				frm.set_value("course_code", result.message[6]) // course code
			}
		})
	},
	participant_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.get_participant_name',
			args:{
				participant_group_id: frm.doc.participant_group,
				participant_id: frm.doc.participant_id
			},
			callback: function(result){
				frm.set_value("participant_name", result.message)
			}
		})
	},
	get_result: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.get_assignments',
			args:{
				participant_group_id : frm.doc.participant_group,
				participant_id : frm.doc.participant_id,
				grading_scale : frm.doc.grading_scale
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'assessment_result_item')
					result.message[0].forEach(element => {
						var childTable = frm.add_child('assessment_result_item')
						childTable.assignment_id = element.select_assignment
						childTable.assignment_name = element.assignment_name
						childTable.assessment_criteria = element.assessment_criteria
						childTable.earned_marks = element.marks_earned
						childTable.total_marks = element.total_marks
						childTable.percentage = element.percentage
						childTable.grade = element.grade_code
						childTable.result = element.result
					})
				}
				frm.refresh()
				frm.refresh_field('assessment_result_item')

				frm.set_value("overall_percentage", result.message[1]) //overall grade
				frm.set_value("overall_grade", result.message[2]) // overall percentage
				frm.set_value("overall_result", result.message[3]) // overall result
			}
		})
	}
});
