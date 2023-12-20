from __future__ import unicode_literals
from frappe import _


def get_data(data):
	return {
		"fieldname": "supplier",
		"transactions": [
			{
				"label": _("Payment"),
				"items": ["Payment Entry","Journal Entry"]
	        },
			{
			    "label": _("References"),
				"items": ["Purchase Order","Purchase Receipt"]
	        },
        ]
	}
