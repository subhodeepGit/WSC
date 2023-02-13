// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Drive Calendar', {
	// refresh: function(frm) {
	
	// },
	placement_drive: function(frm) {
		frappe.call({
			method:'wsc.wsc.doctype.placement_tool.placement_tool.get_rounds_of_placement',
			args:{
				drive_name: frm.doc.placement_drive
			},
			callback: function(result){
				let arr = [];
				for(let x in result.message){
					arr.push(result.message[x]);
				}
				// alert(arr)
				frm.set_df_property('round_of_placement', 'options', arr)
				
			}
		})
	},
	round_of_placement: function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.placement_tool.placement_tool.get_date_of_round',
			args:{
				doc:frm.doc,
				drive_name: frm.doc.placement_drive,
				round_name: frm.doc.round_of_placement
			},
			callback: function(result){
					// alert(result.message)
					console.log(result.message[0][0]);
					// frm.set_value("scheduled_date_of_round", result.message[0]);
					frm.set_value("reporting_date", result.message[0][0]);
					frm.set_value("reporting_time", result.message[0][1]);
			}
		})
	}

})
// wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_rounds