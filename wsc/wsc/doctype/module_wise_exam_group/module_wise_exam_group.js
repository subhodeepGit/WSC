// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Module Wise Exam Group', {
	refresh: function(frm){
		frm.set_df_property('student_list', 'cannot_add_rows', true);
		frm.set_df_property('student_list', 'cannot_delete_rows', true);
		frm.set_df_property('scheduling_group_exam', 'cannot_add_rows', true);
		// frm.set_df_property('scheduling_group_exam', 'cannot_delete_rows', true);
		if(frm.doc.docstatus == 1 && frappe.user.has_role(["Education Administrator"]) || frappe.user.has_role(["Exam Coordinator"]) || frappe.user.has_role(["System Manager"])){
			frm.add_custom_button("Create Setter & Moderator", () => {
				let data = {}
				data.programs = frm.doc.exam_course
				data.program = frm.doc.semester
				data.academic_year = frm.doc.academic_year
				data.academic_term = frm.doc.academic_term
				data.exam_declaration = frm.doc.exam_declaration_id
				frappe.new_doc("Exam Assessment Plan", data)
			},__('Create'));
		}
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
		frm.set_query("marker_name", function() {
			return {
				query: 'wsc.wsc.doctype.module_wise_exam_group.module_wise_exam_group.get_marker',
				filters:{
					
						"department":frm.doc.department,
					}
			};
		});
		frm.set_query("checker", function() {
			return {
				query: 'wsc.wsc.doctype.module_wise_exam_group.module_wise_exam_group.get_checker',
				filters:{
					
						"department":frm.doc.department,
					}
			};
		});
		frm.set_query("course_manager_name", function() {
			return {
				query: 'wsc.wsc.doctype.module_wise_exam_group.module_wise_exam_group.get_cm',
				filters:{
					
						"department":frm.doc.department,
					}
			};
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
		frm.clear_table("student_list");
		frappe.call({
			method: 'wsc.wsc.doctype.module_wise_exam_group.module_wise_exam_group.get_student',
			args:{
				programs: frm.doc.exam_course,
				academic_term: frm.doc.academic_term,
                class_data: frm.doc.class,
                minimum_attendance_criteria:frm.doc.percentage,
				attendance_criteria:frm.doc.attendance_criteria,
				start_date_of_attendence_duration:frm.doc.start_date_of_attendence_duration,
				end_date_of_attendence_duration:frm.doc.end_date_of_attendence_duration,
				modules_id:frm.doc.modules_id,
				semester:frm.doc.semester,
				exam_category:frm.doc.exam_category,
				exam_schedule_id:frm.doc.exam_schedule_id,
				course_type:frm.doc.course_type,
				assessment_component:frm.doc.assessment_component			
			},
			callback: function(r) {
				(r.message).forEach(element => {
					var row = frm.add_child("student_list")
					row.student_no=element.student
					row.student_name=element.student_name
                    row.roll_no = element.roll_no
                    row.permanent_registration_no = element.permanant_registration_number
					row.total_no_of_classes_scheduled = element.total_no_of_classes_scheduled
					row.elegibility_status = element.elegibility_status
					row.examination_qualification_approval = element.examination_qualification_approval
					row.total_no_of_class_attended_by_the_studen = element.total_no_of_class_attended_by_the_studen
					row.attendance_percentage=element.attendance_percentage
				});
				frm.refresh_field("student_list")
				frm.save();
				frm.set_value("total_enrolled_student",(r.message).length)
			}
		})
	}
});
