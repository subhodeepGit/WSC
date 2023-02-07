frappe.ui.form.on('Student',{
    refresh: function(frm) {
        if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role('System Manager')){
            frm.remove_custom_button("Accounting Ledger");
        } 
        
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
    }
);


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