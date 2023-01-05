frappe.ui.form.on('Program Enrollment', {
	seat_reservation_type:function(frm){
        if(frm.doc.seat_reservation_type){
            frappe.call({
                method: "wsc.wsc.doctype.program_enrollment.get_available_seats",
                args:{
                    "student_applicant":frm.doc.reference_name,
                    "seat_reservation_type":frm.doc.seat_reservation_type,
                    "programs":frm.doc.programs,
                    "program":frm.doc.program
                },
                callback: function(r) {
                    if(r.message) {
                        frm.set_value('available_seats', r.message)
                        frm.refresh_field("available_seats")
                    }
                }
            });
        }
    },
    refresh(frm){
         if(frm.doc.reference_doctype== "Student Applicant" && frm.doc.reference_name){
            if (frm.doc.__islocal){
                frm.set_value('program','')
                frm.set_value('programs','')
            }
            frm.set_query('programs', function() {
                return{
                    query: 'wsc.wsc.doctype.program_enrollment.get_programs_stud_app',
                    filters: {
                        "student_applicant":frm.doc.reference_name
                    }
                }
            });
            frm.set_query('program', function() {
                return{
                    query: 'wsc.wsc.doctype.program_enrollment.get_program_stud_app',
                    filters: {
                        "student_applicant":frm.doc.reference_name,
                        "programs":frm.doc.programs
                    }
                }
            });
            frm.set_query("seat_reservation_type", function() {
                return {
                    query: 'wsc.wsc.doctype.program_enrollment.get_seat_reservation_type',
                    filters: {
                        "student_applicant": frm.doc.reference_name,
                    }
                };
            });
        
    
        }
       
        if (!frm.doc.__islocal && frm.doc.boarding_student){
			frm.add_custom_button("Hostel Admission", () => {
				let data = {}
				data.student=frm.doc.student
				data.student_name=frm.doc.student_name
                data.programs=frm.doc.programs
                if (frm.doc.reference_doctype=="Student Applicant"){
                    frappe.db.get_doc("Student Applicant",frm.doc.reference_name).then(( resp ) => {
                        data.hostel_type=resp.room_type
                        data.capacity=resp.sharing
                        frappe.new_doc("Hostel Admission", data)
                    });
                }
                else{
                    frappe.new_doc("Hostel Admission", data)
                }
			},__('Create'));
		}
        frm.set_df_property('program','label','Semester')
        // if (["Student Applicant","Student Exchange Applicant"].includes(frm.doc.reference_name)){
        //     frm.set_df_property('programs','read_only',1)
        //     frm.set_df_property('program','read_only',1)
        //     frm.set_df_property('fee_structure_item','read_only',1)
        // }
        frm.set_query('student', function() {
			return{
				query: 'wsc.wsc.doctype.program_enrollment.get_students',
				filters: {
					"programs":frm.doc.programs
				}
			}
		});
        frm.trigger("set_fields_readonly")

        
    },
    setup(frm){
        frm.set_query("course","courses", function() {
            return {
                query: 'wsc.wsc.doctype.program_enrollment.get_courses',
                filters: {
                    "semester":frm.doc.program
                }
            };
        });
        
        if(!frm.doc.reference_name || frm.doc.reference_doctype=="Branch Sliding Application"){
            frm.set_query("program", function() {
                return {
                    filters: {
                        "programs":frm.doc.programs
                    }
                };
            });
            frm.set_query("programs", function() {
                return {
                    filters: {
                        "program_grade":frm.doc.program_grade
                    }
                };
            });
            frm.set_query("student_category", function() {
                return {
                    query: 'wsc.wsc.doctype.program_enrollment.get_cat',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
        }
        frm.set_query("academic_term", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year
                }
            };
        });

    },
    program(frm){
        if (frm.doc.program){
            frappe.call({
                method: "wsc.wsc.doctype.program_enrollment.get_program_courses",
                args: {
                    semester: frm.doc.program,
                    year_end_date: frm.doc.year_end_date
                },
                callback: function(r) { 
                    if(r.message){
                        frappe.model.clear_table(frm.doc, 'courses');
                        (r.message).forEach(element => {
                            var c = frm.add_child("courses")
                            c.course=element.name
                            c.course_name=element.course_name
                            c.course_code=element.course_code
                        });
                    }
                    frm.refresh_field("courses")
                } 
                
            }); 
            frappe.call({
                method: "wsc.wsc.doctype.program_enrollment.get_academic_calender_table",
                args: {
                    programs:frm.doc.programs,
                    semester: frm.doc.program,
                },
                callback: function(r) { 
                    if(r.message){
                        frappe.model.clear_table(frm.doc, 'academic_events_table');
                        (r.message).forEach(d => {
                            var c = frm.add_child("academic_events_table")
                            c.academic_events=d.academic_events,
                            c.start_date=d.start_date,
                            c.end_date=d.end_date,
                            c.duration=d.duration
                        });
                    }
                    frm.refresh_field("academic_events_table")
                } 
            });   
        }
    },
    set_fields_readonly(frm){
        if (["Student Applicant","Student Exchange Applicant"].includes(frm.doc.reference_doctype)){
            frm.set_df_property('student','read_only',1)
            frm.set_df_property('student_category','read_only',1)
            frm.set_df_property('program_grade','read_only',1)
            frm.set_df_property('academic_year','read_only',1)
            frm.set_df_property('academic_term','read_only',1)
        }
    }
})

