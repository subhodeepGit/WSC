// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Leave Application for Student","to_date", function(frm, cdt, cdn) { 
//     var df = frappe.meta.get_docfield("Class Wise Leave","leave_applicability_check", cur_frm.doc.name);
//     df.read_only = 0;
//     frm.refresh_field("class_wise_leave")
// });
frappe.ui.form.on('Leave Application for Student', {
    refresh: function(frm) {
        frm.set_df_property('class_wise_leave', 'cannot_add_rows', true);
        frm.set_df_property('class_wise_leave', 'cannot_delete_rows', true);
	},
    onload: function(frm) {
           frappe.call({            
               "method": "wsc.wsc.doctype.room_allotment.room_allotment.get",
               args: {
                   name: frm.doc.student
               },
       
               callback: function (data) {
                   if(!frm.is_new()){
                   frm.add_custom_button(__('Hostel Details'), function(){
                   if(Object.keys(data.message).length!=0){
                   var msg ='Enrollment No. : ' + data.message.name+'<br/>';
                   msg = msg + 'Hostel Registration No. : ' + data.message.hostel_registration_no+'<br/>';
                   msg = msg + 'Hostel : ' + data.message.hostel_id+'<br/>';
                   msg = msg + 'Room Number : ' + data.message.room_number+'<br/>';
                   msg = msg + 'Room Type : ' + data.message.room_type+'<br/>';
                   msg = msg + 'Start Date : ' + data.message.start_date+'<br/>';
                   msg = msg + 'End date : ' + data.message.end_date + '<br/>';
                   msgprint(__(msg));
               }
               else
                   {
                   var daysc = "Student is a day Scholar"
                   msgprint(__(daysc));
                   }
               });
       
               }}
           })
        },
    show_classes: function(frm){
            frappe.call({
                "method": "wsc.wsc.doctype.leave_application_for_student.leave_application_for_student.get_classes",
                args:{
                    from_date:frm.doc.from_date,
                    to_date:frm.doc.to_date,
                    curr:frm.doc.current_education_details
                },
                callback: function(r) {
                    if (r.message){
                        frappe.model.clear_table(frm.doc, 'class_wise_leave');
                        (r.message).forEach(element => {
                            var c = frm.add_child("class_wise_leave")
                            c.class_schedule_id=element.name
                            c.module_name=element.course_name
                            c.class=element.room_name
                            c.schedule_date=element.schedule_date
                            c.from_time=element.from_time
                            c.to_time=element.to_time
                        });
                        frm.refresh_field("class_wise_leave")
                    }
                }
            })
        },
    student: function(frm) {
        frappe.call({
            method: 'wsc.wsc.doctype.leave_application_for_student.leave_application_for_student.current_education',
            args: {
                'student_no': frm.doc.student,
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.clear_table(frm.doc, 'current_education_details');
                    (r.message).forEach(element => {
                        var c = frm.add_child("current_education_details")
                        c.programs=element.programs
                        c.semesters=element.semesters
                        c.academic_year=element.academic_year
                        c.academic_term=element.academic_term
                    });
                    frm.refresh_field("current_education_details")
                }
            },
        })
    },

    }
);

frappe.ui.form.on("Leave Application for Student", {
    from_date: function(frm) {
        // set To Date equal to From Date, if it's still empty
        // if (!frm.doc.to_date) {
        //     frm.set_value("to_date", frm.doc.from_date);
        // }

        // set minimum To Date equal to From Date
        frm.fields_dict.to_date.datepicker.update({
            minDate: frm.doc.from_date ? new Date(frm.doc.from_date) : null
        });
    },

    to_date: function(frm) {
        // set maximum From Date equal to To Date
        frm.fields_dict.from_date.datepicker.update({
            maxDate: frm.doc.to_date ? new Date(frm.doc.to_date) : null
        });
    },
});

