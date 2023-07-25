// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Participant', {
	refresh: function(frm){
		frm.set_df_property('previous_participations', 'cannot_add_rows', true)
		frm.set_df_property('previous_participations', 'cannot_delete_rows', true)
	},
	// developers notes
	
	// the data for the previous participation selection will be filled from the ToT Participant reporting screen as that marks the participant as physically 
	// present for the program and at that point the participant should be considered to have participated in the program
	// hence the user cannot enter or delete records for the previous_participations table from this screen.
	
});
