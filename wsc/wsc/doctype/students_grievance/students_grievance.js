// Copyright (c) 2022, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Students Grievance', {
		setup: function(frm) {
			frm.set_query('grievance_against_party', function() {
				return {
					filters: {
						name: ['in', [
							'Department', 'Employee Group', 'Employee']
						]
					}
				};
			});
		},
	
		grievance_against_party: function(frm) {
			let filters = {};
			if (frm.doc.grievance_against_party == 'Employee' && frm.doc.raised_by) {
				filters.name =  ["!=", frm.doc.raised_by];
			}
			frm.set_query('grievance_against', function() {
				return {
					filters: filters
				};
			});
		},
});
