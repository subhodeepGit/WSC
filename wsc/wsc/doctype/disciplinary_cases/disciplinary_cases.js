// Copyright (c) 2023, SOUL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Disciplinary cases', {
	refresh: function(frm) {
		if (frm.doc.docstatus==0 || frappe.session.user==frm.doc.employee_email || frappe.session.user==frm.doc.email || frm.doc.complaint_status=="Resolved" || frm.doc.complaint_status=="Action Taken"){
			frm.set_df_property('complaint_status', 'read_only', 1)
		}
		else{
			frm.set_df_property('complaint_status', 'read_only', 0)
		}
		if(frm.doc.action=="First Warning" || frm.doc.action=="Second Warning" || frm.doc.action=="Termination"){
			frm.set_df_property('discipline_committee', 'read_only', 1)
			frm.set_df_property('action', 'read_only', 1)
			frm.set_df_property('action_description', 'read_only', 1)
		}
		else{
			frm.set_df_property('discipline_committee', 'read_only', 0)
			frm.set_df_property('action', 'read_only', 0)
			frm.set_df_property('action_description', 'read_only', 0)
		}
		if(frm.doc.docstatus==1){
			frm.set_df_property('complaint_status', 'reqd', 1)
		}
		else{
			frm.set_df_property('complaint_status', 'reqd', 0)
		}
	}
});
