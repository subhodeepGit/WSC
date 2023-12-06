// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Cumulative Marksheet', {
	student(frm){
		if (frm.doc.student) {
			frappe.call({
				method: 'get_student_details',
				doc:frm.doc,
				callback: function(r) {
					if (r.message) {
						frm.set_value("grading_scale",r.message)
					}
					frm.refresh();
					refresh_field('cummulative_courses_item');
				}
			});
		}
	},
	employee: function(frm) {
		if(frm.doc.employee){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) { 
					if(r.message){
						if (r.message['designation']){
							frm.set_value("designation",r.message['designation'])
						}
						if (r.message['employee_name']){
							frm.set_value("employee_name",r.message['employee_name'])
						}
					}
				} 
			}); 
		}
	},
});
