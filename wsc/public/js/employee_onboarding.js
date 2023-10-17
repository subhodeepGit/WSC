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
                            frappe.show_alert("Final Mail Sent to HR", 5);

                        });
                    }

                });

            }
        }
    },
    employee_onboarding_template: function(frm) {
		frm.set_value("activities" ,"");
		if (frm.doc.employee_onboarding_template) {
			frappe.call({
				method: "wsc.wsc.doctype.employee_onboarding.get_onboarding_details",
				args: {
					"parent": frm.doc.employee_onboarding_template,
                    "parenttype": "Employee Onboarding Template"
				},
				callback: function(r) {
					if (r.message) {
						$.each(r.message, function(i, d) {
							var row = frappe.model.add_child(frm.doc, "Employee Boarding Activity", "activities");
							$.extend(row, d);
						});
					}
					refresh_field("activities");
				}
			});
		}
	}

            
                
                
});
