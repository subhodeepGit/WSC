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
    get_result:function(frm){
        frm.clear_table("course_pass_");
        if (frm.doc.academic_year && frm.doc.academic_term && frm.doc.program_grade && frm.doc.programs) {
            frappe.call({
                method: 'get_details',
                doc:frm.doc,
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("status",r.message)
                    }
                    frm.refresh();
                    refresh_field('course_pass_');
                }
            });
        }
        else{
            frappe.throw("Please Enter the Mandatory Fields First")
        }
    },
    academic_term: function(frm) {
		frm.trigger("get_details");
        refresh_field('course_pass_');
	},
	academic_year: function(frm) {
		frm.trigger("get_details");
        refresh_field('course_pass_');
	},
    program_grade: function(frm) {
		frm.trigger("get_details");
        refresh_field('course_pass_');
	},
    programs: function(frm) {
		frm.trigger("get_details");
        refresh_field('course_pass_');
	},
});
