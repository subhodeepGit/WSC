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
		const date = new Date()
		let year = date.getFullYear()
		let month = String(date.getMonth() + 1).padStart(2,'0')
		let day = String(date.getDate()).padStart(2,'0')
		frm.set_value('current_date', `${year}-${month}-${day}`)
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
	application_start_date: function(frm){
		if(frm.doc.application_start_date < frm.doc.current_date){
			frappe.throw('Start date cannot be before current date')
		}
	},
	application_end_date:function(frm){
		if(frm.doc.application_start_date && frm.doc.application_end_date){
			if(frm.doc.application_end_date < frm.doc.application_start_date){
				frappe.throw("Application End Date should be Greater than Application Start date");
			}
		}
	},
});
