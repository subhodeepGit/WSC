// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Continuous Evaluation Tool', {
	exam_declaration_id:function(frm){
		if (frm.doc.exam_cate=="Re-Exam"){
			let fname=frm.doc.exam_declaration_id;    
        	frm.set_value("exam_declaration",fname);
		}
		frappe.call({
			method: "wsc.wsc.doctype.continuous_evaluation_tool.continuous_evaluation_tool.get_semester_and_exam_assessment_plan",
			args:{
				declaration_id:frm.doc.exam_declaration_id,
			},
			callback: function(r) {
				if (r.message) {
					var sem=r.message
					frm.set_value('semester', sem['semester']);
				}
			}
		})
		frm.trigger("get_student_details");
	},
	// "enroll_students": function(frm) {
	// 	if (frm.doc.new_semester && frm.doc.new_academic_year){
	// 		frappe.call({
	// 			method: "enroll_students",
	// 			doc:frm.doc,
	// 			callback: function(r) {
	// 				// frm.set_value("students", []);
	// 				frappe.hide_msgprint(true);
	// 			}
	// 		});
	// 	}

	// },
	// course:function(frm){
	// 	// window.location.reload();
	// 	frappe.call({
	// 		method: "wsc.wsc.doctype.continuous_evaluation_tool.continuous_evaluation_tool.get_module_details",
	// 		args: {
	// 			"assessment_component":frm.doc.assessment_criteria,
	// 			"module":frm.doc.course
	// 			},
	// 		callback: function(r) {
	// 			frm.set_value("module_exam_group",r.message['name'])
	// 		}
	// 	})	
	// 	frm.trigger("get_student_details");	
	// },
	course:function(frm){
		frm.disable_save();
		frm.set_query("programs", function () {
			return {
				filters: [
					["Programs", "program_grade", "=", frm.doc.program_grade],
				]
			}
		});
		frm.set_query("module_exam_group", function () {
			return {
				filters: [
					["Module Wise Exam Group", "modules_id", "=", frm.doc.course],
					["Module Wise Exam Group", "assessment_component", "=", frm.doc.assessment_criteria],
					["Module Wise Exam Group", "exam_declaration_id", "=", frm.doc.exam_declaration_id],
					["Module Wise Exam Group", "docstatus", "=", 1],
				]
			}
		});
		// frm.set_query("module_exam_group", function() {
        //     return {
        //         filters: {
        //             "module_id":frm.doc.course
        //         }
        //     };
        // });
		frappe.call({
			method: "wsc.wsc.doctype.continuous_evaluation_tool.continuous_evaluation_tool.get_module_details",
			args: {
				"assessment_component":frm.doc.assessment_criteria,
				"module":frm.doc.course
				},
			callback: function(r) {
				frm.page.set_primary_action(("Submit"), function() {
					let html_values=cur_frm.fields_dict.student_inputs.wrapper;
					var continuous_evaluation={};
					continuous_evaluation["rows"]={};
					continuous_evaluation["criteria"]=frm.doc.assessment_criteria;
					continuous_evaluation["academic_year"]=frm.doc.academic_year;
					continuous_evaluation["academic_term"]=frm.doc.academic_term;
					continuous_evaluation["course"]=frm.doc.course;
					continuous_evaluation["course_name"]=frm.doc.course_name;
					continuous_evaluation["course_code"]=frm.doc.course_code;
					continuous_evaluation["semester"]=frm.doc.semester;
					continuous_evaluation["exam_cate"]=frm.doc.exam_cate;
					continuous_evaluation["programs"]=frm.doc.programs;
					continuous_evaluation["marker"]=frm.doc.marker;
					continuous_evaluation["marker_name"]=frm.doc.marker_name;
					continuous_evaluation["checker"]=frm.doc.checker;
					continuous_evaluation["checker_name"]=frm.doc.checker_name;
					continuous_evaluation["module_exam_group"]=frm.doc.module_exam_group;
					continuous_evaluation["program_grade"]=frm.doc.program_grade;
					continuous_evaluation["exam_declaration"]=frm.doc.exam_declaration;
					if(cur_frm.doc.students){
						(cur_frm.doc.students).forEach(resp => {
							var row={};
							
							row['student']=resp.student;
							row['student_name']=resp.student_name;
							row['roll_no']=resp.roll_no;
							row['registration_number']=resp.registration_number;
							// row['student_name']=resp.student_name;
							
							$(html_values).find(`[data-row="${resp.student}"].evaluation`).each(function(el, input){
								row['evaluation']=$(input).val();
							})
							
							$(html_values).find(`[data-row="${resp.student}"].grace_marks`).each(function(el, input){
								row['grace_marks']=$(input).val();
							})
							$(html_values).find(`[data-row="${resp.student}"].comment`).each(function(el, input){
								row['comment']=$(input).val();
							})
							$(html_values).find(`[data-row="${resp.student}"].weightage_marks`).each(function(el, input){
								row['weightage_marks']=$(input).val();
							})
		
							$(html_values).find(`[data-row="${resp.student}"].final_marks`).each(function(el, input){
								row['final_marks']=$(input).val();
							})
		
							$(html_values).find(`[data-row="${resp.student}"].earned_credits`).each(function(el, input){
								row['earned_credits']=$(input).val();
							})
							
							$(html_values).find(`[data-row="${resp.student}"].earned_marks`).each(function(el, input){
								row['earned_marks']=$(input).val();
							})
							$(html_values).find(`[data-row="${resp.student}"].total_marks`).each(function(el, input){
								row['total_marks']=$(input).val();
							})
							$(html_values).find(`[data-row="${resp.student}"].total_credits`).each(function(el, input){
								row['total_credits']=$(input).val();
							})
		
							$(html_values).find(`[data-row="${resp.student}"].out_of_marks`).each(function(el, input){
								row['out_of_marks']=$(input).val();
							})
		
							$(html_values).find(`[data-row="${resp.student}"].exam_attendence`).each(function(el, input){
								row['exam_attendence']=$(input).val();
							})
							continuous_evaluation['rows'][resp.student]=row;
						})
					}
					frappe.call({
						
						method: "wsc.wsc.doctype.continuous_evaluation_tool.continuous_evaluation_tool.make_continuous_evaluation",
						
						args: {
							"continuous_evaluation":continuous_evaluation,
							"exam_declaration_id":frm.doc.exam_declaration_id,
							// "module_exam_group":frm.doc.module_exam_group,
						}
					});
				});
			}
			
		})	
		frm.trigger("get_student_details");	
	// },
		// 	frm.page.set_primary_action(("Submit"), function() {
		// 	let html_values=cur_frm.fields_dict.student_inputs.wrapper;
		// 	var continuous_evaluation={};
		// 	continuous_evaluation["rows"]={};
		// 	continuous_evaluation["criteria"]=frm.doc.assessment_criteria;
		// 	continuous_evaluation["academic_year"]=frm.doc.academic_year;
		// 	continuous_evaluation["academic_term"]=frm.doc.academic_term;
		// 	continuous_evaluation["course"]=frm.doc.course;
		// 	continuous_evaluation["course_name"]=frm.doc.course_name;
		// 	continuous_evaluation["course_code"]=frm.doc.course_code;
		// 	continuous_evaluation["semester"]=frm.doc.semester;
		// 	continuous_evaluation["exam_cate"]=frm.doc.exam_cate;
		// 	continuous_evaluation["programs"]=frm.doc.programs;
		// 	continuous_evaluation["marker"]=frm.doc.marker;
		// 	continuous_evaluation["checker"]=frm.doc.checker;
		// 	continuous_evaluation["module_exam_group"]=frm.doc.module_exam_group;
		// 	continuous_evaluation["program_grade"]=frm.doc.program_grade;
		// 	continuous_evaluation["exam_declaration"]=frm.doc.exam_declaration;
		// 	alert(continuous_evaluation["module_exam_group"])
		// 	if(cur_frm.doc.students){
		// 		(cur_frm.doc.students).forEach(resp => {
		// 			var row={};
					
		// 			row['student']=resp.student;
		// 			row['student_name']=resp.student_name;
		// 			row['roll_no']=resp.roll_no;
		// 			row['registration_number']=resp.registration_number;
		// 			// row['student_name']=resp.student_name;
					
		// 			$(html_values).find(`[data-row="${resp.student}"].evaluation`).each(function(el, input){
		// 				row['evaluation']=$(input).val();
		// 			})
					
		// 			$(html_values).find(`[data-row="${resp.student}"].grace_marks`).each(function(el, input){
		// 				row['grace_marks']=$(input).val();
		// 			})

		// 			$(html_values).find(`[data-row="${resp.student}"].weightage_marks`).each(function(el, input){
		// 				row['weightage_marks']=$(input).val();
		// 			})

		// 			$(html_values).find(`[data-row="${resp.student}"].final_marks`).each(function(el, input){
		// 				row['final_marks']=$(input).val();
		// 			})

		// 			$(html_values).find(`[data-row="${resp.student}"].earned_credits`).each(function(el, input){
		// 				row['earned_credits']=$(input).val();
		// 			})
					
		// 			$(html_values).find(`[data-row="${resp.student}"].earned_marks`).each(function(el, input){
		// 				row['earned_marks']=$(input).val();
		// 			})
		// 			$(html_values).find(`[data-row="${resp.student}"].total_marks`).each(function(el, input){
		// 				row['total_marks']=$(input).val();
		// 			})
		// 			$(html_values).find(`[data-row="${resp.student}"].total_credits`).each(function(el, input){
		// 				row['total_credits']=$(input).val();
		// 			})

		// 			$(html_values).find(`[data-row="${resp.student}"].out_of_marks`).each(function(el, input){
		// 				row['out_of_marks']=$(input).val();
		// 			})

		// 			$(html_values).find(`[data-row="${resp.student}"].exam_attendence`).each(function(el, input){
		// 				row['exam_attendence']=$(input).val();
		// 			})
		// 			continuous_evaluation['rows'][resp.student]=row;
		// 		})
		// 	}
		// 	alert(frm.doc.module_exam_group)
		// 	frappe.call({
				
		// 		method: "wsc.wsc.doctype.continuous_evaluation_tool.continuous_evaluation_tool.make_continuous_evaluation",
				
		// 		args: {
		// 			"continuous_evaluation":continuous_evaluation,
		// 			"exam_declaration_id":frm.doc.exam_declaration_id,
		// 			// "module_exam_group":frm.doc.module_exam_group,
		// 		}
		// 	});
		// });
	},
	setup: function(frm) {
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year,
				}
			};
		});
		frm.set_query('semester', function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
		frm.set_query('course', function() {
			return {
				query: 'wsc.wsc.doctype.continuous_evaluation_tool.continuous_evaluation_tool.get_courses',
				// 'wsc.wsc.validations.program_enrollment.get_program_courses',
				// 'education.education.doctype.program_enrollment.program_enrollment.get_program_courses',
				filters: {
					'semester': frm.doc.semester
					// 'program': frm.doc.semester
				}
			};
		});
		frm.set_query('exam_declaration', function() {
			return {
				filters: {
					"exam_category":"Re-Exam",
					"docstatus":1
				}
			};
		});
	},
	academic_year:function(frm){
		frm.trigger("get_student_details");
	},
	academic_term:function(frm){
		frm.trigger("get_student_details");
	},
	programs:function(frm){
		frm.trigger("get_student_details");
	},
	semester:function(frm){
		frm.trigger("get_student_details");
	},
	assessment_criteria: function(frm) {
		frm.trigger("get_student_details");
	},
	
	// get_student_details:function(frm){
		
	get_student_details:function(frm){
		if(frm.doc.exam_cate=="Regular"){
			frm.doc.students=[];
			$(frm.fields_dict.student_inputs.wrapper).empty();
			if(frm.doc.academic_year && frm.doc.academic_term && frm.doc.course && frm.doc.assessment_criteria && frm.doc.programs && frm.doc.semester) {
				frappe.call({
					method: "get_student_allocations",
					doc:frm.doc,
					callback: function(r) {
						if (r.message) {
							$(frm.fields_dict.student_inputs.wrapper).empty();
							frm.doc.students=r.message;
							var result_table = $(frappe.render_template('continuous_evaluation_tool', {
								frm: frm,
								students: r.message,
							}));
							result_table.appendTo(frm.fields_dict.student_inputs.wrapper);
						}
					}
				});
			}
		}
	},
	exam_declaration:function(frm){
		if(frm.doc.exam_cate=="Re-Exam"){
			frm.doc.students=[];
			$(frm.fields_dict.student_inputs.wrapper).empty();

			if(frm.doc.academic_year && frm.doc.academic_term && frm.doc.course && frm.doc.assessment_criteria && frm.doc.programs && frm.doc.semester) {
				frappe.call({
					method: "get_student_allocations",
					doc:frm.doc,
					callback: function(r) {
						if (r.message) {
							$(frm.fields_dict.student_inputs.wrapper).empty();
							frm.doc.students=r.message;
							var result_table = $(frappe.render_template('continuous_evaluation_tool', {
								frm: frm,
								students: r.message,
							}));
							result_table.appendTo(frm.fields_dict.student_inputs.wrapper);
						}
					}
				});
			}
		}
	}
});
