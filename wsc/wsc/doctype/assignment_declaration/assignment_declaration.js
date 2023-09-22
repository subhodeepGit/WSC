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

		frm.set_query("select_assessment_criteria", function() {
			return {
				query: 'wsc.wsc.doctype.assignment_declaration.assignment_declaration.criteria',
				filters:{"course":frm.doc.module}
				
			};
		});
		frm.set_query("participant_group", function(){
			return {
				"filters": [
					["Participant Group", "program", "=", frm.doc.course],
					["Participant Group", "course", "=", frm.doc.module],
					["Participant Group", "academic_year", "=", frm.doc.academic_year],
				]
			}
		});
		frm.set_query('course', function(){
			return{
				"filters": [
					["Programs", "program_grade", "=", frm.doc.course_type],
					["Programs", "is_tot", "=", 1],
				]
			}
		})
		frm.set_query('course_type', function(){
			return{
				"filters": [
					["Program Grades", "is_short_term_course", "=", "Yes"],
				]
			}
		})
	},
	participant_group: function(frm){
		frm.trigger('get_participant')
	},
	attendance_percentage: function(frm){
		frm.trigger('get_participant')
	},
	attendance_applicable: function(frm){
		if (frm.is_dirty()) {
			frm.set_value("attendance_percentage",0)
			frm.trigger('get_participant')
		}
	},
	tot_start_date: function(frm) {
		frm.fields_dict.assignment_start_date.datepicker.update({
            minDate: frm.doc.tot_start_date ? new Date(frm.doc.tot_start_date) : null
        });
		// frm.fields_dict.assignment_start_date.datepicker.update({
        //     maxDate: frm.doc.tot_end_date ? new Date(frm.doc.tot_end_date) : null
        // });
	},
	tot_end_date: function(frm) {
		frm.fields_dict.assignment_end_date.datepicker.update({
            minDate: frm.doc.tot_start_date ? new Date(frm.doc.tot_start_date) : null
        });
		// frm.fields_dict.assignment_end_date.datepicker.update({
        //     maxDate: frm.doc.tot_end_date ? new Date(frm.doc.tot_end_date) : null
        // });
	},
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
		}),
		frappe.call({
			"method": "wsc.wsc.doctype.assignment_declaration.assignment_declaration.get_assignments",
			args:{
				participant_group:frm.doc.participant_group,
				select_assessment_criteria:frm.doc.select_assessment_criteria
			},
			callback: function(r) {
				if (r.message){
					frappe.model.clear_table(frm.doc, 'job_sheet');
					(r.message).forEach(element => {
					    var c = frm.add_child("job_sheet")
					    c.job_sheet_name=element.assignment_name
					    c.assessment_criteria=element.assessment_criteria
					    c.total_marks=element.total_marks
					    c.pass_marks=element.passing_marks
					    c.weightage=element.weightage
						c.start_date_and_time=element.start_date
						c.end_date_and_time=element.end_date
						c.total_durationin_hours=element.total_duration
						c.job_sheet_number=element.name
					});
					frm.refresh_field("job_sheet")
				}
			}
		})
	},
	assignment_start_date: function(frm) {
        frm.fields_dict.assignment_end_date.datepicker.update({
            minDate: frm.doc.assignment_start_date ? new Date(frm.doc.assignment_start_date) : null
        });
    },

    assignment_end_date: function(frm) {
        frm.fields_dict.assignment_start_date.datepicker.update({
            maxDate: frm.doc.assignment_end_date ? new Date(frm.doc.assignment_end_date) : null
        });
    },

	course_type: function(frm){
		frm.set_value("participant_group","")
	},

	course: function(frm){
		frm.set_value("participant_group","")
	},

	academic_year: function(frm){
		frm.set_value("participant_group","")
	},

	module: function(frm){
		frm.set_value("participant_group","")
	},
});