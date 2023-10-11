frappe.ui.form.on('Student Applicant', {
    // first_name:function(frm){    
    //     let fname=frm.doc.first_name;    
    //     let lname=frm.doc.last_name;    
    //     frm.set_value("title",fname+" "+lname);    
    // },   
    // last_name:function(frm){        
    //     let fname=frm.doc.first_name;        
    //     let lname=frm.doc.last_name;        
    //     frm.set_value("title",fname+" "+lname)
    // },
    // on_submit:function(frm){
    //     frappe.msgprint({
    //         title: __('Notification'),
    //         indicator: 'purple',
    //         message: __('Your Application form is Successfully Submitted. Please Notedown Your Application No. <b>{0}</b> for Future reference.',[frm.doc.name]),
    //         primary_action: {
    //             'label': 'Kindly Print the Application Form For the Future Admission Process',
    //             }
    //     });
      
        
    // },
    go_to_top:function(frm){
        window.scrollTo(0, 0);
    },
    onload: function(frm) {
        //For Counselling Based Program Priority
        
        if (frm.doc.couselling_start === 1){
            frm.set_df_property("counselling_based_program_priority" , "hidden" , 0)
        }
         
        frm.set_query("counselling_structure", function() {
            return {
                filters: {
                    "program_grade":frm.doc.program_grade,
                    "academic_year":frm.doc.academic_year
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
        frm.fields_dict['program_priority'].grid.get_field('programs').get_query = function(doc, cdt, cdn) {
            return {   
                query: 'wsc.wsc.doctype.student_applicant.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.department,
                    "program_grade":frm.doc.program_grade
                }
            }
        }
        //New Code by Tousiff//
        // frm.fields_dict['counselling_based_program_priority'].grid.get_field('programs').get_query = function(doc, cdt, cdn) {
        //     return {   
        //         query: 'wsc.wsc.doctype.student_applicant.filter_programs_by_department_counselling', 
        //         filters:{
        //             "department":frm.doc.department,
        //             "program_grade":frm.doc.program_grade
        //         }
        //     }
        // }
        //End
        frm.fields_dict['counselling_based_program_priority'].grid.get_field('programs').get_query = function(doc, cdt, cdn) {
            return {   
                query: 'wsc.wsc.doctype.student_applicant.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.department,
                    "program_grade":frm.doc.program_grade
                }
            }
        }
        frm.set_query("department", function(){
	        return{
	            filters:{
	                "is_group":0,
	                // "is_stream": 0
	            }
	        }
	    });
        

    },
    states(frm){
        frm.set_value("country_code",'')
        frappe.db.get_value('State',{'name':frm.doc.states},['country'],(val1) =>
        {
            frappe.db.get_value('Country',{'name':val1.country},['country_phone_code'],(val2) =>
            {
                frm.set_value("country_code",val2.country_phone_code)
            })
        })
    },

    after_save: function(frm) {
        frm.trigger("hide_n_show_child_table_fields");
    },
    districts:function(frm){
        frm.set_value("blocks","")
    },
    setup: function(frm) {
        console.log(frm.doc);
        //Hostel Required Checkbox
        frm.doc.hostel_required = 1;
        
        frm.set_query("blocks", function() {
            return {
                filters: [
                    // "districts":frm.doc.districts
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

        frm.set_query("districts", "exam_center_locations" , function(_doc , cdt, cdn){
            var d = locals[cdt][cdn];
            return {
                filters: {
                    "state":d.state
                }
            }
        })      
    },
    hide_n_show_child_table_fields(frm){
        var df = frappe.meta.get_docfield("Education Qualifications Details","qualification_", frm.doc.name);
        df.hidden = 1
        var df0 = frappe.meta.get_docfield("Education Qualifications Details","qualification", frm.doc.name);
        df0.hidden = 0
        // var df1 = frappe.meta.get_docfield("Education Qualifications Details","year_of_completion_", frm.doc.name);
        // df1.hidden = 1
        var df11 = frappe.meta.get_docfield("Education Qualifications Details","year_of_completion", frm.doc.name);
        df11.hidden = 0
        var df2 = frappe.meta.get_docfield("Document List","document_name_", frm.doc.name);
        df2.hidden = 1
        var df4 = frappe.meta.get_docfield("Document List","document_name", frm.doc.name);
        df4.hidden = 0
        var df5 = frappe.meta.get_docfield("Document List","attach", frm.doc.name);
        var df6 = frappe.meta.get_docfield("Document List","attached", frm.doc.name);
        if(df5!=null){
            df6.default = 0
        }
    },
    before_load: function(frm) {
        frm.trigger("hide_n_show_child_table_fields");
    },
    after_save:function(frm){
        frm.set_df_property('image', 'reqd', 1);
    },
    review_student: function(frm) {
		frappe.model.open_mapped_doc({
			method: "wsc.wsc.doctype.student_applicant.review_student",
			frm: frm
		})
    },
    // before_submit: function(frm){
    //     frappe.msgprint({
    //         title: __('Notification'),
    //         message: __('I hereby declare that the information given by me in the Application is true. If any point of time, I am found to have concealed any information or given any false document, my application shall liable to be summarily rejected without notice or compensation.'),
    //         primary_action:{
    //             action(values) {
    //                 console.log(values);
    //             }
    //         }
    //     });
    // },
    before_submit: function(frm){
        frm.set_value("declaration", "I hereby declare that I have read and understood all the instructions clearly. The information given by me in the application is true and to the best of my knowledge. I understand and accept that World Skill Center reserves the rights to reject my application, if any of the information provided by me is found to be false.");
        let fname=frm.doc.first_name;    
        let lname=frm.doc.last_name;    
        frm.set_value("title",fname+" "+lname);  
    },
    
    on_submit: function(frm){  
        
        frappe.msgprint({
            title: __('Declaration'),
            message:__('I hereby declare that I have read and understood all the instructions clearly. The information given by me in the application is true and to the best of my knowledge.<br> I understand and accept that World Skill Center reserves the rights to reject my application, if any of the information provided by me is found to be false.'),
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
    refresh(frm){
        if (frm.doc.application_status==="Applied" && frm.doc.docstatus===1 ) {
			frm.add_custom_button(__("Approve"), function() {
				frm.set_value("application_status", "Approved");
				frm.save_or_update();

			}, 'Actions');

			frm.add_custom_button(__("Not Approve"), function() {
				frm.set_value("application_status", "Hold");
				frm.save_or_update();
			}, 'Actions');           
		}
    //     if (frm.doc.application_status=="Rejected"){
    //         frm.add_custom_button(__("Approve"), function() {
    //             frm.set_value("application_status", "Approved");
    //             frm.save_or_update();
    //     }, 'Actions');
    // };
        // frm.set_df_property('application_status', 'options', ['Applied', 'Approved','Hold', 'Not Approved','Rejected']);

        frm.remove_custom_button("Reject","Actions");

        frm.fields_dict.go_to_top.$input.addClass(' btn btn-primary');
        if(!frm.is_new()){
            frm.add_custom_button(__("Preview"), function()  {
                frm.trigger("review_student")
            }).addClass("btn-primary");
        }
        if (frm.doc.docstatus==1){
            frm.remove_custom_button("Preview")
        }
            frm.add_custom_button("Instruction", () => {
                frappe.new_doc("Application Form Instruction")
            });    
            frm.add_custom_button("Instruction", () => {
                frappe.new_doc("Application Form Instruction")
            });    

        // }
        if(frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){
			frm.set_value("student_email_id", frappe.session.user)
			frm.set_df_property('student_email_id', 'read_only', 1);
		}

        frm.set_df_property('student_rank', 'cannot_add_rows', true)
		// frm.set_df_property('student_rank', 'cannot_delete_rows', true) 
        frm.set_df_property('education_qualifications_details', 'cannot_add_rows', true);
        frm.set_df_property('education_qualifications_details', 'cannot_delete_rows', true);
        frm.set_df_property('document_list', 'cannot_add_rows', true);
        frm.set_df_property('document_list', 'cannot_delete_rows', true);
        
        if (cur_frm.doc.document_list){
            cur_frm.doc.document_list.forEach(data=>{
                var dn = frappe.meta.get_docfield("Document List", "document_name",data.name);
                dn.read_only=1;
            })
        }
        frm.set_df_property('image', 'hidden', 1);
        frm.set_df_property('program', 'hidden', 1);
        frm.set_df_property('program', 'reqd', 0);
        frm.set_df_property('program', 'allow_on_submit', 1);
        frm.set_df_property('programs_', 'hidden', 1);
        frm.set_df_property('student_admission', 'hidden', 1);
        frm.remove_custom_button("Enroll")
        
        if (!cur_frm.doc.__islocal && frappe.user.has_role(["Student"]) && !frappe.user.has_role(["System Manager"])){
            frm.remove_custom_button("Reject","Actions");
            frm.remove_custom_button("Approve","Actions");
            frm.remove_custom_button("Not Approve","Actions");
            
        }

        if (!cur_frm.doc.__islocal && frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){
            frm.remove_custom_button("Reject","Actions");
            frm.remove_custom_button("Approve","Actions");
            frm.remove_custom_button("Not Approve","Actions");
            
        }
        if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role(["System Manager"])){
            frm.set_df_property('application_status', 'read_only', 1);
        }
        if (frm.doc.application_status === "Approved" && frm.doc.docstatus === 1 && (frappe.user.has_role(["Education Admission Head"]))) {
            frappe.db.get_value('User',{'name':frappe.session.user},['module_profile'],(val) =>
			{
                if (val.module_profile!="Student"){
                    // frm.trigger("show_fees_button")
                    frappe.db.get_list("Program Enrollment", {
                        filters:{"reference_doctype":"Student Applicant","reference_name":frm.doc.name},
                        fields: ["name"]
                    }).then((data) => { 
                        if (data.length==0) 
                        console.log("Promise Success");
                        frm.add_custom_button(__("Enroll"), function()  {
                            frm.trigger("enroll_student")
                        }).addClass("btn-primary");
                    })
                    .catch((err) => {
                        console.log(err);
                    })
                }
			});
        }
        else if (frm.doc.enrollment_status=="Not Enrolled"){
            frm.remove_custom_button("Enroll")
        }
        // frappe.call({
        //     method: "wsc.wsc.doctype.student_applicant.get_qualification_list",
        //     callback: function(r) {
        //         cur_frm.doc.education_qualifications_details.forEach(data=>{
        //             var df = frappe.meta.get_docfield("Education Qualifications Details","qualification_", data.name);
        //             df.options = r.message.qual;
        //             var df1 = frappe.meta.get_docfield("Education Qualifications Details","year_of_completion_", data.name);
        //             df1.options = r.message.acadmic;
        //         })
        //     }
        // });
        
        // set Sharing Types 
        frappe.call({
            method: "wsc.wsc.doctype.student_applicant.get_sharing_type",
            callback: function(r) {
                frm.set_df_property('sharing', 'options', r.message);
            }
        }); 
  
        // clear education qualification details table

        // if (frm.doc.__islocal){
        //     frm.set_value("education_qualifications_details",[]);
        //     // frm.set_value("student_category","")
        // }      

    },
    // couselling_start: function(frm){
    //     let field = frm.get_field("counselling_based_program_priority")
    //     let isHidden = field.df.hidden

    //     if (isHidden){
    //         frm.set_df_property("counselling_based_program_priority" , "hidden" , 0)
    //     } else {
    //         frm.set_df_property("counselling_based_program_priority" , "hidden" , 1)
    //     }
    // },
    counselling_structure: function(frm) {
        frm.trigger("get_education_and_document_list");
        frm.set_value("document_list",[]);
    },
    enroll_student: function(frm) {
		frappe.model.open_mapped_doc({
			method: "wsc.wsc.doctype.student_applicant.enroll_student",
			frm: frm
		})
        // frappe.call({
        //     method: "wsc.wsc.doctype.student_applicant.enroll_student",
        //     args: {
        //         frm:frm
        //     },
        //     // callback: function(r) {
        //     //     console.log(r);
        //     //     var doc = frappe.model.sync(r.message);
        //     //     frappe.set_route("Form", doc[0].doctype, doc[0].name);
        //     // }
        // });
	},
//     show_fees_button(frm){
//         if (frm.doc.name && frm.doc.application_status=="Approved"){
//             frm.add_custom_button(__("Fees"), function() {
//                 frappe.model.open_mapped_doc({
//                     method: "wsc.wsc.doctype.student_applicant.create_fees",
//                     frm: frm,
//                 });
//             })
//     }
// },
    program_grade(frm){
        // frm.trigger("get_counselling_structure");
        frm.set_value("counselling_structure",'')
        frm.set_value("program_priority",[]);
        frm.trigger("get_qualification_detail_for_admission");
        
    },
    academic_year(frm){
        // frm.trigger("get_counselling_structure");
        frm.set_value("program_priority",[]);
        frm.set_value("counselling_structure",'')
        frm.set_value("counselling_structure",'');
    },
    department(frm){
        // frm.trigger("get_counselling_structure");
        frm.set_value("counselling_structure",'')
        frm.set_value("program_priority",[]);
    },
    student_category(frm){
        frm.trigger("get_education_and_document_list");
    },
    // get_counselling_structure(frm){
    //     frm.set_value("counselling_structure",'');
    //     if (frm.doc.program_grade && frm.doc.academic_year && frm.doc.department){
    //         frappe.call({
    //             method: "wsc.wsc.doctype.student_applicant.get_counselling_structure",
    //             args:{
    //                program_grade: frm.doc.program_grade,
    //                academic_year: frm.doc.academic_year,
    //                department: frm.doc.department
    //             },
    //             callback: function(r) { 
    //                 if (r.message){
    //                    frm.set_value("counselling_structure",r.message['name']);
    //                 }
    //             } 
    //         });
    //     }
        
    // },
    get_education_and_document_list(frm){
        frm.set_value("education_qualifications_details",[]);
        
        // if (frm.doc.counselling_structure && frm.doc.student_category){
            
        //     frappe.model.with_doc("Counselling Structure", frm.doc.counselling_structure, function() {
        //         var tabletransfer= frappe.model.get_doc("Counselling Structure", frm.doc.counselling_structure)
        //         // frappe.model.clear_table(frm.doc, 'education_qualifications_details');  //Sukalyan Code
        //         $.each(tabletransfer.eligibility_parameter_list, function(index, row){
                    
        //             if(frm.doc.student_category == row.student_category){
        //                 var d = frm.add_child("education_qualifications_details");
        //                 d.qualification = row.parameter;
        //                 d.percentage_cgpa = row.percentagecgpa
        //                 d.mandatory = row.is_mandatory;
        //                 d.admission_percentage = row.eligible_score;
        //             }
        //             // frm.refresh_field("education_qualifications_details");
        //         });
        //         $.each(tabletransfer.counselling_fees, function(index, row){
        //             if(frm.doc.student_category == row.student_category){
        //                 frm.set_value("total_counselling_fee",row.amount) 
        //             }
        //             // frm.refresh_field("total_counselling_fee");
        //         });
        //     });
        // }
       
    },
    // get_qualification_detail_for_admission(frm){
    //     if (!frm.doc.counselling_structure && frm.doc.student_category && (frm.doc.program_priority).length!=0){
    //         frm.set_value("education_qualifications_details",[]);
    //         frappe.call({
    //             method: "wsc.wsc.doctype.student_applicant.get_education_qualifications_details_by_admissions",
    //             args:{
    //                 student_category: frm.doc.student_category,
    //                 admission:  frm.doc.program_priority,
    //                 // self:frm.doc
    //             },
    //             callback: function(resp) { 
    //                 if (resp.message){
    //                     $.each(resp.message, function(index, row){
    //                             var edu_row = frm.add_child("education_qualifications_details");
    //                             edu_row.qualification = row.parameter;
    //                             edu_row.percentage_cgpa = row.percentagecgpa
    //                         frm.refresh_field("education_qualifications_details");
    //                     });
    //                 }
    //             } 
    //         });
    //     }
    // }
})
frappe.ui.form.on("Education Qualifications Details", "total_marks", function(frm, cdt, cdn) {
       
    var data = locals[cdt][cdn];

    if(data.total_marks>=data.earned_marks){
        data.total_marks==" " && data.earned_marks==" "
        data.score=(data.earned_marks/data.total_marks)*100
        
    }
    else{
        // frm.set_value("score","")
        
        // cur_frm.refresh_field (data.score);
        data.score=""
        data.earned_marks=""
        refresh_field("score", data.name, data.parentfield);
        refresh_field("earned_marks", data.name, data.parentfield);
        frappe.msgprint("Earned Marks is greater then the Total Marks.")
    }       
    cur_frm.refresh_field ("education_qualifications_details");
    // if (data.score < data.admission_percentage){
    //     frappe.throw("You are not eligible to apply for these course.")
    // }
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
        // frm.set_value("score","")
    
        data.earned_marks=""
        refresh_field("earned_marks", data.name, data.parentfield);
        data.score=""
        refresh_field("score", data.name, data.parentfield);
        frappe.throw("Earned Marks is greater then the Total Marks.")
    }       
    cur_frm.refresh_field ("education_qualifications_details");
    // if (data.score < data.admission_percentage){
    //     frappe.throw("You are not eligible to apply for these course.")
    // }
 });	
 frappe.ui.form.on("Education Qualifications Details", "cgpa", function(frm, cdt, cdn) {
  
    var data = locals[cdt][cdn];
    if(data.cgpa<=10 && data.cgpa>=0){
        data.score=data.cgpa*10   
    }
    else if(data.cgpa>10.000 || data.cgpa<0){
        data.score=""
        data.cgpa=""
        // data.
        refresh_field("score", data.name, data.parentfield);
        refresh_field("cgpa", data.name, data.parentfield);
        frappe.throw("Please enter your valid CGPA")
    }
    else{
        alert("hey 4")
        frappe.throw("Wrong Entry")
    }
    cur_frm.refresh_field ("education_qualifications_details");
    // if (data.score < data.admission_percentage){
    //     frappe.throw("You are not eligible to apply for these course.")
    // }
 
 });      

 //             "academic_year":frm.doc.academic_year,
 //             'academic_term':frm.doc.academic_term,
 //             "state":d.state,
 //             "district":d.districts,
 //             "available_center":1 

 frappe.ui.form.on("Exam Centre Preference" , {
    // center_name:function(frm){
    //     console.log(frm.doc.exam_center_locations);
    // },
    exam_center_locations_add:function(frm , cdt ,cdn){
        var d = locals[cdt][cdn]

        frm.fields_dict['exam_center_locations'].grid.get_field('center_name').get_query = function(doc){
            var exam_center_list = [];
            // if(!doc.__islocal) exam_center_list.push(doc.name)
            $.each(doc.exam_center_locations , function(idx , val){
                if (val.center_name) exam_center_list.push(val.center_name)
            })
            
            return { filters:[
                        ['Entrance exam select' , 'name' , 'not in' , exam_center_list] , 
                        ['docstatus','=',1] , 
                        ['academic_year' , '=' , frm.doc.academic_year] , 
                        ['academic_term' , '=' , frm.doc.academic_term] ,
                        ['state' , '=' , d.state] , 
                        ['district' , '=' , d.districts] , 
                        ['available_center' , '=' , 1],
                        ['docstatus' , '=' , 1]
                    ]}
        }
    }
 })

frappe.ui.form.on("Program Priority" , {
    program_priority_remove: function(frm , cdt , cdn) {
        frappe.model.clear_table(frm.doc, 'education_qualifications_details');  
        frm.refresh();
        frm.refresh_field("education_qualifications_details")
    }
})

frappe.ui.form.on("Exam Centre Preference" , "center_name" , function(frm , cdt , cdn){
    var d = locals[cdt][cdn];
    var a = 0;
    // if (d.programs && frappe.user.has_role(["Student Applicant"])){
    if (d.center_name){
        a=frm.doc.exam_center_locations.length;
        // frm.set_value("count_programs", a);
        if(a>=3){
            frm.set_df_property('exam_center_locations', 'cannot_add_rows', true);
            frm.set_df_property('exam_center_locations', 'cannot_delete_rows', true);
            // frm.set_df_property('program_priority', 'cannot_insert_below', true);
        }
    }
})

frappe.ui.form.on("Counseling Based Program Priority","programs", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    var a = 0
    frappe.model.set_value(cdt, cdn, "student_admission",'');
    frappe.model.set_value(cdt, cdn, "semester", '');
    if (d.programs){
        a = frm.doc.counselling_based_program_priority.length
        if(a>=3){
            frm.set_df_property('exam_center_locations', 'cannot_add_rows', true);
            frm.set_df_property('exam_center_locations', 'cannot_delete_rows', true);
        } 
        frappe.call({
            method: "wsc.wsc.doctype.student_applicant.get_admission_and_semester_by_program",
            args: {
               programs:d.programs,
               program_grade:frm.doc.program_grade,
               academic_year:frm.doc.academic_year
            },
            callback: function(r) { 
                if (r.message){
                    // console.log(r.message);
                    // if (r.message["no_record_found"]){
                    //     frappe.msgprint("Admission Not Declared for this program")
                    //     frappe.model.set_value(cdt, cdn, "programs",'');
                    // }
                    // var a=0
                    // a=frm.doc.program_priority.length;
                    // frm.set_value("count_programs", a);
                    // if(a<=1){
                        frm.set_value("counselling_semester",r.message['semester'])
                        frm.set_value("counselling_course",r.message['admission_program'])
                    // }
                    // frm.set_value("program",r.message['semester'])
                    // frm.set_value("programs_",r.message['admission_program'])
                    frappe.model.set_value(cdt, cdn, "student_admission", r.message['name']);
                    frappe.model.set_value(cdt, cdn, "semester", r.message['semester']);
                }
            }
        })
    }

 }) 


frappe.ui.form.on("Program Priority", "programs", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    
    if(d.programs.length === 0){
        console.log(d);
    }

    frappe.model.set_value(cdt, cdn, "student_admission",'');
    frappe.model.set_value(cdt, cdn, "semester", '');
    frm.set_value("counselling_structure",'')
    // frm.set_value("program",'')
    if (!frm.doc.program_grade){
        frappe.msgprint("Please Fill Program Grade First")
        d.programs=''
    }
    if (!frm.doc.academic_year){
        frappe.msgprint("Please Fill Academic Year First")
        d.programs=''
    }
    if (!frm.doc.student_category){
        frappe.msgprint("Please Fill Student First")
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
                        frappe.msgprint("Admission Not Declared for this program")
                        frappe.model.set_value(cdt, cdn, "programs",'');
                    }
                    // var a=0
                    // a=frm.doc.program_priority.length;
                    // frm.set_value("count_programs", a);
                    // if(a<=1){
                        frm.set_value("program",r.message['semester'])
                        frm.set_value("programs_",r.message['admission_program'])
                        frm.set_value("student_admission",r.message['name'])
                    // }
                    // frm.set_value("program",r.message['semester'])
                    // frm.set_value("programs_",r.message['admission_program'])
                    frappe.model.set_value(cdt, cdn, "student_admission", r.message['name']);
                    frappe.model.set_value(cdt, cdn, "semester", r.message['semester']);
                    if (r.message['counselling_required']){
                        frm.set_value("counselling_structure",r.message['counselling_structure'])
                    }
                    //##################################for future student applicant in wsc (Tousiff)#########################################3
                    // !frm.doc.counselling_structure && frm.doc.student_category && 
                    // if (frm.doc.program_priority){
                    //     frm.set_value("education_qualifications_details",[]);
                    //     frappe.call({
                    //         method: "wsc.wsc.doctype.student_applicant.get_education_qualifications_details_by_admissions",
                    //         args:{
                    //             student_category: frm.doc.student_category,
                    //             admission:  frm.doc.program_priority,
                    //             // self:frm.doc
                    //         },
                    //         callback: function(resp) { 
                    //             if (resp.message){
                    //                 console.log("edu qualify");
                    //                 console.log(resp.message);
                    //                 $.each(resp.message, function(index, row){
                    //                         var edu_row = frm.add_child("education_qualifications_details");
                    //                         edu_row.qualification = row.parameter;
                    //                         edu_row.percentage_cgpa = row.percentagecgpa;
                    //                         edu_row.mandatory = row.is_mandatory;
                    //                         edu_row.admission_percentage = row.eligible_score;
                    //                     frm.refresh_field("education_qualifications_details");
                    //                 });
                    //                 frm.refresh_field("education_qualifications_details");
                    //             }
                    //             else{
                    //                 // frappe.model.clear_table(frm.doc, 'education_qualifications_details');  //Sukalyan Code
                    //                 frm.refresh_field("education_qualifications_details");
                    //             }
                    //         } 
                    //     });
                    // }
                    //##########################################END########################################################
                    
                }
            } 
        }); 
    }
});

