frappe.views.calendar["Placement Drive Calendar"] = {
	field_map: {
		"start": "reporting_date",
		"end": "reporting_date",
		"id": "name",
		// "reporting_date":"reporting_date",
		"title": "placement_drive",
		"allDay": "allDay",
        // "date": "reporting_date",
        // "time": "reporting_time",
        // "round_of_placement": "round_of_placement",
        // "company_name": "company_name",
	},
	gantt: false,
	order_by: "reporting_date",
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
			"fieldtype": "Date",
			"fieldname": "reporting_date",
			"label": __("Reporting Date")
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
