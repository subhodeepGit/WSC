// Copyright (c) 2022, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Students Grievance', {
	refresh: function(frm) {
		if(frm.doc.docstatus===1 && frm.doc.status=="Issue Posted By the Student") {
			frm.add_custom_button(__("Register Complaint"), function() {
				frm.events.register_complaint(frm);
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
	},
	register_complaint: function(frm) {
		return frappe.call({
			method: "wsc.wsc.doctype.students_grievance.students_grievance.get_register_complaint",
			args: {
				"dt": frm.doc.doctype,
				"dn": frm.doc.name,
			},
			callback: function(r) {
				var doc = frappe.model.sync(r.message);
				frappe.set_route("Form", doc[0].doctype, doc[0].name);
			}
		});
	},

});
