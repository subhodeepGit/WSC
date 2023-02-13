frappe.views.calendar["Placement Tool"] = {
	field_map: {
		// "start": "from_time",
		// "end": "to_time",
		// "id": "name",
		// "title": "course",
		// "allDay": "allDay",
        "date": "scheduled_date_of_round",
        "time": "scheduled_time_of_round",
        "round_of_placement": "round_of_placement",
        "company_name": "company_name",
	},
	gantt: false,
	order_by: "scheduled_date_of_round",
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "student_group",
			"options": "Student Group",
			"label": __("Student Group")
		},
		{
			"fieldtype": "Link",
			"fieldname": "course",
			"options": "Course",
			"label": __("Course")
		},
		{
			"fieldtype": "Link",
			"fieldname": "instructor",
			"options": "Instructor",
			"label": __("Instructor")
		},
		{
			"fieldtype": "Link",
			"fieldname": "room",
			"options": "Room",
			"label": __("Room")
		}
	],
	get_events_method: "wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_round_placement_event"
}
