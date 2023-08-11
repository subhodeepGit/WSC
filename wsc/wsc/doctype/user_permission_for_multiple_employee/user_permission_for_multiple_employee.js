// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('User Permission for multiple Employee', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('User Permission for multiple Employee Child', {
	employees_add: function(frm){
		frm.fields_dict['employees'].grid.get_field('employee').get_query = function(doc){
			var topics_list = [];
			if(!doc.__islocal) topics_list.push(doc.name);
			$.each(doc.employees, function(idx, val){
				if (val.employee) topics_list.push(val.employee);
			});
			return { filters: [['Employee', 'name', 'not in', topics_list],['Employee', 'not in', frm.doc.employee]] };
		};
	}
});
