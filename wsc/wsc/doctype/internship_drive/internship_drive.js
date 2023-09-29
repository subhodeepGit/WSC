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
	application_start_date : function(frm){
		if(frm.doc.application_start_date && frm.doc.application_end_date){
			if(frm.doc.application_start_date > frm.doc.application_end_date){
				frappe.throw("Application Start Date should be Less than Application Start date");
			}
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
