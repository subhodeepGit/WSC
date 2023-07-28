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
	},
    get__details(frm){
        if (frm.doc.academic_year && frm.doc.academic_term && frm.doc.program_grade) {
            frappe.call({
                method: 'get_details',
                doc:frm.doc,
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("remarks",r.message)
                    }
                    frm.refresh();
                    refresh_field('programs_pass_');
                }
            });
        }
    },
    academic_term: function(frm) {
		frm.trigger("get__details");
	},
	academic_year: function(frm) {
		frm.trigger("get__details");
	},
    program_grade: function(frm) {
		frm.trigger("get__details");
	},
});

