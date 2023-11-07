// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Internship Drive', {
	refresh: function(frm) {
		frm.set_query('internship_company', function(){
			return{
				filters:{
					'visitor' : 'Internship',
					'black_list' : 0
				}
			}
		})
	},
	setup: function(frm){
		frm.set_query("semester","for_programs", function(frm, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					"programs" :d.programs
				}
			};
		});
	},
	application_start_date(frm) {
        frm.fields_dict.application_end_date.datepicker.update({
            minDate: frm.doc.application_start_date ? new Date(frm.doc.application_start_date) : null
        });
    },

    application_end_date(frm) {
        frm.fields_dict.application_start_date.datepicker.update({
            maxDate: frm.doc.application_end_date ? new Date(frm.doc.application_end_date) : null
        });
    },
	
});
