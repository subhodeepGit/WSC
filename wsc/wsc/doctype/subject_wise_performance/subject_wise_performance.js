// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subject Wise Performance', {
	onload: function(frm) {
		frm.set_query("academic_term", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year
                }
            };
        });
		frm.set_query("programs", function() {
            return {
                filters: {
                    "program_grade":frm.doc.program_grade,
                }
            };
        });
	}
});
