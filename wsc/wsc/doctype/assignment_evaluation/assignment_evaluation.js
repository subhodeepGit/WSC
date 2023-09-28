// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// ------------------------------------------------------------------------------------------------------------
frappe.ui.form.on('Assignment Evaluation', {
	setup: function(frm){
		frm.set_df_property('job_sheet_fetch', 'cannot_add_rows', true);
		frm.set_df_property('job_sheet_fetch', 'cannot_delete_rows', true);
		var df = frappe.meta.get_docfield("Job sheet","job_sheet_number", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","job_sheet_name", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","start_date_and_time", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","end_date_and_time", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","total_durationin_hours", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","assessment_criteria", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","total_marks", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","pass_marks", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","weightage", frm.doc.name);
		df.read_only = 1;
		var df = frappe.meta.get_docfield("Job sheet","marks", frm.doc.name);
		df.reqd = 1;

		frm.refresh_field('job_sheet_fetch');
		frm.refresh_field('job_sheet_name');
		frm.refresh_field('start_date_and_time');
		frm.refresh_field('end_date_and_time');
		frm.refresh_field('total_durationin_hours');
		frm.refresh_field('assessment_criteria');
		frm.refresh_field('total_marks');
		frm.refresh_field('pass_marks');
		frm.refresh_field('weightage');
		frm.refresh_field('marks');

		frm.set_query('assignment_declaration', function(){
			return{
				"filters": [
					["Assignment Declaration", "docstatus", "=", 1],
				]
			}
		})

		frm.set_query("instructor_id", function() {
			return {
				query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.instructor',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});

		// frm.set_query("participant_id", function() {
		// 	return {
		// 		query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.participant',
		// 		filters:{"participant_group_id":frm.doc.participant_group}
		// 		// filters:{"assignment_declaration":frm.doc.assignment_declaration}
				
		// 	};
		// });
		frm.set_query("participant_id", function() {
			return {
				query: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_qualified_participants',
				filters: {
					"assignment_declaration":frm.doc.assignment_declaration,
				}
			};
		});
	},
	// participant_group: function(frm){
	// 	frappe.call({
	// 		method : 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_details',
	// 		args: {
	// 			participant_group_id: frm.doc.participant_group
	// 		},
	// 		callback: function(result){
	// 			if(result.message){
	// 				frm.set_value("select_course", result.message[2])
	// 				frm.set_value("select_module", result.message[3])
	// 				frm.set_value("academic_year", result.message[0])
	// 				frm.set_value("academic_term", result.message[1])
	// 				// frm.set_df_property('instructor_id', 'options', result.message[4])
	// 				// frm.set_df_property('participant_id', 'options', result.message[5])
	// 				// frm.set_df_property('select_assignment', 'options', result.message[6]) // need help with this
	// 			}
	// 		}
	// 	})
	// },
	// participant_id: function(frm){
	// 	frappe.call({
	// 		method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_participant_name',
	// 		args:{
	// 			participant_group_id : frm.doc.participant_group,
	// 			participant_id : frm.doc.participant_id
	// 		},
	// 		callback: function(result){
	// 			// alert(JSON.stringify(result))
	// 			if(result.message){
	// 				frm.set_value("participant_name",result.message)
	// 			}
	// 		}
	// 	})
	// },
	participant_name: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.set_marks',
			args:{
				participant_id : frm.doc.participant_id,
				assignment_name : frm.doc.select_assignment
			},
			callback: function(result){
				if(result.message){
					frm.set_value("marks_earned", '0')
				}
			}
		})
	},
	// instructor_id: function(frm){
	// 	frappe.call({
	// 		method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_instructor_name',
	// 		args: {
	// 			participant_group_id: frm.doc.participant_group,
	// 			instructor_id: frm.doc.instructor_id
	// 		},
	// 		callback: function(result){
	// 			frm.set_value("instructor_name", result.message)
	// 		}
	// 	})
	// },
	instructor_name: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_assignment_list',
			args: {
				instructor_id: frm.doc.instructor_id,
				participant_group_id: frm.doc.participant_group,
				programs : frm.doc.select_course,
				course: frm.doc.select_module,
			},
			callback: function(result){
				frm.set_df_property('select_assignment', 'options', result.message) // assignment
			}
		})
	},
	select_assignment: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_assignment_details',
			args:{
				assignment_name : frm.doc.select_assignment
			},
			callback: function(result){
				if(result.message){
					frm.set_value("assessment_component", result.message[0])
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
			frappe.msgprint('Earned marks cannot be more than total marks')
			frm.set_value('marks_earned', '')
		}
	},
	assignment_declaration: function(frm){
		// alert(JSON.stringify(frm.doc.job_sheet_fetch))
		if (frm.doc.job_sheet_fetch != ""){
			frm.set_df_property('marks_earned', 'read_only', 1)
		} else {
			frm.set_df_property('marks_earned', 'read_only', 0)
		}
		if (frm.doc.assignment_declaration == undefined || frm.doc.assignment_declaration == "" || frm.doc.assignment_declaration == null) {

		} else {
			frappe.model.with_doc("Assignment Declaration", frm.doc.assignment_declaration, function () {
				var tabletransfer = frappe.model.get_doc("Assignment Declaration", frm.doc.assignment_declaration);
				cur_frm.doc.job_sheet_fetch = "";
				cur_frm.refresh_field("job_sheet_fetch");
				$.each(tabletransfer.job_sheet, function (index, row) {
					var d = frappe.model.add_child(cur_frm.doc, "Job sheet", "job_sheet_fetch");
					d.job_sheet_number = row.job_sheet_number;
					d.job_sheet_name = row.job_sheet_name;
					d.start_date_and_time = row.start_date_and_time;
					d.end_date_and_time = row.end_date_and_time;
					d.total_durationin_hours = row.total_durationin_hours;
					d.assessment_criteria = row.assessment_criteria;
					d.total_marks = row.total_marks;
					d.pass_marks = row.pass_marks;
					d.weightage = row.weightage;
					cur_frm.refresh_field("job_sheet_fetch");
				});
			});
		}
	}
})

// Child table Calculation
frappe.ui.form.on('Job sheet', {	//Child table Name
	marks:function(frm, cdt, cdn){	//Child table field Name where you data enter
	var d = locals[cdt][cdn];
	// if (d.marks > d.total_marks){
	// 	d.marks = ''
	// 	frm.set_value("marks_earned", '');
	// 	refresh_field("marks", d.name, d.parentfield);
	// }
	var total = 0;
	let a= parseInt(total)
	frm.doc.job_sheet_fetch.forEach(function(d)  { if (d.marks >= 0){a = a+ parseInt(d.marks);} }); //Child table name and field name
	frm.set_value("marks_earned", a);			// Parent field name where calculation going to fetch
	refresh_field("marks_earned");
  },
});