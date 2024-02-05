from __future__ import unicode_literals
from frappe import _


def get_data(data):
	return {
		"fieldname": "supplier",
		"transactions": [
			{
				"label": _("Maintenance"),
				"items": ["Asset Maintenance"]
	        },
			{
			    "label": _("Journal Entry"),
				"items": ["Journal Entry"]
	        },
			{
				"label": _("Repair"),
				"items": ["Asset Repair"]
	        },
        ]
	}
