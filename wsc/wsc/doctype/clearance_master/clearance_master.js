// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Clearance Master', {
	refresh: function(frm) {
        frm.fields_dict.user_disable_date.datepicker.update({
            minDate: new Date(frappe.datetime.get_today()),
        });
        frm.set_query("academic_term", function() {
            return{
                filters:{
                    "academic_year":frm.doc.academic_year
                    }
                }
        })
	},
});
