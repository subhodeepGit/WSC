// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Participant Selection', {
	course: function(frm) {
		if (frm.doc.course){
			frappe.call({
				method: "wsc.wsc.doctype.tot_participant_selection.tot_participant_selection.get_semester",
				args: {
					course: frm.doc.course,
				},
				callback: function(r) { 
					if(r.message){
						frm.set_value('semester', r.message)
						frm.refresh_field("semester")
					}
				} 
				
			}); 
		}
	},
	academic_year: function(frm) {
		if (frm.doc.academic_year){
			frappe.call({
				method: "wsc.wsc.doctype.tot_participant_selection.tot_participant_selection.get_academic_term",
				args: {
					academic_year: frm.doc.academic_year,
				},
				callback: function(r) { 
					if(r.message){
						frm.set_value('academic_term', r.message)
						frm.refresh_field("academic_term")
					}
				} 
				
			}); 
		}
	}
});
