
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
            d.qualification = row.qualification;
            d.level = row.level;
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
			cur_frm.refresh_field("external_work_history");
		});
	});
}


});

