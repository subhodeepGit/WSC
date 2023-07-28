// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('TnP Program', {
	refresh: function(frm) {

	},
	start_date : function(frm){
		if(frm.doc.start_date && frm.doc.end_date){
			if(frm.doc.start_date > frm.doc.end_date){
				frappe.throw("Application Start Date should be Less than Application Start date");
			}
		}
	},
	end_date:function(frm){
		if(frm.doc.start_date && frm.doc.end_date){
			if(frm.doc.end_date < frm.doc.start_date){
				frappe.throw("Application End Date should be Greater than Application Start date");
			}
		}
	},
});
