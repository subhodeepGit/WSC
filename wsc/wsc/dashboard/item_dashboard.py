from __future__ import unicode_literals
from frappe import _


def get_data(data):
	return {
		"fieldname": "item",
		"transactions": [
			{
				"label": _("Buy"),
				"items": ["Purchase Requisition", "Supplier Quotation","Request for Quotation","Purchase Order","Purchase Receipt","Purchase Invoice"]
	        },
			{
				"label": _("Stock Movement"),
				"items": [
					"Stock Entry",
				],
			},
			{
				"label": _("Pricing"),
				"items": ["Item Price"],
			}
		]
	}