// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Academic Calendar Template', {
	setup(frm){
		frm.set_query("program", function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
	}
	
});
