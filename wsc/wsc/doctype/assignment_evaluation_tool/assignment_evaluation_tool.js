// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Assignment Evaluation Tool', {
// 	// refresh: function(frm) {

// 	// }
// 	setup: function(frm){
// 		frm.set_query("instructor_id", function() {
// 			return {
// 				query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.instructor',
// 				filters:{"participant_group_id":frm.doc.participant_group}
				
// 			};
// 		});

// 		frm.set_query("participant_id", function() {
// 			return {
// 				query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.participant',
// 				filters:{"participant_group_id":frm.doc.participant_group}
				
// 			};
// 		});
// 	},
// 	participant_group: function(frm){
// 		frappe.call({
// 			method : 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_details',
// 			args: {
// 				participant_group_id: frm.doc.participant_group
// 			},
// 			callback: function(result){
// 				if(result.message){
// 					frm.set_value("course", result.message[2])
// 					frm.set_value("module", result.message[3])
// 					frm.set_value("academic_year", result.message[0])
// 					frm.set_value("academic_term", result.message[1])
// 					// frm.set_df_property('instructor_id', 'options', result.message[4])
// 					// frm.set_df_property('participant_id', 'options', result.message[5])
// 					frm.set_value("total_participants", result.message[6])
// 				}
// 			}
// 		})
// 	},
// 	instructor_id: function(frm){
// 		alert(frm.doc.instructor_id)
// 		frappe.call({
// 			method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_instructor_name',
// 			args: {
// 				participant_group_id: frm.doc.participant_group,
// 				instructor_id: frm.doc.instructor_id
// 			},
// 			callback: function(result){
// 				frm.set_value("instructor_name", result.message)
// 			}
// 		}),
// 		frappe.call({
// 			method: 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_assignment_list',
// 			args:{
// 				instructor_id: frm.doc.instructor_id,
// 				participant_group_id : frm.doc.participant_group,
// 				programs : frm.doc.course,
// 				course: frm.doc.module
// 			},
// 			callback: function(result){
// 				frm.set_df_property('select_job_sheetassessment', 'options', result.message)  // select assignment
// 			}
// 		})

// 	},
// 	// instructor_id: function(frm){
// 	// 	// alert(frm.doc.instructor_id)
// 	// 	frappe.call({
// 	// 		method: 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_assignment_list',
// 	// 		args:{
// 	// 			instructor_id: frm.doc.instructor_id,
// 	// 			participant_group_id : frm.doc.participant_group,
// 	// 			programs : frm.doc.course,
// 	// 			course: frm.doc.module
// 	// 		},
// 	// 		callback: function(result){
// 	// 			frm.set_df_property('select_job_sheetassessment', 'options', result.message)  // select assignment
// 	// 		}
// 	// 	})
// 	// },
// 	get_participants : function(frm){
// 		frappe.call({
			
// 			method: 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_participants',
// 			args: {
// 				assignment_name: frm.doc.select_job_sheetassessment,
// 				participant_group_id : frm.doc.participant_group
// 			},
// 			callback: function(result){
// 				if(result.message){
// 					// Qualified participants
// 					frappe.model.clear_table(frm.doc, 'participant_details_data')
// 					result.message[0].forEach(element => {
// 						var childTable = frm.add_child('participant_details_data')
// 						childTable.participant_id = element.participant_id
// 						childTable.participant_name = element.participant_name
// 					})
// 					// Not qualified participants
// 					frappe.model.clear_table(frm.doc, 'disqualified_participants')
// 					result.message[1].forEach(element => {
// 						var childTable = frm.add_child('disqualified_participants')
// 						childTable.participant_id = element.participant_id
// 						childTable.participant_name = element.participant_name
// 						childTable.earned_marks = '0'
// 					})
// 				}
// 				frm.refresh()
// 				frm.refresh_field('participant_details_data')
// 				frm.refresh_field('disqualified_participants')
// 			}
// 		})
// 	},
// 	select_job_sheetassessment: function(frm){
// 		frappe.call({
// 			method: 'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_assignment_details',
// 			args: {
// 				assignment_name : frm.doc.select_job_sheetassessment
// 			},
// 			callback: function(result){
// 				frm.set_value('assessment_criteria', result.message[0])
// 				frm.set_value("total_marks", result.message[1])
// 				frm.set_value("passing_marks", result.message[2])
// 				frm.set_value("weightage", result.message[3])
// 				frm.set_value('assignment_name', result.message[4])
// 			}
// 		})
// 	},

// });

// End of Trash Code


frappe.ui.form.on('Assignment Evaluation Tool', {
	setup: function(frm){
		frm.set_df_property('participants_list', 'cannot_add_rows', true);
		frm.set_df_property('participants_list', 'cannot_delete_rows', true);
		frm.set_query("assignment_declaration", function(){
			return {
				"filters": [
					["Assignment Declaration", "docstatus", "=", 1],
				]
			}
		});
	},
	assignment_declaration: function(frm){
		frm.set_value("participants_list","")
	},
	get_participants: function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.assignment_evaluation_tool.assignment_evaluation_tool.get_participants_and_assignments',
			args: {
				assignment_declaration: frm.doc.assignment_declaration,
				participant_group:frm.doc.participant_group,
				select_assessment_criteria:frm.doc.assessment_component
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participants_list')
					result.message.forEach(element => {
						var childTable = frm.add_child('participants_list')
						childTable.participant_id = element.participant_id
						childTable.participant_name = element.participant_name
						childTable.job_sheet_number = element.name
						childTable.job_sheet_name = element.assignment_name
						childTable.assessment_criteria = element.assessment_criteria
						childTable.start_date_and_time = element.start_date
						childTable.total_duration = element.total_duration
						childTable.total_marks = element.total_marks
						childTable.pass_marks = element.passing_marks
						childTable.end_date_and_time = element.end_date
						childTable.weightage = element.weightage
					})
				}
				frm.refresh()
				frm.refresh_field('participants_list')
			}
		})
	}
})

frappe.ui.form.on('Assignment Evaluation Tool Participants', {	
	marks_earned:function(frm, cdt, cdn){	
	var d = locals[cdt][cdn];
	if (d.total_marks != null && d.marks_earned > d.total_marks) {
			d.marks_earned = ''
			refresh_field("marks_earned", d.name, d.parentfield);
			frappe.msgprint("Earned Marks cannot be greater than Total Marks!")
		}
  },
});