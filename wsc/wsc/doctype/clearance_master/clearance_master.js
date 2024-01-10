// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Clearance Master', {
	refresh: function(frm) {
        frm.fields_dict.user_disable_date.datepicker.update({
            minDate: new Date(frappe.datetime.get_today()),
        });
        frm.set_query("academic_term", function() {
            return{
                filters:{
                    "academic_year":frm.doc.academic_year
                    }
                }
        })
	},
});
frappe.ui.form.on('Clearance Departments', {
	department_clearance_add: function(frm){
		frm.fields_dict['department_clearance'].grid.get_field('employee').get_query = function(doc){
			var employee_list = [];
			if(!doc.__islocal) employee_list.push(doc.name);
			$.each(doc.department_clearance, function(idx, val){
				if (val.employee) employee_list.push(val.employee);
			});
			return { filters: [['Employee', 'name', 'not in', employee_list]] };
		};
	}
})

