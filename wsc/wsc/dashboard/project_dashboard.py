from __future__ import unicode_literals
from frappe import _


def get_data(data):
	return {
		"fieldname": "supplier",
		"transactions": [
			{
				"label": _("Project"),
				"items": ["Task","Issue","Project Update"]
	        },
			{
			    "label": _("References"),
				"items": ["Material Request","Purchase Order","Purchase Receipt","Purchase Invoice"]
            }
        ]
	}
