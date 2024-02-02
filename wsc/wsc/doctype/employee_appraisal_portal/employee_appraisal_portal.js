// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Appraisal Portal', {
	// onload: function(frm) {
    //     // alert(frm.doc.approval_status)
    //     if (frm.doc.approval_status === 'Approved') {
    //         // Make the field with the fieldname 'your_fieldname' read-only
    //         frm.toggle_enable('final_grade', false);
    //     }
	// },
	setup:function(frm){

        frm.set_query("appraisal_cycle", function() {
			
            return {
                query:"wsc.wsc.doctype.employee_appraisal_portal.employee_appraisal_portal.get_appraisal_cycle",
                filters: {
                    "appraisal_year":frm.doc.appraisal_year
                }
				
            };
        });
        
    },
	appraisal_year: function(frm) {
        frappe.model.clear_table(frm.doc, 'key_work_goals');
    
        frappe.call({
            method: 'wsc.wsc.doctype.employee_appraisal_portal.employee_appraisal_portal.get_goals',
            args: {
                "employee": frm.doc.employee,
                "appraisal_year": frm.doc.appraisal_year
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.clear_table(frm.doc, 'key_work_goals');
                    r.message.forEach(element => {
                        var c = frm.add_child("key_work_goals");
                        c.goal = element.goal;
                        c.category = element.category;
                        c.due_date = element.due_date;
                    });
                }
                frm.refresh();
                frm.refresh_field("key_work_goals");
            }
        });
    
        frappe.call({
            method: 'wsc.wsc.doctype.employee_appraisal_portal.employee_appraisal_portal.get_mid_year_grade',
            args: {
                employee: frm.doc.employee,
                appraisal_year: frm.doc.appraisal_year
            },
            callback: function(response) {
                if (response.message) {
                    frm.set_value("mid_year_grade", response.message["final_grade"]);
                }
            }
        });
    },
    
    
	appraisal_round : function(frm){
		// Get the value of the "Appraisal Round" field
        var appraisalRound = frm.doc.appraisal_round;

        // Get the field object for "Competency Rating"
        var competencyRatingField = frm.doc.self_rating; // Replace "fieldname" with the actual fieldname

        // Check the value of "Appraisal Round" and show/hide the "Competency Rating" field accordingly
        // alert(frm.doc.status)
        if (frm.doc.status != "Approved" && frm.doc.status != "Rejected"){
            if (appraisalRound === 'End Year') {
                // frm.toggle_display("self_rating", true);
                frm.toggle_display("mid_year_grade",true);
                // frm.toggle_display("self_review",true);
                // frappe.call({
                //     method: 'wsc.wsc.doctype.employee_appraisal_portal.employee_appraisal_portal.get_dimenssions',
                //     // args :{
                //     // 	"appraisal_template":frm.doc.appraisal_template
                //     // },
        
        
                //    callback: function(r) {
                //         if(r.message){
                //             frappe.model.clear_table(frm.doc, 'self_rating');
                //             (r.message).forEach(element => {
                //                 var c = frm.add_child("self_rating")
                //                 c.dimenssion=element.name
                //                 c.description=element.description
                //                 // c.due_date=element.due_date
                //                 // c.status=element.status
                //             });
                //         }
                //         frm.refresh();
                //         frm.refresh_field("self_rating")
                //     },
                
                // });
    
                
    
            } else {
                // alert(typeof appraisalRound)
                // frm.toggle_display("self_rating", false);
                frm.toggle_display("mid_year_grade",false);
                // frm.toggle_display("self_review",false)
            }
        }
        

        

    },
	
});
