// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
frappe.views.calendar["Placement Drive Calendar"] = {
	field_map: {
		"start": "reporting_date",
		"end": "reporting_time",
		"id": "name",
		// "title": "placement_drive",
		// "allDay": "allDay",
        // "date": "reporting_date",
        // "time": "reporting_time",
        // "round_of_placement": "round_of_placement",
        "company_name": "company_name",
	},
	gantt: false,
	order_by: "scheduled_date_of_round",
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "placement_company",
			"options": "Placement Company",
			"label": __("Placement company")
		},
		{
			"fieldtype": "Link",
			"fieldname": "placement_drive",
			"options": "Placement Drive",
			"label": __("Placement Drive")
		},
		{
			"fieldtype": "Select",
			"fieldname": "round_of_placement",
			"options": "Instructor",
			"label": __("Round of Placement")
		}
	// 	{
	// 		"fieldtype": "Link",
	// 		"fieldname": "room",
	// 		"options": "Room",
	// 		"label": __("Room")
	// 	}
	],
	get_events_method: "wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_round_placement_event"
}
frappe.ui.form.on('Placement Drive Calendar', {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Show Calendar"), () =>
				frappe.set_route("List", "Placement Drive Calendar", "Calendar", frm.doc.placement_company)
			);
		}
	},
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
					// console.log(result.message[0][0]);
					// frm.set_value("scheduled_date_of_round", result.message[0]);
					frm.set_value("reporting_date", result.message[0][0]);
					frm.set_value("reporting_time", result.message[0][1]);
			}
		})
	}

})
// wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_rounds