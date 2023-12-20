from __future__ import unicode_literals
from frappe import _


def get_data(data):
	return {
		"fieldname": "item",
		"transactions": [
			{
				"label": _("Purchase"),
				"items": ["Purchase Order","Purchase Invoice","Purchase Receipt"]
	        },
			{
				"label": _("References"),
				"items": ["Supplier Quotation"]
	        },
		]
	}