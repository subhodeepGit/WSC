// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on(`Entrance Exam Centre Selection`, {
	setup:function(frm){
		frm.set_query("academic_term", function() {
			return{
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		})
	},
	refresh:function(frm){
		console.log(frm.doc.flag);
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

	// before_cancel: function(frm){
	// 	frm.doc.flag = 0
	// 	frm.refresh_field('flag');
	// 	console.log(frm.doc.flag);
	// }
	
});


frappe.ui.form.on('Current Centers', {
	current_centers_add: function(frm){
		frm.fields_dict['current_centers'].grid.get_field('center').get_query = function(doc){
			var center_list = [];
			if(!doc.__islocal) center_list.push(doc.name);
			$.each(doc.current_centers, function(idx, val){
				if (val.center) center_list.push(val.center);
			});
			return { filters: [['Entrance Exam Centre Master', 'name', 'not in', center_list]] };
		};
	}
});