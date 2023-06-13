// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// internship_final_list_declaration

frappe.ui.form.on('Internship Final List Declaration', {
	refresh: function(frm) {

	},
	select_internship : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.internship_final_list_declaration.internship_final_list_declaration.get_internship_name',
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
			method: 'wsc.wsc.doctype.internship_final_list_declaration.internship_final_list_declaration.get_selected_participants',
			args : {
				internship_id : frm.doc.select_internship
			},
			callback : function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'selected_participants_list')
					result.message.forEach(element =>{
						var childTable = frm.add_child('selected_participants_list')
						childTable.participant_id = element.applicant_id
						childTable.participant_name = element.applicant_name
					})
				}
				frm.refresh()
				frm.refresh_field('selected_participants_list')
			}
		})
	}
});
