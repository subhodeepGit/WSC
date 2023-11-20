// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Renewal Form', {
	new_contract_start_date(frm) {
        frm.fields_dict.new_contract_end_date.datepicker.update({
            minDate: frm.doc.new_contract_start_date ? new Date(frm.doc.new_contract_start_date) : null
        });
    },

    new_contract_end_date(frm) {
        frm.fields_dict.new_contract_start_date.datepicker.update({
            maxDate: frm.doc.new_contract_end_date ? new Date(frm.doc.new_contract_end_date) : null
        });
    },
	refresh: function(frm) {
		frm.set_query("employee", function () {
			return {
				filters:{
					"Status":"Active",
				}
			};
		})
	},
	onload: function(frm) {
        // Check if the form is new
        if (!frm.doc.__islocal) {
            // Form is not new, check status
            if (frm.doc.status !== 'Pending' && frm.doc.status !== 'Pending Approval From HR') {
                // Call Python function
                frappe.call({
                    method: 'wsc.wsc.doctype.employee_renewal_form.employee_renewal_form.get_appraisal_details',
                    args: {
                        "employee": frm.doc.employee,
                        "date": frm.doc.date
                    },
                    callback: function(response) {
                        // Handle the callback response as needed
                        // For example, display a message or perform other actions
                        if (response.message) {
                            // Set values in the form fields
                            frm.set_value('appraisal_document', response.message.doc_name);
                            frm.set_value('grade', response.message.final_grade);

                            // Clear existing child table rows
                            frm.clear_table('key_work_goals');

                            // Add rows to the child table
							// alert(response.message.goal_documents)
                            for (var i = 0; i < response.message.goal_documents.length; i++) {
                                var row = frappe.model.add_child(frm.doc, 'Key Work Goals', 'key_work_goals');
                                // Set values for each row in the child table
								// alert(response.message.goal_documents[i])
                                row.goal = response.message.goal_documents[i].goal;
                                row.category = response.message.goal_documents[i].category;
								row.due_date = response.message.goal_documents[i].due_date;
								row.employee_comment = response.message.goal_documents[i].employee_comment;
								row.status = response.message.goal_documents[i].status;
								row.ros_comment = response.message.goal_documents[i].ros_comment;
								row.upload_document=response.message.goal_documents[i].upload_document
                                // Add more fields as needed
                            }

                            // Refresh the form to update the UI
                            frm.refresh();
                        }
                    }
                });
            }
        }
    }
});
