frappe.views.calendar["ToT Class Schedule"] = {
	field_map: {
		"start": "from_time",
		"end": "to_time",
		"id": "name",
		"title": "course",
		"allDay": "allDay",
	},
	gantt: false,
	order_by: "scheduled_date",
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "participant_group_id",
			"options": "Participant Group ID",
			"label": __("Participant Group ID")
		},
		{
			"fieldtype": "Link",
			"fieldname": "course_id",
			"options": "Course",
			"label": __("Course")
		},
		{
			"fieldtype": "Link",
			"fieldname": "trainers",
			"options": "Trainers",
			"label": __("Trainers")
		},
		{
			"fieldtype": "Link",
			"fieldname": "room_number",
			"options": "Room Number",
			"label": __("Room Number")
		}
	],
	get_events_method: "wsc.wsc.doctype.tot_class_schedule.tot_class_schedule.get_class_schedule_calendar" 
}
