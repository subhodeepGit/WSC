from frappe import _


def get_data(data):
	return {
		# "heatmap": True,
		# "heatmap_message": _("This is based on the course schedules of this Instructor"),
		# "fieldname": "instructor",
		# "non_standard_fieldnames": {"Assessment Plan": "supervisor"},
		"transactions": [
			{
				"label": _("Time Table"),
				"items": ["Course Schedule"],
			},
			{"label": _("Students"), "items": ["Student Group"]},
		],
	}
