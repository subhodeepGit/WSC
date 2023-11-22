
frappe.ui.form.on('Job Offer', {
    job_applicant_id:function(frm){    
        let fname=frm.doc.job_applicant_id;     
        frm.set_value("job_applicant",fname);    
    },   
    employee_name:function(frm){    
        let fname=frm.doc.employee_name;     
        frm.set_value("name_for",fname);    
    },     
    applicant_name:function(frm){    
        let fname=frm.doc.applicant_name;     
        frm.set_value("name_for",fname);    
    }, 
    refresh: function(frm) {
        if (frm.doc.is_reengagement === 1) {
            frm.remove_custom_button('Create Employee');
        }
    },
    setup:function(frm){
		// frm.remove_custom_button("Add to Programs","Action");
		frm.set_query("job_applicant_id", function() {
			return {
				filters: {
					"job_title":frm.doc.job_opening,
                    "application_year":frm.doc.year,
                    "current_status":"Selected"
				}
			};
		});
	},


});

