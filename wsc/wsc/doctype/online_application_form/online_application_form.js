// Copyright (c) 2024, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Online Application Form', {

	districts:function(frm){
        frm.set_value("blocks","")
    },
	setup: function(frm) {
        console.log(frm.doc);
        frm.doc.hostel_required = 1;
        
        frm.set_query("blocks", function() {
            return {
                filters: [
                    ["Blocks","districts","=",frm.doc.districts]
                ]
            }; 
        });

        frm.set_query("districts", function() {
            return {
                filters: {
                    "state":frm.doc.state
                }
            };
        });
	},
	after_save:function(frm){
        // frm.set_df_property('image', 'reqd', 1);
		frm.trigger("hide_n_show_child_table_fields");
    },
    go_to_top:function(frm){
        window.scrollTo(0, 0);
    },
    on_submit: function(frm){  
        frappe.msgprint({
            title: __('Declaration'),
            message:__('I hereby confirm that, all the data furnished in the form are correct and if any information is found incorrect then my candidature for admission will be cancelled. In case of any wrong information leading to legal, reputational hazard for WSC, it will have the right to take legal action. The final decision of application and admission process is solely lies with WSC. WSC can change the process of admission including data at its own discretion'),
            primary_action: {
                label: __("Yes"),
                action: function () {
                    if (frm.doc.docstatus==1){
                        frappe.msgprint({
                            title: __('Notification'),
                            indicator: 'purple',
                            message: __('Your Application form is Successfully Submitted. Please Notedown Your Acknowledge No. <b>{0}</b> for Future reference.',[frm.doc.name]),
                            primary_action: {
                                'label': 'Kindly Print the Application Form For the Future Admission Process',
                                }
							});
						}
					},
				}
			})
		},

	//Previously Used
	// category: function(frm) {
    //     // frappe.call({
    //     //     method: "wsc.wsc.doctype.student_applicant.get_cateogry_details",
    //     //     args: {
    //     //         category:frm.doc.category
    //     //     },
    //     //     callback: function(r) {
    //     //         if (r.message) {
    //     //             frm.set_value("gender",r.message['gender'])               
    //     //         }
    //     //     }
    //     // });
	// 	// 
	// },
	first_name:function(frm){
		var fieldname = 'first_name';
		var field_value = frm.doc[fieldname];
		frm.set_value(fieldname, field_value.toUpperCase());
	},
	middle_name:function(frm){
		var fieldname = 'middle_name';
		var field_value = frm.doc[fieldname];
		frm.set_value(fieldname, field_value.toUpperCase());
	},
	last_name:function(frm){
		var fieldname = 'last_name';
		var field_value = frm.doc[fieldname];
		frm.set_value(fieldname, field_value.toUpperCase());
	},
	program_grade(frm){
        frm.set_value("program_priority",[]);    
    },
	department(frm){
		frm.set_value("program","")
		frm.set_value("student_admission","")
		frm.set_value("programs","")
        frm.set_value("education_qualifications_details",[]);    
		frm.set_value("education_qualifications_details","")
		frappe.call({
            method: "wsc.wsc.doctype.online_application_form.online_application_form.get_courses",
            args: {
				department:frm.doc.department,
				program_grade:frm.doc.program_grade,
				academic_term:frm.doc.academic_term,
				gender:frm.doc.gender,
            },
			callback: function(r) { 
				if(r.message){
					frappe.model.clear_table(frm.doc, 'program_priority');
					(r.message).forEach(element => {
						var c = frm.add_child("program_priority")
						c.programs=element.admission_program
						c.semester=element.semester
						c.department=element.department
						c.student_admission=element.name
					});
				}
				frm.refresh_field("program_priority")
			}  
        });
    },
	academic_term(frm){
        frm.set_value("program_priority",[]);    
    },
	student_category(frm){
        frm.set_value("program_priority",[]);  
		frm.trigger("get_education_and_document_list");  
    },
	gender(frm){
        frm.set_value("program_priority",[]);  
		frm.set_value("program_priority","")
		frm.trigger("get_education_and_document_list");  
    },
	refresh:function(frm){
		if (frm.doc.application_status==="Applied" && frm.doc.docstatus===1 && !frappe.user.has_role(["Applicant"])) {
			frm.add_custom_button(__("Approve"), function() {
				frm.set_value("application_status", "Approved");
				frm.save_or_update();

			}, 'Actions');

			frm.add_custom_button(__("Not Approve"), function() {
				frm.set_value("application_status", "Not Approved");
				frm.save_or_update();
			}, 'Actions');           
		}
		if (frm.doc.application_status==="Approved" && frm.doc.docstatus===1 && !frappe.user.has_role(["Applicant"])) {
			frm.add_custom_button(__("Permission to Upload Documents"), function() {
				frm.set_value("is_applicant_reported", 1);
				frm.save_or_update();
			});
		}
		if (frm.doc.is_applicant_reported==1){
			frm.remove_custom_button("Permission to Upload Documents")
		}
		frm.set_df_property('education_qualifications_details', 'cannot_add_rows', true);
        // frm.set_df_property('education_qualifications_details', 'cannot_delete_rows', true);
		frm.set_df_property('program_priority', 'cannot_add_rows', true);
        // frm.set_df_property('program_priority', 'cannot_delete_rows', true);
		frm.add_custom_button("Instruction", () => {
			frappe.new_doc("Application Form Instruction")
		});
		if(frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){
			frm.set_value("student_email_id", frappe.session.user)
			frm.set_df_property('student_email_id', 'read_only', 1);
		}
	},
	before_load: function(frm) {
        frm.trigger("hide_n_show_child_table_fields");
    },
	hide_n_show_child_table_fields(frm){
        var df = frappe.meta.get_docfield("Program Priority","approve", frm.doc.name);
        df.hidden = 1
	},
	onload:function(frm){
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year
				}
			};
		});
		// frm.fields_dict['program_priority'].grid.get_field('').get_query = function(doc, cdt, cdn) 
		frm.fields_dict['program_priority'].grid.get_field('select_your_preferences').get_query = function(doc){
			var num = [];
			$.each(doc.program_priority, function(idx, val){
				if (val.select_your_preferences) num.push(val.select_your_preferences);
				val.select_your_preferences.preventDefault();
			});
			val.select_your_preferences.preventDefault();
			return { filters: [['Numbers', 'name', 'not in', num]] };
		};
		// frm.fields_dict['program_priority'].grid.get_field('programs').get_query = function(doc, cdt, cdn) {
		// 	return {   
		// 		query: 'wsc.wsc.doctype.online_application_form.online_application_form.get_validate_course', 
		// 		filters:{
		// 			"department":frm.doc.department,
		// 			"program_grade":frm.doc.program_grade,
		// 			"academic_term":frm.doc.academic_term,
		// 			"gender":frm.doc.gender
		// 		}
		// 	}
		// }

		 
		frm.set_query("department", function(){
	        return{
	            filters:{
	                "is_group":0,
	                "is_stream": 1
	            }
	        }
	    });
	},
	get_education_and_document_list(frm){
		frm.set_value("education_qualifications_details",[]);
	},
});

