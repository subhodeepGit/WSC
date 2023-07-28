// Copyright (c) 2023, SOUL Limited and Contributors
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
	},
    get__details(frm){
        if (frm.doc.academic_year && frm.doc.academic_term && frm.doc.program_grade && frm.doc.programs) {
            frappe.call({
                method: 'get_details',
                doc:frm.doc,
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("remarks",r.message)
                    }
                    frm.refresh();
                    refresh_field('course_pass_');
                }
            });
        }
    },
    academic_term: function(frm) {
		frm.trigger("get__details");
        refresh_field('course_pass_');
	},
	academic_year: function(frm) {
		frm.trigger("get__details");
        refresh_field('course_pass_');
	},
    program_grade: function(frm) {
		frm.trigger("get__details");
        refresh_field('course_pass_');
	},
    programs: function(frm) {
		frm.trigger("get__details");
        refresh_field('course_pass_');
	},
});
