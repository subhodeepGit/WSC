// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scholarships', {
	refresh: function(frm) {
		frm.set_query("document_required", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year,
					"student_category":frm.doc.student_category
                }
            };
        })
	}
});
