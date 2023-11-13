frappe.ui.form.on('Student',{
    refresh: function(frm) {
        frm.add_custom_button(__('Tnp Round Selection Report'), function() {
            frappe.route_options = {
                student_id: frm.doc.name,
            };
            frappe.set_route("query-report", "Selection Round Report");
        })
        frm.set_df_property('document_list', 'cannot_delete_rows', true);
        if (!frm.doc.__islocal){
            frm.add_custom_button("Enroll", () => {
                let data = {}
                data.student = frm.doc.name
                data.student_name = frm.doc.student_name
                data.roll_no = frm.doc.roll_no
                data.permanant_registration_number = frm.doc.permanant_registration_number
                frappe.new_doc("Program Enrollment", data)
            });    
        }  
        if ((frappe.user.has_role("Student")|| frappe.user.has_role("Instructor")) && !frappe.user.has_role("System Manager")){
            frm.remove_custom_button("Accounting Ledger");
            frm.remove_custom_button("Enroll");
            $(".menu-btn-group").hide();
        }  
        frm.set_query("block", function() {
            return {
                filters: {
                    "districts":frm.doc.district
                }
            }; 
        });

        frm.set_query("district", function() {
            return {
                filters: {
                    "state":frm.doc.stat
                }
            };
        });
    }    
})

// Pop-up message Room Allotment Data in Student doctype in js

frappe.ui.form.on('Student', {
    onload: function(frm) {
           frappe.call({            
               "method": "wsc.wsc.doctype.room_allotment.room_allotment.get",
               args: {
                   name: frm.doc.name
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
    }
    })
    frappe.ui.form.on("Educational Details", "total_marks", function(frm, cdt, cdn) {
       
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
        cur_frm.refresh_field ("education_details");
     });
    frappe.ui.form.on("Educational Details", "earned_marks", function(frm, cdt, cdn) {
           
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
        cur_frm.refresh_field ("education_details");
     });	
     frappe.ui.form.on("Education Qualifications Details", "cgpa", function(frm, cdt, cdn) {
      
        var data = locals[cdt][cdn];
        if(data.cgpa<=10 && data.cgpa>=0){
            data.score=data.cgpa*10   
        }
        else if(data.cgpa>10 || data.cgpa<0){
            data.score=""
            data.
            frappe.throw("Please enter your valid CGPA")
        }
        else{
            frappe.throw("Wrong Entry")
        }
        
        
        cur_frm.refresh_field ("education_details");
     });     
 

frappe.ui.form.on('Experience child table', {
    'job_end_date':function(frm,cdt,cdn){
        console.log(2)
        var d=locals[cdt][cdn];
        if(d.job_start_date && d.job_end_date){
            let joining_date = new Date(d.job_start_date)
            let resigning_date = new Date(d.job_end_date)
            const diffTime = Math.abs(joining_date - resigning_date);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            const diffyears = (diffDays/365).toFixed(1)
            d.job_duration=diffyears            
            refresh_field('d.job_duration',d.name,d.parentfield)
            console.log(d.job_duration)
        }
    }
})