
//Fetching Employee Education Qualification Details and External Work History on the basis of Job Applicant
frappe.ui.form.on("Employee", "job_applicant", function (frm) {
	if (frm.doc.job_applicant == undefined || frm.doc.job_applicant == "" || frm.doc.job_applicant == null){

	}else{
	frappe.model.with_doc("Job Applicant", frm.doc.job_applicant, function () {
		frm.clear_table("education");
        frm.clear_table("external_work_history")
		var tabletransfer = frappe.model.get_doc("Job Applicant", frm.doc.job_applicant);
		cur_frm.doc.educational_details = "";
        cur_frm.doc.work_history = "";
		cur_frm.refresh_field("educational_details");
        cur_frm.refresh_field("work_history");
		$.each(tabletransfer.educational_details, function (index, row) {
			var d = frappe.model.add_child(cur_frm.doc, "Employee Education", "education");
			d.school_univ = row.school_univ;
            d.qualification_1 = row.qualification_1;
            d.level_1 = row.level_1;
            d.year_of_passing = row.year_of_passing;
            d.class_per = row.class_per;
            d.maj_opt_subj = row.maj_opt_subj;
            d.marksheetcertificate = row.marksheetcertificate;
			cur_frm.refresh_field("education");
		});
        $.each(tabletransfer.work_history, function (index, row) {
			var d = frappe.model.add_child(cur_frm.doc, "Employee External Work History", "external_work_history");
			d.company_name = row.company_name;
            d.designation = row.designation;
            d.salary = row.salary;
            d.address = row.address;
            d.contact = row.contact;
            d.total_experience = row.total_experience;
            d.document = row.document;
			d.from_date= row.from_date;
			d.to_date= row.to_date;
			cur_frm.refresh_field("external_work_history");
		});
	});
}


});
frappe.ui.form.on("Employee External Work History" , "to_date" , function(frm , cdt , cdn){
    var d = locals[cdt][cdn];
	if (d.from_date && d.to_date) {
        if (d.from_date > d.to_date) {
            frappe.msgprint(__("From Date should be less than To Date."));
            frappe.model.set_value(cdt, cdn, "to_date", ""); 
        }
    }
      
    });


frappe.ui.form.on('Dynamnic Workflow for Goal Setting', {
	goal_settings_workflow_add: function(frm){
		frm.fields_dict['goal_settings_workflow'].grid.get_field('employee').get_query = function(doc){
			var employee_list = [];
			if(!doc.__islocal) ;
			$.each(doc.goal_settings_workflow, function(idx, val){
				if (val.employee) employee_list.push(val.employee);
			});
			return { filters: [['Employee', 'name', 'not in', employee_list]] };
		};
	}
})