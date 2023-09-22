// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Appraisal Portal', {
	refresh: function(frm) {

	},
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
	appraisal_template: function(frm) {
        frappe.call({
            method: 'wsc.wsc.doctype.employee_appraisal_portal.employee_appraisal_portal.get_goals',
            args :{
                "appraisal_template":frm.doc.appraisal_template
            },


           callback: function(r) {
                if(r.message){
                    frappe.model.clear_table(frm.doc, 'goals');
                    (r.message).forEach(element => {
                        var c = frm.add_child("goals")
                        c.goal=element.goal
                        c.category=element.category
                        c.due_date=element.due_date
                        c.status=element.status
                        // c.goal.$input.prop('readonly', true);
                        // c.category.$input.prop('readonly', true);
                        // c.due_date.$input.prop('readonly', true);
                    });
                }
                frm.refresh();
                frm.refresh_field("goals")
            }
        })
			
	},
	appraisal_cycle : function(frm){
		// Get the value of the "Appraisal Round" field
        var appraisalRound = frm.doc.appraisal_round;

        // Get the field object for "Competency Rating"
        var competencyRatingField = frm.doc.self_rating; // Replace "fieldname" with the actual fieldname

        // Check the value of "Appraisal Round" and show/hide the "Competency Rating" field accordingly
        if (appraisalRound === '2') {
            frm.toggle_display("self_rating", true);
			frm.toggle_display("mid_year_grade",true);
            frm.toggle_display("self_review",true);
			frappe.call({
				method: 'wsc.wsc.doctype.employee_appraisal_portal.employee_appraisal_portal.get_dimenssions',
				// args :{
				// 	"appraisal_template":frm.doc.appraisal_template
				// },
	
	
			   callback: function(r) {
					if(r.message){
						frappe.model.clear_table(frm.doc, 'self_rating');
						(r.message).forEach(element => {
							var c = frm.add_child("self_rating")
							c.dimenssion=element.name
							c.description=element.description
							// c.due_date=element.due_date
							// c.status=element.status
						});
					}
					frm.refresh();
					frm.refresh_field("self_rating")
				},
			
			});

			frappe.call({
                method: 'wsc.wsc.doctype.employee_appraisal_portal.employee_appraisal_portal.get_mid_year_grade',
                args: {
                    employee: frm.doc.employee,
					appraisal_year:frm.doc.appraisal_year // Pass necessary arguments as needed
                },
                callback: function(response) {
                    if (response.message) {
						// alert(response.message["final_grade"])
						frm.set_value("mid_year_grade",response.message["final_grade"])
                    }
                }
            });

        } else {
			// alert(typeof appraisalRound)
            frm.toggle_display("self_rating", false);
			frm.toggle_display("mid_year_grade",false);
            frm.toggle_display("self_review",false)
        }

    },
	
});
