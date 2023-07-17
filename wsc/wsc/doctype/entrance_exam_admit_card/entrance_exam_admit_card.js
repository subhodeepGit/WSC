// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Admit Card', {
	setup:function(frm){
		frm.set_query("applicant_id", function() {
			return{
				filters:{
					"docstatus":1
				}
			}
		});
	},
	applicant_id:function(frm){
		let arr = [' ']
		frappe.call({
			method:'wsc.wsc.doctype.entrance_exam_admit_card.entrance_exam_admit_card.center_option',
			args:{
				applicant_id:frm.doc.applicant_id,
				academic_year:frm.doc.academic_year,
				academic_term:frm.doc.academic_term,
				department:frm.doc.department
			}
		})
	}
});
