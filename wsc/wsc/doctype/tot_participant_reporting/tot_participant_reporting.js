// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Participant Reporting', {
	refresh: function(frm) {
			frm.set_query('course_name', function(){
				return{
					filters:{
						'is_tot' : 1
					}
				}
			})
	},	
	participant_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.tot_participant_reporting.tot_participant_reporting.get_participant_details',
			args: {
				participant_id : frm.doc.participant_id
			},
			callback : function(result){
				frm.set_value("participant_name", result.message[0])
				frm.set_value("department", result.message[1])
				frm.set_value("designation", result.message[2])
				frm.set_value("name_of_institute", result.message[3])
			}
		})
	},
});