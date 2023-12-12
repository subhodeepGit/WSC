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
				filters: [["Program","programs",'=',frm.doc.program]]
					
			};
		});
		// frm.fields_dict['mentee_list'].grid.get_field('student').get_query = function(doc, cdt, cdn) {
		// 	if(frm.doc.program){
		// 		return {
		// 			query: 'wsc.wsc.doctype.mentor_allocation.mentor_allocation.get_students',
		// 			// filters: {
		// 			// 	"programs":frm.doc.program,
		// 			// }
		// 			filters: [["programs",'=',frm.doc.program]]
		// 		};
		
		// 	}

        // }
	},

});


frappe.ui.form.on('Mentee List', {
	mentee_list_add: function(frm){
		frm.fields_dict['mentee_list'].grid.get_field('student').get_query = function(doc){

			var stu_list = [];
			if(!doc.__islocal) stu_list.push(doc.name);
			$.each(doc.mentee_list, function(idx, val){
				if (val.student) stu_list.push(val.student);
			});
			return { 
				query: 'wsc.wsc.doctype.mentor_allocation.mentor_allocation.get_students',
				filters: [['Student', 'name', 'not in', stu_list],["Program","programs",'=',frm.doc.program]] 
			};
		};
	}
});