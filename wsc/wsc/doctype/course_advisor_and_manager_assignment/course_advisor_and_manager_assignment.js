// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course Advisor and Manager Assignment', {
	refresh: function(frm){
		if (frm.is_new()){
			frm.set_intro('This form assigns eligible Advisor, Manager, and Deputy Director to receive notifications for the Leave Application process and take necessary actions for specified students.', 'blue');
		}
	},
	
	get_students: function(frm){
		frm.clear_table("students_details");
		frappe.call({
			method: 'wsc.wsc.doctype.course_advisor_and_manager_assignment.course_advisor_and_manager_assignment.get_students',
			args:{
				programs: frm.doc.programs,
				academic_term: frm.doc.academic_term,
                class_data: frm.doc.class,
				semester:frm.doc.semester
			},
			callback: function(r) {
				(r.message).forEach(element => {
					var row = frm.add_child("students_details")
					row.student=element.student
					row.student_name=element.student_name
                    row.roll_number = element.roll_no
                    row.permanent_registration_number = element.permanant_registration_number
				});
				frm.refresh_field("students_details")
				
			}
		})
	},

	employee: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.course_advisor_and_manager_assignment.course_advisor_and_manager_assignment.get_cm_email',
			args:{
				employee: frm.doc.employee
			},
			callback: function(r) {
				if (r.message){
					frm.set_value('cm_email',r.message)
				}
			}
		})
	},

	employee_1: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.course_advisor_and_manager_assignment.course_advisor_and_manager_assignment.get_ca_email',
			args:{
				employee_1: frm.doc.employee_1
			},
			callback: function(r) {
				if (r.message){
					frm.set_value('ca_email',r.message)
				}
			}
		})
	},

	academic_year: function(frm){
		frm.set_value("academic_term","")
	},

	program_grades: function(frm){
		frm.set_value("programs","")
	},

	programs: function(frm){
		frm.set_value("semester","")
	},
	});

	frappe.ui.form.on('Course Advisor and Manager Assignment', 'onload', function(frm) {

		{

			frm.set_query("academic_term", function() {
				return {
					filters: {
						"academic_year":frm.doc.academic_year
					}
				};
			});
			frm.set_query("semester", function() {
				return {
					filters: {
						"programs":frm.doc.programs
					}
				};
			});
			frm.set_query("programs", function() {
				return {
					filters: {
						"program_grade":frm.doc.program_grades
					}
				};
			});
			frm.set_query("course", function() {
				return {
					query:"wsc.wsc.doctype.course_advisor_and_manager_assignment.course_advisor_and_manager_assignment.get_courses",
					filters: {
						"semester":frm.doc.semester
					}
					
				};
			});
		 }
		 
	});
