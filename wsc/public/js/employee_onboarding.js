frappe.ui.form.on('Employee Onboarding', {
    refresh: function(frm) {
        if(frm.doc.boarding_status==="Completed"){
            // alert("Hello Boy")
            // alert(!frm.doc.mail_sent)
            if(frm.doc.mail_sent!=1){
                frappe.call({
                    // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                    method: 'wsc.wsc.doctype.employee_onboarding.hr_mail_after_complete',
                    args: {
                        docname: frm.doc.name
                    },
                    callback :function(r){
                        frm.set_value("mail_sent",1)
                        frm.save("Submit",function(){
                            // frape.msgprint("Final Mail Sent to HR");
                        })
                    }
                });

            }
        }
    }

            
                
                
});
