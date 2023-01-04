// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Pass Percentage', {
	onload: function(frm) {
		frm.set_query("academic_term", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year
                }
            };
        });
	}
});
