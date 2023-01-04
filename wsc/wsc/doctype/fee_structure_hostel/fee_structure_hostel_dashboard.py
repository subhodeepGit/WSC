
from frappe import _


def get_data():
	return {
		# 'heatmap': True,
		# 'heatmap_message': _('This is based on transactions against this Customer. See timeline below for details'),
		# 'fieldname': 'customer',
		'non_standard_fieldnames': {
			'Hostel Fees': 'hostel_fee_structure',
            'Hostel Fee Schedule': 'fee_structure'
		},
		'transactions': [
			{
				'label': _('Fee'),
				'items': ['Hostel Fees', 'Hostel Fee Schedule']
			},
		]
	}
