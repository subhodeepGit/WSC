// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment Declaration', {
	// refresh: function(frm) {

	// }
	// participant_group: function(frm){
	// 	frappe.call({
	// 		method : 'wsc.wsc.doctype.assignment_declaration.assignment_declaration.get_details',
	// 		args: {
	// 			participant_group_id: frm.doc.participant_group
	// 		},
	// 		callback: function(result){
	// 			if(result.message){
	// 				frm.set_value("course", result.message[2])
	// 				frm.set_value("module", result.message[3])
	// 				frm.set_df_property('select_sub_module', 'options', result.message[5])
	// 				frm.set_value("academic_year", result.message[0])
	// 				frm.set_value("academic_term", result.message[1])
	// 				frm.set_df_property('trainer_id', 'options', result.message[4])
	// 			}
	// 		}
	// 	})
	// },
	participant_group: function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.assignment_declaration.assignment_declaration.get_details',
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
					frm.set_df_property('trainer_id', 'options', result.message[4])
					frm.set_df_property('select_assessment_criteria', 'options', result.message[6])
				}
			}
		})
	},
	trainer_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_declaration.assignment_declaration.get_instructor_name',
			args:{
				participant_group_id : frm.doc.participant_group,
				instructor_id: frm.doc.trainer_id
			},
			callback: function(result){
				if(result.message){
					frm.set_value("trainer_name", result.message)
				}
			}
		})
	},
	get_participant: function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.assignment_declaration.assignment_declaration.get_participants',
			args: {
				participant_group_id: frm.doc.participant_group
			},
			callback: function(result){
				alert(200)
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participant_list')
					result.message.forEach(element => {
						var childTable = frm.add_child('participant_list')
						childTable.participant_id = element.participant
						childTable.participant_name = element.participant_name
					})
				}
				frm.refresh()
				frm.refresh_field('participant_list')
			}
		})
	},
	select_assessment_criteria: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_declaration.assignment_declaration.get_criteria_details',
			args:{
				course: frm.doc.module,
				assessment_criteria : frm.doc.select_assessment_criteria
			},
			callback: function(result){
				frm.set_value("total_marks", result.message[0])
				frm.set_value("pass_marks", result.message[1])
				frm.set_value("weightage", result.message[2])
			}
		})
	}
});
