// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// ------------------------------------------------------------------------------------------------------------
frappe.ui.form.on('Assignment Evaluation', {
	participant_group: function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_details',
			args: {
				participant_group_id: frm.doc.participant_group
			},
			callback: function(result){
				if(result.message){
					frm.set_value("select_course", result.message[2])
					frm.set_value("select_module", result.message[3])
					frm.set_value("academic_year", result.message[0])
					frm.set_value("academic_term", result.message[1])
					frm.set_df_property('instructor_id', 'options', result.message[4])
					frm.set_df_property('participant_id', 'options', result.message[5])
				}
			}
		})
	},
	participant_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_participant_name',
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
			method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_assignment_list',
			args: {
				instructor_id: frm.doc.instructor_id,
				participant_group_id : frm.doc.participant_group,
				programs : frm.doc.select_course,
				course: frm.doc.select_module,
				topic : frm.doc.select_sub_module
			},
			callback: function(result){
				frm.set_df_property('select_assignment', 'options', result.message) // assignment
			}
		})
	},
	select_assignment: function(frm){
		alert(500)
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_assignment_details',
			args:{
				assignment_name : frm.doc.select_assignment
			},
			callback: function(result){
				alert(600)
				if(result.message){
					frm.set_value("assessment_criteria", result.message[0])
					frm.set_value("total_marks", result.message[1])
					frm.set_value("passing_marks", result.message[2])
					frm.set_value("weightage", result.message[3])
					frm.set_value("assignment_name", result.message[4])
				}
			}
		})
	},
	marks_earned: function(frm){
		if(frm.doc.marks_earned > frm.doc.total_marks){
			alert('Earned marks cannot be more than total marks')
			frm.set_value('marks_earned', '')
		}
	}
})