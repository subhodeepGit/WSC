// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Participant', {
	refresh: function(frm){
		frm.set_df_property('previous_participations', 'cannot_add_rows', true)
		frm.set_df_property('previous_participations', 'cannot_delete_rows', true)
	},
	setup:function(frm){
		frm.set_query("block", function() {
            return {
                filters: {
                    "districts":frm.doc.district
                }
            }; 
        });

        frm.set_query("district", function() {
            return {
                filters: {
                    "state":frm.doc.state
                }
            };
        });
	}
	// developers notes
	
	// the data for the previous participation selection will be filled from the ToT Participant reporting screen as that marks the participant as physically 
	// present for the program and at that point the participant should be considered to have participated in the program
	// hence the user cannot enter or delete records for the previous_participations table from this screen.
	
// 	onload:function(frm){
// 			var dialog = new frappe.ui.Dialog({
// 				fields: [
// 					{
// 						"label" : "Date",
//                         "fieldname": "course_schedule_date",
//                         "fieldtype": "Date",
//                         "reqd":1,
// 					}
// 				],
// 				primary_action: function() {
// 					var data = dialog.get_values();
// 						// frm.set_query("course_schedule", function () {
// 						// 	return {
// 						// 		filters: {
// 						// 			"schedule_date":data.course_schedule_date
// 						// 		}
// 						// 	}
// 						// });
// 					dialog.hide(); 
// 				}
// 			});
// 			dialog.show();
//     },
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
