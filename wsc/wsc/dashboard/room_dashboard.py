from frappe import _


def get_data(data):
	return {
		"fieldname": "room",
		"transactions": [
			{"label": _("Time Table"), "items": ["Course Schedule"]},
			# {"label": _("Assessment"), "items": ["Assessment Plan"]},
		],
	}
