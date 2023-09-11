// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment Declaration', {
	setup: function(frm){
		frm.set_df_property('participant_list', 'cannot_add_rows', true);
		frm.set_df_property('participant_list', 'cannot_delete_rows', true);
		frm.set_query("evaluator_id", function() {
			return {
				query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.instructor',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});

		frm.set_query("participant_id", function() {
			return {
				query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.participant',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});
	},
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
					frm.set_value("academic_year", result.message[0])
					frm.set_value("academic_term", result.message[1])
					// frm.set_df_property('evaluator_id', 'options', result.message[4])
					frm.set_df_property('select_assessment_criteria', 'options', result.message[5])
				}
			}
		})
	},
	// evaluator_id: function(frm){
	// 	frappe.call({
	// 		method: 'wsc.wsc.doctype.assignment_declaration.assignment_declaration.get_instructor_name',
	// 		args:{
	// 			participant_group_id : frm.doc.participant_group,
	// 			instructor_id: frm.doc.evaluator_id
	// 		},
	// 		callback: function(result){
	// 			if(result.message){
	// 				frm.set_value("evaluator_name", result.message)
	// 			}
	// 		}
	// 	})
	// },
	get_participant: function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.assignment_declaration.assignment_declaration.get_participants',
			args: {
				participant_group_id: frm.doc.participant_group,
				attendance_applicable: frm.doc.attendance_applicable,
				attendance_percentage : frm.doc.attendance_percentage,
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participant_list')
					result.message.forEach(element => {
						var childTable = frm.add_child('participant_list')
						childTable.participant_id = element.participant
						childTable.participant_name = element.participant_name
						childTable.participant_attendance = element.attendance
						childTable.status = element.status
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
	},
	assignment_start_date: function(frm) {
        // set minimum To Date equal to From Date
        frm.fields_dict.assignment_end_date.datepicker.update({
            minDate: frm.doc.assignment_start_date ? new Date(frm.doc.assignment_start_date) : null
        });
    },

    assignment_end_date: function(frm) {
        // set maximum From Date equal to To Date
        frm.fields_dict.assignment_start_date.datepicker.update({
            maxDate: frm.doc.assignment_end_date ? new Date(frm.doc.assignment_end_date) : null
        });
    },
});

// frappe.ui.form.on("Job Sheet", "assessment_criteria", function(frm, cdt, cdn) {
//     alert(500)
// });