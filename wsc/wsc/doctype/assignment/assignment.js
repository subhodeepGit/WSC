// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment', {
	refresh: function(frm) {
		frm.set_query("participant_group", function() {
            return {
                filters: {
                    "disabled":0
                }
            };
        });
		if(frm.doc.docstatus===1 && frm.doc.assignment_creation_status=="Pending") {
			frm.add_custom_button(__("Create Assignment"), function() {
                frappe.model.open_mapped_doc({
					method: "wsc.wsc.doctype.assignment.assignment.create_assignment",
					frm: frm,
				});
			});
		}
	},
	setup: function(frm){
		frm.set_query("instructor_id", function() {
			return {
				query: 'wsc.wsc.doctype.assignment.assignment.instructor',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});

		frm.set_query("participant_id", function() {
			return {
				query: 'wsc.wsc.doctype.assignment.assignment.participant',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});

		frm.set_query("assessment_criteria", function() {
			return {
				query: 'wsc.wsc.doctype.assignment.assignment.criteria',
				filters:{"course":frm.doc.course}
				
			};
		});
	},
	participant_group: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment.assignment.get_details',
			args: {
				participant_group_id : frm.doc.participant_group
			},
			callback: function(result){
				frm.set_value("academic_year", result.message[0]) // academic year
				frm.set_value("academic_term", result.message[1]) // acadmic term
				frm.set_value("programs", result.message[2]) // course
				frm.set_value("course", result.message[3]) // module
			}
		})
	},
	instructor_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment.assignment.get_instructor_name',
			args: {
				participant_group_id: frm.doc.participant_group,
				instructor_id: frm.doc.instructor_id
			},
			callback: function(result){
				frm.set_value("instructor_name", result.message)
			}
		})
	},
	assessment_criteria: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.assignment.assignment.get_criteria_details',
			args:{
				course: frm.doc.course,
				assessment_criteria : frm.doc.assessment_criteria
			},
			callback: function(result){
				frm.set_value("total_marks", result.message[0])
				frm.set_value("passing_marks", result.message[1])
				frm.set_value("weightage", result.message[2])
			}
		})
	},
	start_date: function(frm) {
        // set minimum To Date equal to From Date
        frm.fields_dict.end_date.datepicker.update({
            minDate: frm.doc.start_date ? new Date(frm.doc.start_date) : null
        });
		// Define the start and end datetime strings
		var start_date_time = frm.doc.start_date;
		var end_date_time = frm.doc.end_date;

		// Parse the datetime strings into Date objects
		var startDate = new Date(start_date_time);
		var endDate = new Date(end_date_time);

		if (isNaN(startDate) || isNaN(endDate)) {
			
		  } else {
		var timeDifference = endDate - startDate;

		// Convert the time difference to days, hours, minutes, and seconds
		var days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
		var hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		var minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
		
		// Output the total duration
		// console.log("Total Duration: " + days + " days, " + hours + " hours, " + minutes + " minutes, " + seconds + " seconds");
		frm.set_value("total_duration",days + " days, " + hours + " hours, " + minutes + " minutes, " + seconds + " seconds")
		  }
    },

	end_date: function(frm) {
        // set maximum From Date equal to To Date
        frm.fields_dict.start_date.datepicker.update({
            maxDate: frm.doc.end_date ? new Date(frm.doc.end_date) : null
        });
		// Define the start and end datetime strings
		var start_date_time = frm.doc.start_date;
		var end_date_time = frm.doc.end_date;

		// Parse the datetime strings into Date objects
		var startDate = new Date(start_date_time);
		var endDate = new Date(end_date_time);


		if (isNaN(startDate) || isNaN(endDate)) {
			
		} else {
		var timeDifference = endDate - startDate;

		// Convert the time difference to days, hours, minutes, and seconds
		var days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
		var hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		var minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
		
		// Output the total duration
		// console.log("Total Duration: " + days + " days, " + hours + " hours, " + minutes + " minutes, " + seconds + " seconds");
		frm.set_value("total_duration",days + " days, " + hours + " hours, " + minutes + " minutes, " + seconds + " seconds")
		}
    },
	tot_start_date: function(frm) {
		frm.fields_dict.start_date.datepicker.update({
            minDate: frm.doc.tot_start_date ? new Date(frm.doc.tot_start_date) : null
        });
		frm.fields_dict.start_date.datepicker.update({
            maxDate: frm.doc.tot_end_date ? new Date(frm.doc.tot_end_date) : null
        });
	},
	tot_end_date: function(frm) {
		frm.fields_dict.end_date.datepicker.update({
            minDate: frm.doc.tot_start_date ? new Date(frm.doc.tot_start_date) : null
        });
		frm.fields_dict.end_date.datepicker.update({
            maxDate: frm.doc.tot_end_date ? new Date(frm.doc.tot_end_date) : null
        });
	}
});
