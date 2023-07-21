from frappe import _


def get_data(data):
	return {
		"fieldname": "student_group",
		"transactions": [
			{"label": _("Course"), "items": ["Course Schedule"]},
		],
	}
