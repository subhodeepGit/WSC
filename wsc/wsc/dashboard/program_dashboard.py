from frappe import _


def get_data(data):
	return {
		"fieldname": "program",
		"transactions": [
			{
				"label": _("Enrollment"),
				"items": ["Program Enrollment"],
			},
			{"label": _("Student Activity"), "items": ["Student Group"]},
			# {"label": _("Fee"), "items": ["Fees"]},
		],
	}
