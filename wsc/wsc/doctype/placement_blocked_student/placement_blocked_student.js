// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Blocked Student', {
	setup: function(frm) {
		frm.set_df_property('block_drive_list', 'cannot_add_rows', true)
		frm.set_df_property('block_drive_list', 'cannot_delete_rows', true)
		frm.set_df_property('for_courses', 'cannot_add_rows', true)
		frm.set_df_property('for_courses', 'cannot_delete_rows', true)
		frm.set_query('semester', function(doc) {
			return {
				filters: {
					"programs":frm.doc.programs,
				}
			};
		});
		// frm.set_query('placement_drive','block_drive_list', function(doc) {
		// 	return {
		// 		query:"wsc.wsc.doctype.placement_blocked_student.placement_blocked_student.get_placement_drive",
		// 		filters: {
		// 			"programs":frm.doc.programs
		// 		}
		// 	};
		// });
		// frm.set_query('student','blocked_student', function(doc) {
		// 	return {
		// 		query:"wsc.wsc.doctype.placement_blocked_student.placement_blocked_student.get_students",
		// 		filters: {
		// 			"semester":frm.doc.semester,
		// 			"academic_year":frm.doc.academic_year
		// 		}
		// 	};
		// });
	},

});
