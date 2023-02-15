// frappe.views.calendar["Placement Drive Calendar"] = {
// 	field_map: {
// 		"start": "reporting_date",
// 		"end": "reporting_time",
// 		"id": "name",
// 		"title": "placement_drive",
// 		"allDay": "allDay",
//         // "date": "reporting_date",
//         // "time": "reporting_time",
//         // "round_of_placement": "round_of_placement",
//         "company_name": "company_name",
// 	},
// 	// gantt: false,
// 	order_by: "scheduled_date_of_round",
// 	filters: [
// 		{
// 			"fieldtype": "Link",
// 			"fieldname": "placement_company",
// 			"options": "Placement Company",
// 			"label": __("Placement company")
// 		},
// 		{
// 			"fieldtype": "Link",
// 			"fieldname": "placement_drive",
// 			"options": "Placement Drive",
// 			"label": __("Placement Drive")
// 		},
// 		{
// 			"fieldtype": "Select",
// 			"fieldname": "round_of_placement",
// 			"options": "Instructor",
// 			"label": __("Round of Placement")
// 		}
// 	// 	{
// 	// 		"fieldtype": "Link",
// 	// 		"fieldname": "room",
// 	// 		"options": "Room",
// 	// 		"label": __("Room")
// 	// 	}
// 	],
// 	get_events_method: "education.education.api.get_course_schedule_events"
// 	// "wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_round_placement_event"
// }
