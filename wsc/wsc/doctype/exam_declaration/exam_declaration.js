// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Exam Declaration', {
    exam_start_date(frm) {
        frm.fields_dict.exam_end_date.datepicker.update({
            minDate: frm.doc.exam_start_date ? new Date(frm.doc.exam_start_date) : null
        });
    },

    exam_end_date(frm) {
        frm.fields_dict.exam_start_date.datepicker.update({
            maxDate: frm.doc.exam_end_date ? new Date(frm.doc.exam_end_date) : null
        });
    },
    refresh: function(frm){
        frm.set_query("exam_program", function () {
			return {
				filters: [
					["Programs", "program_grade", "=", frm.doc.program_grade],
				]
			}
		});
        if(frm.doc.docstatus == 1 && frappe.user.has_role(["Education Administrator"]) || frappe.user.has_role(["System Manager"])){
            frm.add_custom_button("Exam Assessment Plan", () => {
                let data = {}
                data.programs = frm.doc.exam_program
                data.program = frm.doc.program
                data.academic_year = frm.doc.academic_year
                data.academic_term = frm.doc.academic_term
                data.exam_declaration = frm.doc.name
                frappe.new_doc("Exam Assessment Plan", data)
            },__('Create'));

            // frm.add_custom_button("Student Group", () => {
            //     let data = {}
            //     data.group_based_on = frm.doc.doctype
            //     data.programs = frm.doc.exam_program
            //     data.program = frm.doc.program
            //     data.academic_year = frm.doc.academic_year
            //     data.academic_term = frm.doc.academic_term
            //     data.exam_declaration = frm.doc.name
            //     frappe.new_doc("Student Group", data)
            // },__('Create'));

            // if(frm.doc.is_application_required==0){
            //     frm.add_custom_button("Student Admit Card", () => {
            //         frappe.call({
            //             // method: 'wsc.wsc.doctype.exam_declaration.exam_declaration.create_student_admit_card',
            //             method: 'create_student_admit_card',
            //             doc:frm.doc,
            //             callback: function(r) {
            //                 if (r.message) {
            //                     frappe.msgprint("Student Admit Card Created")
            //                 }
            //             }
            //         });
            //     },__('Create')); 
            // }
        }
        frm.set_df_property('semesters', 'cannot_add_rows', true);
        frm.set_df_property('courses_offered', 'cannot_add_rows', true);
 
		// if (!frm.doc.__islocal){
		// 	frm.add_custom_button(__('Create Fees'), function() {
		// 		frappe.call({
		// 			method: 'make_exam_assessment_result',
        //             // /opt/bench/frappe-bench/apps/wsc/wsc/wsc/doctype/exam_declaration/exam_declaration.py
		// 			doc: frm.doc,
		// 			callback: function() {
		// 				frm.refresh();
		// 			}
		// 		});
		// 	}).addClass('btn-primary');;
		// }
		
	
    },
    setup:function(frm){
        frm.set_query('program', function(doc) {
			return {
				filters: {
					"programs":frm.doc.exam_program
				}
			};
		});
        frm.set_query("academic_term", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year
                }
            };
        });
        frm.set_query('fee_structure', 'fee_structure', function() {
		    return {
				filters: {
					"programs":frm.doc.exam_program,
                    "docstatus":1
				}
			};
		});
        frm.set_query("exam_declaration_no", function() {
			return {
				query:"wsc.wsc.doctype.exam_declaration.exam_declaration.valid_exam_declaration_no",
				filters: {
					"docstatus": 1,
				}
			}
		});
  //       frm.set_query("course_assessment_plan", function() {
  //           var semesters = cur_frm.doc.semesters.map(d => d.semester);
		// 	return {
		// 		filters: {
		// 			"programs":frm.doc.exam_program,
  //                   "program":["in", semesters],
		// 			"academic_year":frm.doc.academic_year,
  //                   "docstatus":1
		// 		}
		// 	};
		// });
        frm.set_query('semester', 'semesters', function() {
		    return {
				filters: {
					"programs":frm.doc.exam_program
				}
			};
		});
        frm.fields_dict['fee_structure'].grid.get_field("fee_structure").get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    "fee_type": "Exam Fees",
                    "programs":frm.doc.exam_program
                }
            }
        }
        frm.fields_dict['courses_offered'].grid.get_field("courses").get_query = function(doc, cdt, cdn) {
            var semesters = cur_frm.doc.semesters.map(d => d.semester);
            return {
                query: 'wsc.wsc.doctype.exam_declaration.exam_declaration.filter_courses',
                filters: {
                    "program":semesters
                }
            };
        }
        
    },
	get_courses: function(frm) {
		frm.clear_table("courses_offered");
        frappe.call({
            method: 'get_courses',
            doc: frm.doc,
            args: { 
                year_end_date:frm.doc.year_end_date,
            },
            callback: function(r) {
                if (r.message) {
                    (r.message).forEach(element => {
                        var c = frm.add_child("courses_offered")
                        c.courses = element.name
                        c.course_code = element.course_code
                        c.course_name = element.course_name
                        c.semester = element.semester
                    });
                    frm.refresh_field("courses_offered")
                }
            }
        });
	},
    // get_students:function(frm){
	// 	frm.clear_table("students");
	// 	frappe.call({
	// 		method: "wsc.wsc.doctype.exam_declaration.exam_declaration.get_students",
	// 		args: {
	// 			programs: frm.doc.exam_program,
	// 			academic_term: frm.doc.academic_term,
    //             class_data: frm.doc.class,
    //             minimum_attendance_criteria:frm.doc.minimum_attendance_criteria,
	// 		},
	// 		callback: function(r) {
				
	// 			(r.message).forEach(element => {
	// 				var row = frm.add_child("students")
	// 				row.student=element.student
	// 				row.student_name=element.student_name
    //                 row.roll_no = element.roll_no
    //                 row.registration_number = element.permanant_registration_number
	// 			});
	// 			frm.refresh_field("students")
    //             frm.save();
	// 			frm.set_value("total_enrolled_student",(r.message).length)
	// 		}
			
	// 	});
	// },
}); 



