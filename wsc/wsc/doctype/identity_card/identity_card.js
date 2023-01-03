// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Identity Card', {
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) { 
					// frm.set_value("date",frappe.datetime.get_today())
					if(r.message){
						if (r.message['academic_year']){
							frm.set_value("session",r.message['academic_year'])
						}
						if (r.message['programs']){
							frm.set_value("class_stream",r.message['programs'])
						}
						// if (r.message['prn']){
						// 	frm.set_value("permanant_registration_number",r.message['prn'])
						// }
					}
				} 
			}); 
		}
	}
});
