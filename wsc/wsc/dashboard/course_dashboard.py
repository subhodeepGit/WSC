from frappe import _


def get_data(data):
	return {
		"fieldname": "course",
		"transactions": [
			{
				"label": _("Semester and Module"),
				"items": ["Program", "Course Enrollment", "Course Schedule"],
			},
			{"label": _("Student"), "items": ["Student Group"]},
		],
	}
