// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Internship Completion status', {
	refresh: function(frm) {
		frm.set_query("select_participant", function() {
			return {
				query: 'wsc.wsc.doctype.internship_completion_status.internship_completion_status.participants',
				filters:{
					"internship_id":frm.doc.select_internship,
				}
				
			};
		});
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
	},
	
});
