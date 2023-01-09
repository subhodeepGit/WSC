// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt


frappe.ui.form.on("Building Room", {
	setup: function(frm) {
		frm.set_query("residence_type_name", function() {
			return {
				filters: [
					["Quarter Type","type_of_residence", "in", [frm.doc.type_of_residence]],
                    
				]
			}
		});
	}
});