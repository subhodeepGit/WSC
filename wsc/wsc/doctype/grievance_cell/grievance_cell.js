// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grievance Cell', {
	show_grievance_workflow: function(frm){
		if (frm.doc.type_of_grievance) {
			frappe.call({
				method: "wsc.wsc.doctype.grievance_cell.grievance_cell.get_workflow_components",
				args: {
					"type_of_grievance": frm.doc.type_of_grievance
				},
				callback: function(r) {
					if(r.message){
						frappe.model.clear_table(frm.doc, 'workflow_of_grievance');
						frappe.model.clear_table(frm.doc,"grievance_status");
						(r.message).forEach(element => {
							var c = frm.add_child("workflow_of_grievance")
							var d = frm.add_child("grievance_status")
							c.emp_no=element.emp_no
							c.emp_name=element.emp_name
							c.department=element.department
							c.designation=element.designation
							c.email_id=element.email_id
							d.emp_no=element.emp_no
							d.emp_name = element.emp_name
						});
					}
					frm.refresh();
					frm.refresh_field("workflow_of_grievance")
					frm.refresh_field("grievance_status")
				}
			});
	
		}
	},

});