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
frappe.ui.form.on('Job Applicant', {
	refresh(frm){
		if(frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){
			frm.set_value("email_id", frappe.session.user)
			frm.set_df_property('email_id', 'read_only', 1);
		}
		frm.set_value("current_status", "CV Selected");
		if (frm.doc.docstatus===1) {
			frm.add_custom_button(__("CV Selected"), function() {
				frm.set_value("current_status", "CV Selected");
				frm.save_or_update();
				frappe.msgprint("Please Click on the Confirm button")
			}, 'Actions');

			frm.add_custom_button(__("Qualified"), function() {
				frm.set_value("current_status", "Qualified");
				frm.save_or_update();
				frappe.msgprint("Please Click on the Confirm button")
			}, 'Actions');
			frm.add_custom_button(__("Disqualified"), function() {
				frm.set_value("current_status", "Disqualified");
				frm.save_or_update();
				frappe.msgprint("Please Click on the Confirm button")
			}, 'Actions');

			frm.add_custom_button(__("Selected"), function() {
				frm.set_value("current_status", "Selected");
				frm.save_or_update();
				frappe.msgprint("Please Click on the Confirm button")
			}, 'Actions');
			frm.add_custom_button(__("On Hold"), function() {
				frm.set_value("current_status", "On Hold");
				frm.save_or_update();
				frappe.msgprint("Please Click on the Confirm button")
			}, 'Actions');

			frm.add_custom_button(__("Waiting"), function() {
				frm.set_value("current_status", "Waiting");
				frm.save_or_update();
				frappe.msgprint("Please Click on the Confirm button")
			}, 'Actions');
		}
		if(frm.doc.docstatus===1){
		frm.add_custom_button(__("Confirm"), function() {
			frm.set_value("current_status", frm.doc.current_status);
			frm.save_or_update();

		});
	}
	
		if (!cur_frm.doc.__islocal && frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){
			frm.remove_custom_button("Waiting","Actions");
			frm.remove_custom_button("Selected","Actions");
			frm.remove_custom_button("Confirm");
			frm.remove_custom_button("Interview","Create");
			frm.remove_custom_button("On Hold","Actions");
			frm.remove_custom_button("Disqualified","Actions");
			frm.remove_custom_button("Qualified","Actions");
			frm.remove_custom_button("CV Selected","Actions");
		}
	}
		
})