frappe.ui.form.on("Exam Declaration Fee Item",{
    fee_structure: function(frm,cdt,cdn){
        var row = locals[cdt][cdn]
        frappe.db.get_value("Fee Structure", {'name':row.fee_structure,  "docstatus":1},'total_amount', resp => {
            row.amount = resp.total_amount
            frm.refresh_fields(row.amount)
        })
    }
})
// frappe.ui.form.on('Exam Declaration', {
//     refresh: function(frm) {
// 		if(frm.doc.docstatus > 0) {
// 			frm.add_custom_button(__('Accounting Ledger'), function() {
// 				frappe.route_options = {
// 					voucher_no: frm.doc.name,
// 					from_date: frm.doc.posting_date,
// 					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
// 					company: frm.doc.company,
// 					group_by: '',
// 					show_cancelled_entries: frm.doc.docstatus === 2
// 				};
// 				frappe.set_route("query-report", "General Ledger");
// 			}, __("View"));
// 		}
// 	}
// })

frappe.ui.form.on("Exam Courses", "fee_structure", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    var a=0;
    if (d.fee_structure){
        a=frm.doc.fee_structure.length;
        frm.set_value("fee_structure_count", a);
        if(a>=1){
            frm.set_df_property('fee_structure', 'cannot_add_rows', true);
            frm.set_df_property('fee_structure', 'cannot_delete_rows', true);
        }
    }
});


frappe.ui.form.on('Exam Declaration', {
    to_date: function(frm) {
        var selectedDate = frappe.datetime.str_to_obj(frm.doc.to_date);
        var exam_start_date = frappe.datetime.str_to_obj(frm.doc.exam_start_date);
    
        if (selectedDate <= get_today()) {
        frappe.msgprint('Please select a date after today.');
        frm.set_value('to_date', '');
        } else if (selectedDate > exam_start_date) {
        frappe.msgprint('Please select a date on or before Exam Start Date');
        frm.set_value('to_date', '');
        }
        // if (frm.doc.exam_start_date === null || typeof frm.doc.exam_start_date  === 'undefined'){
        //     frappe.msgprint('Please select Exam Start Date');
        //     frm.set_value('to_date', '');
        // }
    }
  });

