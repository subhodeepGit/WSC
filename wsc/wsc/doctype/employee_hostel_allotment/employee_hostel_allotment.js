// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Hostel Allotment', {
	refresh: function(frm) {
		if(!frm.is_new()){
			frm.set_df_property('employees', 'read_only', 1)
		}
		else{
			frm.set_df_property('employees', 'read_only', 0)
		}
	},
	employees: function(frm) {
		if(frm.doc.employees){
			frappe.call({
				doc:frm.doc,
				method: "get_emp_data",
				callback: function(r) {
					if(r.message){
						if (r.message){
							frm.set_value("employee",r.message['employee_name'])
							frm.set_value("user_name",r.message['user_id'])
							frm.set_value("designation",r.message['designation'])
						}
					} 
				} 
			});
		}
	}
});
