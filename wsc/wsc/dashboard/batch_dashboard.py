from __future__ import unicode_literals
from frappe import _


def get_data(data):
	return {
		"fieldname": "supplier",
		"transactions": [
			{
				"label": _("Move"),
				"items": ["Stock Entry"]
	        },
			{
			    "label": _("Buy"),
				"items": ["Purchase Invoice","Purchase Receipt"]
	        },
        ]
	}
