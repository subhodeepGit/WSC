// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Internship Application', {
	refresh: function(frm) {
		frm.set_query("select_internship", function() {
			return {
				query: 'wsc.wsc.doctype.internship_application.internship_application.get_select_internship',
				filters: {
					"today_date":frappe.datetime.get_today(),
					"enable":1
				}
			};
		});
		frm.set_query("select_internship", function() {
			return {
				query: 'wsc.wsc.doctype.internship_application.internship_application.drive_filter',
				filters:{
					"participant_id":frm.doc.participant_id,
				}
				
			};
		});
	},
	select_internship : function(frm){
		if(participant_id){
			if(frm.doc.select_internship){
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
		}
		else{
			frm.set_value('internship_name', '')
		}
		
	},
	participant_id : function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.internship_application.internship_application.get_participant_name',
			args: {
				participant_type : frm.doc.participant_type,
				participant_id : frm.doc.participant_id
			},
			callback: function(result){
				frm.set_value("participant_name", result.message)
			}
		})
	}
});
