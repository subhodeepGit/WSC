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
        var df = frappe.meta.get_docfield("Job sheet","assignment_upload_status", frm.doc.name);
        df.read_only = 1;
        var df = frappe.meta.get_docfield("Job sheet","assignment_upload_link", frm.doc.name);
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
        frm.refresh_field('assignment_upload_status');
        frm.refresh_field('assignment_upload_link');
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
        //  return {
        //      query: 'wsc.wsc.doctype.tot_participant_attendance.tot_participant_attendance.participant',
        //      filters:{"participant_group_id":frm.doc.participant_group}
        //      // filters:{"assignment_declaration":frm.doc.assignment_declaration}
        //  };
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
	participant_id: function(frm){
		frm.set_value("marks_earned","")
		frm.set_value("job_sheet_fetch","")

		if (frm.doc.participant_id == undefined || frm.doc.participant_id == "" || frm.doc.participant_id == null) {
			// frm.set_df_property('marks_earned', 'read_only', 0)
		} else {
			frappe.call({
				method:'wsc.wsc.doctype.assignment_evaluation.assignment_evaluation.get_assignments_if_uploaded',
				args: {
					assignment_declaration: frm.doc.assignment_declaration,
					participant_id: frm.doc.participant_id,
				},
				callback: function(result){
					if(result.message){
						frappe.model.clear_table(frm.doc, 'job_sheet_fetch')
						result.message.forEach(element => {
							var childTable = frm.add_child('job_sheet_fetch')
							childTable.job_sheet_number = element.job_sheet_number
							childTable.job_sheet_name = element.job_sheet_name
							childTable.assessment_criteria = element.assessment_criteria
							childTable.start_date_and_time = element.start_date_and_time
							childTable.total_durationin_hours = element.total_durationin_hours
							childTable.total_marks = element.total_marks
							childTable.pass_marks = element.pass_marks
							childTable.end_date_and_time = element.end_date_and_time
							childTable.weightage = element.weightage
							childTable.assignment_upload_status = element.assignment_upload_status
							childTable.assignment_upload_link = element.assignment_upload_link
						})
					}
					frm.refresh()
					frm.refresh_field('job_sheet_fetch')
					if (frm.doc.job_sheet_fetch.length === 0){
						frm.set_df_property('marks_earned', 'read_only', 0)
					} else {
						frm.set_df_property('marks_earned', 'read_only', 1)
					}
					
				}
			})
		}
},
assignment_declaration: function(frm){
	frm.set_value("participant_id","")
	frm.set_value("job_sheet_fetch","")
},
})
// Child table Calculation
frappe.ui.form.on('Job sheet', {    //Child table Name
    marks:function(frm, cdt, cdn){  //Child table field Name where you data enter
    var d = locals[cdt][cdn];
    let total_marks = parseInt(d.total_marks)
    let marks = parseInt(d.marks)
    if (marks > total_marks){
        d.marks = ''
        frm.set_value("marks_earned", '');
        refresh_field("marks", d.name, d.parentfield);
        frappe.msgprint("Earned Marks cannot be greater than Total Marks!")
    }
    var total = 0;
    let a= parseInt(total)
    frm.doc.job_sheet_fetch.forEach(function(d)  { if (d.marks >= 0){a = a+ parseInt(d.marks);} }); //Child table name and field name
    frm.set_value("marks_earned", a);           // Parent field name where calculation going to fetch
    refresh_field("marks_earned");
  },
});












