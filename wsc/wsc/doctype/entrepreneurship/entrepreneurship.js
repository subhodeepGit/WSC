// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrepreneurship', {
	number_of_employees: function(frm){
		if(isNaN(frm.doc.number_of_employees)){
			frm.set_value("number_of_employees", '')
			frappe.throw('value needs to be a positive number')
		}
		else if(frm.doc.number_of_employees < 0){
			frm.set_value("number_of_employees", '')
			frappe.throw('value needs to be a positive number')
		}
	}
});
