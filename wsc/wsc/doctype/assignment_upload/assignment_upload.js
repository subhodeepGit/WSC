// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment Upload', {
	// refresh: function(frm) {

	// }
	refresh: function(frm){

		if (!frm.doc.attach_assignment_button && !frm.is_new() && frm.doc.docstatus != 1) {
			frm.set_intro('Please Attach your Assignment using the "Attach Assignment" Button.', 'green');
		}		

		frm.set_query("participant_group", function() {
            return {
                filters: {
                    "disabled":0
                }
            };
        });
		frm.set_query("instructor_id", function() {
			return {
				query: 'wsc.wsc.doctype.assignment_upload.assignment_upload.instructor',
				filters:{
					"participant_group_id":frm.doc.participant_group,
				}
				
			};
		});

		frm.set_query("participant_id", function() {
			return {
				query: 'wsc.wsc.doctype.assignment_upload.assignment_upload.participant',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});

		frm.set_query("assignment_id", function() {
			return {
				query: 'wsc.wsc.doctype.assignment_upload.assignment_upload.assignment',
				filters:{
					"participant_group_id":frm.doc.participant_group,
					"course":frm.doc.course
				}
				
			};
		});
	},
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
					frm.set_value("academic_year", result.message[2])
					frm.set_value("academic_term", result.message[3])
				}
			}
		})
	},
	assignment_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment_upload.assignment_upload.get_assignment_details',
			args:{
				assignment_name : frm.doc.assignment_id
			},
			callback: function(result){
				if(result.message){
					frm.set_value("assessment_component", result.message[0])
					frm.set_value("total_marks", result.message[1])
					frm.set_value("passing_marks", result.message[2])
					frm.set_value("weightage", result.message[3])
					frm.set_value("assignment_number", result.message[4])
					frm.set_value("start_date", result.message[5])
					frm.set_value("end_date", result.message[6])
				}
			}
		})
	},
	download_questions(frm){
		if (frm.doc.assignment_questions){
			let file_url = frm.doc.assignment_questions;
			if (frm.doc.file_name) {
				file_url = file_url.replace(/#/g, "%23");
			}
			window.open(file_url);
		}
	},
	download_answer(frm){
		if (frm.doc.assignment_attach_button){
			let file_url = frm.doc.assignment_attach_button;
			if (frm.doc.file_name) {
				file_url = file_url.replace(/#/g, "%23");
			}
			window.open(file_url);
		}
	},
});

