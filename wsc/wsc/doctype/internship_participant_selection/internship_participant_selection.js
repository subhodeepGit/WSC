// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// internship_participant_selection

frappe.ui.form.on('Internship Participant Selection', {
	refresh: function(frm) {
		frm.set_df_property('select_participants_table', 'cannot_add_rows', true)
		frm.set_df_property('select_participants_table', 'cannot_delete_rows', true)
	},
	select_internship : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.internship_participant_selection.internship_participant_selection.get_internship_name',
			args: {
				internship_id : frm.doc.select_internship
			},
			callback : function(result){
				frm.set_value('internship_name', result.message)
			}
		})
	},
	get_participants : function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.internship_participant_selection.internship_participant_selection.get_applied_participants',
			args : {
				internship_id : frm.doc.select_internship
			},
			callback : function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'select_participants_table')
					result.message.forEach(element =>{
						var childTable = frm.add_child('select_participants_table')
						childTable.applicant_id = element.participant_id
						childTable.applicant_name = element.participant_name
						childTable.applicant_type = element.participant_type
					})
				}
				frm.refresh()
				frm.refresh_field('select_participants_table')
			}
		})
	}
});
