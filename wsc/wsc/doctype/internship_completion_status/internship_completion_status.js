// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Internship Completion status', {
	refresh: function(frm) {
		frm.set_query("select_participant", function() {
			return {
				query: 'wsc.wsc.doctype.internship_completion_status.internship_completion_status.participants',
				filters:{
					"internship_id":frm.doc.select_internship,
					"participant_type":frm.doc.participant_type
				}
				
			};
		});
	},
	select_internship : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.internship_completion_status.internship_completion_status.get_internship_name',
			args: {
				internship_id : frm.doc.select_internship
			},
			callback : function(result){
				frm.set_value('internship_name', result.message)
			}
		})
	},
	select_participant: function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.internship_completion_status.internship_completion_status.get_participant_name',
			args: {
				participant_type : frm.doc.participant_type,
				participant_id : frm.doc.select_participant
			},
			callback : function(result){
				frm.set_value('participant_name', result.message)
			}
		})
	}
});
