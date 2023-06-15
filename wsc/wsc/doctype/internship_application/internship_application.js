// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Internship Application', {
	refresh: function(frm) {

	},
	participant_id : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.internship_application.internship_application.get_participant_name',
			args: {
				participant_id : frm.doc.participant_id
			},
			callback : function(result){
				frm.set_value('participant_name', result.message)
			}
		})
	},
	select_internship : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.internship_application.internship_application.get_internship_name',
			args: {
				internship_id : frm.doc.select_internship
			},
			callback : function(result){
				frm.set_value('internship_name', result.message)
			}
		})
	}
});
