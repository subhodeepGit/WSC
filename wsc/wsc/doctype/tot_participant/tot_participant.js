// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Participant', {
	onload:function(frm){
			var dialog = new frappe.ui.Dialog({
				fields: [
					{
						"label" : "Date",
                        "fieldname": "course_schedule_date",
                        "fieldtype": "Date",
                        "reqd":1,
					}
				],
				primary_action: function() {
					var data = dialog.get_values();
						// frm.set_query("course_schedule", function () {
						// 	return {
						// 		filters: {
						// 			"schedule_date":data.course_schedule_date
						// 		}
						// 	}
						// });
					dialog.hide(); 
				}
			});
			dialog.show();
    },
//    onload: function(frm) {
//         frm.add_field({
//             fieldname: 'your_fieldname',
//             label: __('Your Field'),
//             fieldtype: 'Data',
//             reqd: 1,
//             // Add other field properties as needed
//         });
//     }
});