frappe.ui.form.on("Education Qualifications Details", "total_marks", function(frm, cdt, cdn) {
   
	var data = locals[cdt][cdn];

	if(data.total_marks>=data.earned_marks){
		data.total_marks==" " && data.earned_marks==" "
		data.score=(data.earned_marks/data.total_marks)*100	
	}
	else{
		data.score=""
		data.earned_marks=""
		refresh_field("score", data.name, data.parentfield);
		refresh_field("earned_marks", data.name, data.parentfield);
		frappe.msgprint("Earned Marks is greater then the Total Marks.")
	}       
	cur_frm.refresh_field ("education_qualifications_details");
});

frappe.ui.form.on("Education Qualifications Details", "percentage_cgpa", function(frm, cdt, cdn) {
   
	var data = locals[cdt][cdn];

	data.score=""
	data.cgpa=""
	data.total_marks=""
	data.earned_marks=""

	refresh_field("score", data.name, data.parentfield);
	refresh_field("cgpa", data.name, data.parentfield);
	refresh_field("total_marks", data.name, data.parentfield);
	refresh_field("earned_marks", data.name, data.parentfield);

});

frappe.ui.form.on("Education Qualifications Details", "earned_marks", function(frm, cdt, cdn) {
   
	var data = locals[cdt][cdn];

	if(data.total_marks>=data.earned_marks){
		data.total_marks==" " && data.earned_marks==" "
		data.score=(data.earned_marks/data.total_marks)*100
	}
	else if (data.earned_marks>data.total_marks){
		data.earned_marks=""
		refresh_field("earned_marks", data.name, data.parentfield);
		data.score=""
		refresh_field("score", data.name, data.parentfield);
		frappe.throw("Earned Marks is greater then the Total Marks.")
	}       
	cur_frm.refresh_field ("education_qualifications_details");
});	

frappe.ui.form.on("Education Qualifications Details", "cgpa", function(frm, cdt, cdn) {
	var data = locals[cdt][cdn];
	if(data.cgpa<=10 && data.cgpa>=0){
		data.score=data.cgpa*10   
	}
	else if(data.cgpa>10.000 || data.cgpa<0){
		data.score=""
		data.cgpa=""
		refresh_field("score", data.name, data.parentfield);
		refresh_field("cgpa", data.name, data.parentfield);
		frappe.throw("Please enter your valid CGPA")
	}
	else{
		frappe.throw("Wrong Entry")
	}
	cur_frm.refresh_field ("education_qualifications_details");
});    

// frappe.ui.form.on("Program Priority" , {
//     program_priority_remove: function(frm , cdt , cdn) {
//         frappe.model.clear_table(frm.doc, 'education_qualifications_details');  
//         frm.refresh();
//         frm.refresh_field("education_qualifications_details")
//     }
// });

frappe.ui.form.on("Program Priority", "programs", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if(d.programs.length === 0){
        console.log(d);
    }
	if (!frm.doc.department){
        frappe.msgprint("Please Fill Department First")
        d.programs=''
    }
    if (!frm.doc.program_grade){
        frappe.msgprint("Please Fill Course Type First")
        d.programs=''
    }
    if (!frm.doc.academic_year){
        frappe.msgprint("Please Fill Academic Year First")
        d.programs=''
    }
    if (!frm.doc.student_category){
        frappe.msgprint("Please Fill Caste Category First")
        d.programs=''
    }
	if (!frm.doc.gender){
        frappe.msgprint("Please Fill Gender First")
        d.programs=''
    }
    if (d.programs){
        frappe.call({
            method: "wsc.wsc.doctype.student_applicant.get_admission_and_semester_by_program",
            args: {
               programs:d.programs,
               program_grade:frm.doc.program_grade,
               academic_year:frm.doc.academic_year
            },
            callback: function(r) { 
                if (r.message){
                    if (r.message["no_record_found"]){
                        frappe.msgprint("Admission Not Declared for this Course")
                        frappe.model.set_value(cdt, cdn, "programs",'');
                    }
						frm.set_value("program",r.message['semester'])
                        frm.set_value("programs",r.message['admission_program'])
                        frm.set_value("student_admission",r.message['name'])
                    frappe.model.set_value(cdt, cdn, "student_admission", r.message['name']);
                    frappe.model.set_value(cdt, cdn, "semester", r.message['semester']);
                }
            } 
        }); 
    }
});
