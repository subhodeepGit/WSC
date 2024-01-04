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
	}
});
