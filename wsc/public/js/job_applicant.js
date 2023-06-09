//Updating Round in Job Applicant in child table Result Status
frappe.ui.form.on("Job Applicant", "job_title", function (frm) {
	if (frm.doc.job_title == undefined || frm.doc.job_title == "" || frm.doc.job_title == null){

	}else{
	frappe.model.with_doc("Job Opening", frm.doc.job_title, function () {
		frm.clear_table("result_status");
		var tabletransfer = frappe.model.get_doc("Job Opening", frm.doc.job_title);
		cur_frm.doc.job_selection_round = "";
		cur_frm.refresh_field("job_selection_round");
		$.each(tabletransfer.job_selection_round, function (index, row) {
			var d = frappe.model.add_child(cur_frm.doc, "Result Status", "result_status");
			d.name_of_the_round = row.name_of_rounds;
			cur_frm.refresh_field("result_status");
		});
	});
}
});
//Adding Data in Previous Application Details Table
frappe.ui.form.on("Job Applicant", "aadhar_card_number", function (frm) {
	frappe.call({
		method: 'wsc.wsc.doctype.job_applicant.previous_applied',
		args: {
			aadhar_number: frm.doc.aadhar_card_number
		},
		callback: function(r) {
			if(r.message){
				frappe.model.clear_table(frm.doc, 'previous_application_details');
				(r.message).forEach(element => {
					var c = frm.add_child("previous_application_details")
					c.job_applicant=element.name
					c.job_opening=element.job_title
				});
			}
			frm.refresh_field("previous_application_details")
		}
	});
});


