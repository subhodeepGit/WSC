// Copyright (c) 2022, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Students Grievance', {
	refresh: function(frm) {
		frm.set_query("type_of_grievance", function() {
            return {
                filters: {
                    "enable":1
                }
            };
        })


		if(frm.doc.docstatus===1 && frm.doc.status=="Issue Posted By the Student") {
			// alert("if condition is triggered")
			frm.add_custom_button(__("Register Complaint"), function() {
				frm.trigger("register_complaint")
				// alert("Function is triggerd")
			}).addClass("btn-primary");
		}

	},
	// register_complaint: function(frm) {
	// 	return frappe.call({
	// 		method: "wsc.wsc.doctype.students_grievance.students_grievance.get_register_complaint",
	// 		args: {
	// 			"dt": frm.doc.doctype,
	// 			"dn": frm.doc.name,
	// 		},
	// 		callback: function(r) {
	// 			var doc = frappe.model.sync(r.message);
	// 			frappe.set_route("Form", doc[0].doctype, doc[0].name);
	// 		}
	// 	});
	// },
	register_complaint: function(frm) {
		frappe.model.open_mapped_doc({
			method: "wsc.wsc.doctype.students_grievance.students_grievance.get_register_complaint",
			frm:frm,
		

		})
	}

});
