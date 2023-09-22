frappe.ui.form.on('Employee Separation', {
    refresh: function(frm) {
        // if(!frm.is_new()){
        //     frappe.call({
        //         method:'wsc.wsc.validations.employee_separation.is_verified_user',
        //         args: {
        //             docname: frm.doc.name
        //         },
        //         callback: function(r) {
        //             if (r.message===false) {
        //                 $('.actions-btn-group').prop('hidden', true);
        //             }
        //         }
        //     });
        // }
        if(frm.doc.boarding_status==="Completed"){
            // alert("Hello Boy")
            // alert(!frm.doc.mail_sent)
            if(frm.doc.mail_sent!=1){
                frappe.call({
                    // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                    method: 'wsc.wsc.validations.employee_separation.mail_after_complete',
                    args: {
                        docname: frm.doc.name
                    },
                    callback :function(r){
                        frm.set_value("mail_sent",1)
                        frm.save("Submit",function(){
                        })
                        frappe.msgprint("Final Mail Sent to HR");


                    },
                    
                });
                // frappe.call({
                //     method: 'wsc.wsc.validations.employee_separation.update_employee_status',
                //     args: {
                //         employee: frm.doc.employee
                //     },
                //     callback: function (r) {
                //         if (!r.exc) {
                //             frappe.msgprint(__('Employee status updated to "Left".'));
                //         }
                //     }
                // });

            }

        }
    },

    department: function(frm){
        frappe.call({
        method: 'wsc.wsc.validations.employee_separation.depart_head',
     args:{
        department: frm.doc.department
             },
        callback: function(result){
            if (result.message) {
                var dept_head = result.message;
                frm.set_value('department_head',dept_head)
          }
        
      },
   
      }); 
    },
    employee_separation_template: function(frm) {
		frm.set_value("activities" ,"");
		if (frm.doc.employee_separation_template) {
			frappe.call({
				method: "wsc.wsc.validations.employee_separation.get_onboarding_details",
				args: {
					"parent": frm.doc.employee_separation_template,
                    "parenttype": "Employee Separation Template"
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
      

    