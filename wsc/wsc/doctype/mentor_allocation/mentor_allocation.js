// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Mentor Allocation', {
	refresh: function(frm) {
		// if(frm.doc.docstatus == 1){
		// 	frm.add_custom_button(__("Course Scheduling Tool"), function() {
		// 		frappe.model.open_mapped_doc({
		// 			method: "wsc.wsc.doctype.mentor_allocation.mentor_allocation.create_course_schedulling_tool",
		// 			frm: frm,
		// 		});
		// 	}, __('Create'))
		// }
	},
	setup(frm){
		frm.set_query("semester", function() {
			return {
				filters: {
					"programs":frm.doc.program
				}
			};
		});
		frm.fields_dict['mentee_list'].grid.get_field('student').get_query = function(doc, cdt, cdn) {
			if(frm.doc.program){
				return {
					query: 'wsc.wsc.doctype.mentor_allocation.mentor_allocation.get_students',
					filters: {
						"programs":frm.doc.program,
					}
				};
		
			}

        }
	},

});
