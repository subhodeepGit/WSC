// Copyright (c) 2022, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Division Child', {
	departments_add: function(frm){
		frm.fields_dict['departments'].grid.get_field('department').get_query = function(doc){
			var department_list = [];
			$.each(doc.departments, function(idx, val){
				if (val.department) department_list.push(val.department);
			});
			return { filters: [['Department', 'name', 'not in', department_list],['is_group','=',0]] };
		};
	}
});