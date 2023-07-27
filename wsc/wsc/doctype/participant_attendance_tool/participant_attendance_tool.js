// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant Attendance Tool', {
	refresh: function(frm) {

	},
	based_on: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.get_participant_group',
			args:{
				based_on : frm.doc.based_on
			},
			callback: function(result){
				frm.set_df_property('participant_group', 'options', result.message) // participant_group
			}
		})
	},
	participant_group: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.get_details',
			args: {
				participant_group_id : frm.doc.participant_group
			},
			callback: function(result){
				frm.set_value("academic_year", result.message[0]) // academic year
				frm.set_value("academic_term", result.message[1]) // acadmic term
				frm.set_value("select_course", result.message[2]) // course
				frm.set_value("select_module", result.message[3]) // module
				frm.set_df_property('instructor_id', 'options', result.message[4]) // instructor_id
				frm.set_df_property('select_sub_module', 'options', result.message[5]) // sub module
			}
		})
	},
	instructor_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.get_instructor_name',
			args: {
				participant_group_id: frm.doc.participant_group,
				instructor_id: frm.doc.instructor_id
			},
			callback: function(result){
				frm.set_value("instructor_name", result.message)
			}
		})
	},
	get_participants: function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.get_participants',
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
	}	
});
