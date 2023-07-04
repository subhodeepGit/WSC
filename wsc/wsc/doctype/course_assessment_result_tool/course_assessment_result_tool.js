// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt


frappe.ui.form.on('Course Assessment Result Tool', {
	setup:function(frm){
		// frm.set_query("programs", function () {
		// 	return {
		// 		filters: [
		// 			["Programs", "program_grade", "=", frm.doc.program_grade],
		// 		]
		// 	}
		// });
		frm.set_query("course", function() {
			return {
				query:"wsc.wsc.doctype.module_wise_exam_group.module_wise_exam_group.valid_module_as_exam_declation",
				txt:frm.doc.exam_declaration,
			}
		});
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year	
				}
			};
        });
        // frm.set_query("course", function() {
		// 	return {
		// 		query:"wsc.wsc.doctype.course_assessment_result_tool.course_assessment_result_tool.get_courses",
		// 		filters: {
		// 			"semester":frm.doc.semester
		// 			// "exam_declaration":frm.doc.exam_declaration
		// 		}
				
		// 	};
        // });
        frm.set_query("assessment_criteria", function() {
			return {
				query:"wsc.wsc.doctype.course_assessment_result_tool.course_assessment_result_tool.get_assessment_criteria_list",
				filters: {
					"course":frm.doc.course
				}
			};
        });
		frm.set_query("exam_declaration", function() {
			return {
				filters: {
					// "semester":frm.doc.semester,
					// "academic_year":frm.doc.academic_year,
					// "academic_term":frm.doc.academic_term,
					"docstatus":1	
				}
			};
        });
		frm.set_query("exam_assessment_plan", function() {
			return {
				filters: {
					"exam_declaration":frm.doc.exam_declaration,
					'docstatus':1
				}
			};
        });
		// frm.set_query("semester", function() {
		// 	return {
		// 		filters: {
		// 			"programs":frm.doc.programs	
		// 		}
		// 	};
        // });
	},
	programs: function(frm) {
		frm.trigger("get_student_details");
	},
	semester: function(frm) {
		frm.trigger("get_student_details");
	},
	course: function(frm) {
		frm.trigger("get_student_details");
	},
	academic_year: function(frm) {
		frm.trigger("get_student_details");
	},
	academic_term: function(frm) {
		frm.trigger("get_student_details");
	},
	exam_declaration:function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.course_assessment_result_tool.course_assessment_result_tool.get_semester_and_exam_assessment_plan',
			args:{
				declaration_id:frm.doc.exam_declaration,
			},
			callback: function(r) {
				if (r.message) {
					var sem=r.message
					frm.set_value('semester', sem['semester']);
				}
			}
		})
	},
	assessment_criteria: function(frm) {
		frm.disable_save();
		frm.page.set_primary_action(("Submit"), function() {
			let html_values=cur_frm.fields_dict.result_html.wrapper;
			var course_assessment={};
			course_assessment["rows"]={};
			course_assessment["criteria"]=frm.doc.assessment_criteria;
			course_assessment["academic_year"]=frm.doc.academic_year;
			course_assessment["academic_term"]=frm.doc.academic_term;
			course_assessment["course"]=frm.doc.course;
			course_assessment["programs"]=frm.doc.programs;
			course_assessment["program_grade"]=frm.doc.program_grade;
			course_assessment["exam_declaration"]=frm.doc.exam_declaration;
			course_assessment["exam_assessment_plan"]=frm.doc.exam_assessment_plan;
			(cur_frm.doc.students).forEach(resp => {
				var row={};
				let earned_marks='';
				$(html_values).find(`[data-row="${resp.id}"].result-earned_marks`).each(function(el, input){
					earned_marks=$(input).val();
				})
				let attendance='';
				$(html_values).find(`[data-row="${resp.id}"].result-attendence`).each(function(el, input){
					attendance=$(input).val();
				})
				if (earned_marks){
					row=resp;
					row['earned_marks']=earned_marks;
					row['attendance']=attendance
					course_assessment['rows'][resp.id]=row;
				}
			})
			frappe.call({
				method: "wsc.wsc.doctype.course_assessment_result_tool.course_assessment_result_tool.make_course_assessment",
				args: {
					"course_assessment":course_assessment,
					},
				callback: function(r) {
					console.log("######################################")
				}
			});
		
		});
		frm.trigger("get_student_details");
	},
	get_student_details:function(frm){
		if(frm.doc.academic_year && frm.doc.academic_term && frm.doc.course && frm.doc.assessment_criteria && frm.doc.programs && frm.doc.semester) {
			frappe.call({
				method: "wsc.wsc.doctype.course_assessment_result_tool.course_assessment_result_tool.get_enroll_students",
				args: {
					// "academic_year":frm.doc.academic_year,
					// "academic_term":frm.doc.academic_term,
					// "programs":frm.doc.programs,
					// "semesters":frm.doc.semester,
					"course":frm.doc.course,
					"criteria":frm.doc.assessment_criteria,
					"exam_declaration":frm.doc.exam_declaration
				},
				callback: function(r) {
					if (r.message) {
						frm.doc.students = r.message[0];
						frm.doc.course_assessment=r.message[1];
						frm.set_value("total_students",(r.message[0]).length)
						frm.events.render_table(frm);
					}
				}
			});
		}
	},
	render_table: function(frm) {
		$(frm.fields_dict.result_html.wrapper).empty();
		frm.events.get_marks(frm);
	},

	get_marks: function(frm) {
		var result_table = $(frappe.render_template('course_assessment_result_tool', {
			frm: frm,
			students: frm.doc.students,
			course_assessment:frm.doc.course_assessment
		}));
		result_table.appendTo(frm.fields_dict.result_html.wrapper);
	},

});
