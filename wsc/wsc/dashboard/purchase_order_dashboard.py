from __future__ import unicode_literals
from frappe import _


def get_data(data):
	return {
		"fieldname": "supplier",
		"transactions": [
			{
				"label": _("References"),
				"items": ["Material Request","Supplier Quotation","Project"]
	        },
			{
				"label": _("Related"),
				"items": ["Purchase Receipt","Purchase Invoice","Stock Entry"]
	        },
			{
				"label": _("Payment"),
				"items": ["Payment Entry","Journal Entry"]
	        }
        ]
	}
