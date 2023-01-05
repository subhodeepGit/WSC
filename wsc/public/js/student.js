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