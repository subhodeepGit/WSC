// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment Evaluation Tool', {
	// refresh: function(frm) {

	// }

	participant_group: function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_details',
			args: {
				participant_group_id: frm.doc.participant_group
			},
			callback: function(result){
				if(result.message){
					frm.set_value("course", result.message[2])
					frm.set_value("module", result.message[3])
					frm.set_df_property('select_sub_module', 'options', result.message[5])
					frm.set_value("academic_year", result.message[0])
					frm.set_value("academic_term", result.message[1])
					frm.set_df_property('instructor_id', 'options', result.message[4])
					frm.set_df_property('participant_id', 'options', result.message[6])
					frm.set_value("total_participants", result.message[7])
				}
			}
		})
	},
	instructor_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_instructor_name',
			args: {
				participant_group_id: frm.doc.participant_group,
				instructor_id: frm.doc.instructor_id
			},
			callback: function(result){
				frm.set_value("instructor_name", result.message)
			}
		})
	},
	select_sub_module: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_assignment_list',
			args:{
				instructor_id: frm.doc.instructor_id,
				participant_group_id : frm.doc.participant_group,
				programs : frm.doc.course,
				course: frm.doc.module,
				topic : frm.doc.select_sub_module
			},
			callback: function(result){
				frm.set_df_property('select_job_sheetassessment', 'options', result.message)  // select assignment
			}
		})
	},
	get_participants : function(frm){
		frappe.call({
			
			method: 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_participants',
			args: {
				participant_group_id: frm.doc.participant_group
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participant_details_data')
					result.message.forEach(element => {
						var childTable = frm.add_child('participant_details_data')
						childTable.participant_id = element.participant
						childTable.participant_name = element.participant_name
					})
				}
				frm.refresh()
				frm.refresh_field('participant_details_data')
			}
		})
	},
	select_job_sheetassessment: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_assignment_details',
			args: {
				assignment_name : frm.doc.select_job_sheetassessment
			},
			callback: function(result){
				frm.set_value('assessment_criteria', result.message[0])
				frm.set_value("total_marks", result.message[1])
				frm.set_value("passing_marks", result.message[2])
				frm.set_value("weightage", result.message[3])
				frm.set_value('assignment_name', result.message[4])
			}
		})
	},

});