frappe.ui.form.on('Program Enrollment Course', {
	courses_add: function(frm){
		frm.fields_dict['courses'].grid.get_field('course').get_query = function(doc) {
			return {
                query: 'wsc.wsc.doctype.program_enrollment.get_courses',
                filters: {
                    "semester":frm.doc.program
                }
            };
		};
	}
});

frappe.ui.form.on('Program Enrollment', {
	student: function(frm) {
		if (frm.doc.student) {
			frappe.call({
				method:"wsc.wsc.doctype.program_enrollment.get_roll",
				args: {
					"student": frm.doc.student,
				},
				callback: function(r) {
					if(r){
                        var info=r.message
                        
                        if(info.roll_no!=null){
                            frm.set_value('roll_no',info.roll_no)
                            frm.set_df_property('roll_no','read_only',1)
                        }
                        if(info.permanant_registration_number!=null){
                            frm.set_value('permanant_registration_number',info.permanant_registration_number)
                            frm.set_df_property('permanant_registration_number','read_only',1)
                        }
                        if(info.student_category!=null){
                            frm.set_value('student_category',info.student_category)
                            frm.set_df_property('student_category','read_only',1)
                        }
                        else{
                            frm.set_df_property('student_category','hidden',1)
                        }
					}
				}
			});
		}
	},
});

frappe.provide("erpnext.accounts.dimensions");

frappe.ui.form.on("Program Enrollment", {
	setup: function(frm) {
		frm.add_fetch("fee_structure", "receivable_account", "receivable_account");
		frm.add_fetch("fee_structure", "income_account", "income_account");
		frm.add_fetch("fee_structure", "cost_center", "cost_center");
	},

	company: function(frm) {
		erpnext.accounts.dimensions.update_dimension(frm, frm.doctype);
	},

	onload: function(frm) {
		frm.set_query("academic_term", function() {
			return{
				"filters": {
					"academic_year": (frm.doc.academic_year)
				}
			};
		});
		frm.set_query("fee_structure", function() {
			return{
				"filters":{
					"academic_year": (frm.doc.academic_year)
				}
			};
		});
		frm.set_query("receivable_account", function(doc) {
			return {
				filters: {
					'account_type': 'Receivable',
					'is_group': 0,
					'company': doc.company
				}
			};
		});
		frm.set_query("income_account", function(doc) {
			return {
				filters: {
					'account_type': 'Income Account',
					'is_group': 0,
					'company': doc.company
				}
			};
		});
		if (!frm.doc.posting_date) {
			frm.doc.posting_date = frappe.datetime.get_today();
		}

		erpnext.accounts.dimensions.setup_dimension_filters(frm, frm.doctype);
	},

	refresh: function(frm) {
		if(frm.doc.docstatus == 0 && frm.doc.set_posting_time) {
			frm.set_df_property('posting_date', 'read_only', 0);
			frm.set_df_property('posting_time', 'read_only', 0);
		} else {
			frm.set_df_property('posting_date', 'read_only', 1);
			frm.set_df_property('posting_time', 'read_only', 1);
		}
		if(frm.doc.docstatus > 0 ) {
            if(frm.doc.voucher_no != null){
                frm.add_custom_button(__('Accounting Ledger'), function() {
                    frappe.route_options = {
                        voucher_no: frm.doc.voucher_no,
                        from_date: frm.doc.enrollment_date,
                        to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
                        company: frm.doc.company,
                        group_by: '',
                        show_cancelled_entries: frm.doc.docstatus === 2
                    };
                    frappe.set_route("query-report", "General Ledger");
                }, __("View"));
            }
			
		}
	},   	
});
