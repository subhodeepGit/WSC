// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Module Wise Exam Group', {
	refresh: function(frm){
		frm.set_df_property('student_list', 'cannot_add_rows', true);
		frm.set_df_property('student_list', 'cannot_delete_rows', true);
	},
	setup: function(frm) {
        frm.set_query("exam_declaration_id", function() {
			return {
				query:"wsc.wsc.doctype.exam_declaration.exam_declaration.valid_exam_declaration_no",
				filters: {
					"docstatus": 1,
				}
			}
		});
		frm.set_query("modules_id", function() {
			return {
				query:"wsc.wsc.doctype.module_wise_exam_group.module_wise_exam_group.valid_module_as_exam_declation",
				txt:frm.doc.exam_declaration_id,
			}
		});
	},
	exam_declaration_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.module_wise_exam_group.module_wise_exam_group.get_semester',
			args:{
				declaration_id:frm.doc.exam_declaration_id,
			},
			callback: function(r) {
				if (r.message) {
					var sem=r.message
					frm.set_value('semester', sem[0]['semester']);
				}
			}
		})
	},
	modules_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.module_wise_exam_group.module_wise_exam_group.module_start_date',
			args:{
				modules_id:frm.doc.modules_id,
				exam_id:frm.doc.exam_declaration_id,
				academic_term:frm.doc.academic_term
			},
			callback: function(r) {
				if (r.message) {
					var sem=r.message
					frm.set_value('module_exam_start_date', sem[0]['examination_date']);
					frm.set_value('module_exam_end_date', sem[0]['examination_end_date']);
					frm.set_value('attendance_criteria', sem[0]['attendance_criteria']);
					frm.set_value('percentage', sem[0]['minimum_attendance_criteria']);
					frm.set_value('start_date_of_attendence_duration', sem[0]['term_start_date']);
					frm.set_value('end_date_of_attendence_duration', sem[0]['term_end_date']);
				}
			}
		})
	},
	get_student:function(frm){
		frappe.call({
			
		})
	}
});
