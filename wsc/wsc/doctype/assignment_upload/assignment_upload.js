// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment Upload', {
	// refresh: function(frm) {

	// }
	participant_group: function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.assignment_upload.assignment_upload.get_details',
			args: {
				participant_group_id: frm.doc.participant_group
			},
			callback: function(result){
				if(result.message){
					frm.set_value("programs", result.message[0])
					frm.set_value("course", result.message[1])
					frm.set_df_property('topic', 'options', result.message[2])
					frm.set_value("academic_year", result.message[3])
					frm.set_value("academic_term", result.message[4])
					frm.set_df_property('participant_id', 'options', result.message[5])
					frm.set_df_property('instructor_id', 'options', result.message[6])
				}
			}
		})
	},
	participant_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_upload.assignment_upload.get_participant_name',
			args:{
				participant_group_id : frm.doc.participant_group,
				participant_id : frm.doc.participant_id
			},
			callback: function(result){
				// alert(JSON.stringify(result))
				if(result.message){
					frm.set_value("participant_name",result.message)
				}
			}
		})
	},
	instructor_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_upload.assignment_upload.get_instructor_name',
			args: {
				participant_group_id: frm.doc.participant_group,
				instructor_id: frm.doc.instructor_id
			},
			callback: function(result){
				frm.set_value("instructor_name", result.message)
			}
		})
	},	
	instructor_name: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_upload.assignment_upload.get_assignment_list',
			args: {
				instructor_name: frm.doc.instructor_name,
				participant_group_id : frm.doc.participant_group,
				programs : frm.doc.programs,
				course: frm.doc.course,
				topic : frm.doc.topic
			},
			callback: function(result){
				if(result.message){
					frm.set_df_property('assignment_number', 'options', result.message)
				}
			}
		})
	},
	assignment_number: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_upload.assignment_upload.get_assignment_details',
			args:{
				assignment_name : frm.doc.assignment_number
			},
			callback: function(result){
				if(result.message){
					frm.set_value("assessment_component", result.message[0])
					frm.set_value("total_marks", result.message[1])
					frm.set_value("passing_marks", result.message[2])
					frm.set_value("weightage", result.message[3])
				}
			}
		})
	}
});

