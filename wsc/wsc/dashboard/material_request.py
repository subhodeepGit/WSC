from __future__ import unicode_literals
from frappe import _


def get_data(data):
	return {
		"fieldname": "item",
		"transactions": [
			# {
			# 	"label": _("References"),
			# 	"items": ["Request for Quotation","Supplier Quotation","Purchase Order"]
	        # },
			# {
			# 	"label": _("Stock"),
			# 	"items": ["Stock Entry","Purchase Receipt"]
	        # },
        ]
	}