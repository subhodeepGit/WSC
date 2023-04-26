frappe.ui.form.on('Employee', {
	job_applicant: function(frm) {
        frappe.call({
            method: 'wsc.wsc.doctype.employee.get_educational_details',
            args :{
                "job_applicant":frm.doc.job_applicant
            },


           callback: function(r) {
                if(r.message){
                    frappe.model.clear_table(frm.doc, 'education');
                    (r.message).forEach(element => {
                        var c = frm.add_child("education")
                        c.level=element.level
                        c.school_univ=element.school_univ
                        c.year_of_passing=element.year_of_passing
                        c.class_per=element.class_per
                        c.document=element.document
                    });
                }
                frm.refresh();
                frm.refresh_field("questionnarie")
            }
        })
    },

});
frappe.ui.form.on('Employee', {
	setup:function(frm){
        frm.set_query("job_applicant", function() {
            return {
                query:"wsc.wsc.doctype.employee.get_job_applicant",
                
            };
        });
    },
})