// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rank Card Master', {
	setup:function(frm){
		frm.set_query("entrance_exam_declaration" , function(){
			return {
				filters:{
					"docstatus":1,
				}
			}
		})
		frm.set_query("academic_term", function() {
			return {
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		})
	}
});
