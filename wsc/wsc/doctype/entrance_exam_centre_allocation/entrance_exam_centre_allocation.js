// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Centre Allocation', {
	setup:function(frm){
		frm.set_query("entrance_exam_declaration", function() {
			return{
				filters:{
					"docstatus":1
				}
			}
		})
	}
});
