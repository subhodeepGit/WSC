// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Type of Grievance', {
	refresh: function(frm) {
		frm.set_query("type_of_grievance", function() {
            return {
                filters: {
                    "disable":0
                }
            };
        })
	},

});

frappe.ui.form.on('Standard WorkFlow For Grievance', {
    workflow_of_grievance_add: function(frm){
		frm.fields_dict['workflow_of_grievance'].grid.get_field('emp_no').get_query = function(doc){
			var emp_no_list = [];
			if(!doc.__islocal) emp_no_list.push(doc.name);
			$.each(doc.workflow_of_grievance, function(idx, val){
				if (val.emp_no) emp_no_list.push(val.emp_no);
			});
			return { filters: [['Employee', 'name', 'not in', emp_no_list]] };
		};
	}
})
