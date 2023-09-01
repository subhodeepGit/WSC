
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
    }
});

