// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Participant Attendance', {

	participant_group: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.get_details',
			args: {
				participant_group_id: frm.doc.participant_group
			},
			callback: function(result){
				frm.set_value("academic_year", result.message[0]) // academic_year
				frm.set_value("academic_term", result.message[1]) // academic_term
				frm.set_value("select_course", result.message[2]) // course
				frm.set_value("select_module", result.message[3]) // module
				frm.set_df_property('select_sub_module', 'options', result.message[4]) // sub module
				frm.set_df_property('instructor_id', 'options', result.message[5]) // instructors
				frm.set_df_property('participant_id', 'options', result.message[6]) // participants
			}
		})
	},
	instructor_id: function(frm){
		//  set the participant name from the course enrollment
		frappe.call({
			method: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.get_instructor_name',
			args: {
				participant_group_id : frm.doc.participant_group,
				instructor_id: frm.doc.instructor_id
			},
			callback: function(result){
				frm.set_value("instructor_name", result.message)
			}
		})
	},	
	participant_id: function(frm){
		//  set the participant name from the course enrollment
		frappe.call({
			method: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.get_participant_name',
			args: {
				participant_group_id : frm.doc.participant_group,
				participant_id: frm.doc.participant_id
			},
			callback: function(result){
				frm.set_value("participant_name", result.message)
			}
		})
	}
});
