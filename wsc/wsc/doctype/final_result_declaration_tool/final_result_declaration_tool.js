// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Result Declaration Tool', {
	// refresh: function(frm) {

	// },
	participant_group: function(frm){
		// based on the participant group, set the course, module, sub-module list, assignment_list, participant list
		frappe.call({
			method: 'wsc.wsc.doctype.final_result_declaration_tool.final_result_declaration_tool.get_details',
			args: {
				participant_group_id : frm.doc.participant_group
			},
			callback: function(result){
				frm.set_value("academic_year", result.message[0]) // academic_year
				frm.set_value("academic_term", result.message[1]) // academic_term
				frm.set_value("select_module", result.message[2]) // course
				frm.set_value("select_course", result.message[3]) // module
				frm.set_df_property('participant_id', 'options', result.message[4]) // participants
				frm.set_value("course_name", result.message[5]) // course name
				frm.set_value("course_code", result.message[6]) // course code
				frm.set_value("no_of_participants", result.message[7]) // course code
			}
		})
	},
	get_participants : function(frm){
		frappe.call({
			
			method: 'wsc.wsc.doctype.final_result_declaration_tool.final_result_declaration_tool.get_participants',
			args: {
				participant_group_id: frm.doc.participant_group
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participants')
					result.message.forEach(element => {
						var childTable = frm.add_child('participants')
						childTable.participant_id = element.participant
						childTable.participant_name = element.participant_name
					})
				}
				frm.refresh()
				frm.refresh_field('participants')
			}
		})
	},
});
