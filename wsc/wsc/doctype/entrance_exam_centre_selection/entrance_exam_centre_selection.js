// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Centre Selection', {
	setup:function(frm){
		frm.set_query("academic_term", function() {
			return{
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		})
		// frm.set_query('center', 'current_centers', function() {
		// 	return {
		// 		filters: {
		// 			'current_centers':1
		// 		}
		// 	};
		// });
	},
	refresh:function(frm){
		if(!frm.is_new() && frm.doc.docstatus === 1 && frm.doc.flag === 0){
			frm.add_custom_button(__('Center Select'), function(){
				frappe.call({
					method: 'selected_centers',
					doc: frm.doc
				})
				frm.remove_custom_button('Center Select')
			}).addClass('btn-primary');
		}
	},
	// after_cancel:function(frm){
	// 	console.log(1);
	// 	frappe.call({
	// 		method: 'wsc.wsc.doctype.entrance_exam_centre_selection.entrance_exam_centre_selection.centers_cancel',
	// 		args: {
	// 			academic_year:frm.doc.academic_year,
	// 			academic_term:frm.doc.academic_term
	// 		}
	// 	})
	// }
	
});
