// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reporting Desk', {
	setup: function(frm){
		frm.set_query("academic_term", function(){
			return {
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		})
	},
	applicant_id: function(frm){
		console.log(1);
		frappe.call({
			method:'wsc.wsc.doctype.reporting_desk.reporting_desk.reporting',
			args: {
				applicant_id:frm.doc.applicant_id
			},
			callback: function(result){
				const { applicant_name , gender , student_category , physically_disabled , academic_year , academic_term , department , total_marks , earned_marks} = result.message[0][0]
				const { general_rank , category_based_rank , pwd_based_rank } = result.message[1][0]
				
				frm.doc.applicant_name = applicant_name
				frm.doc.gender = gender
				frm.doc.student_category = student_category
				frm.doc.physically_disabled = physically_disabled
				frm.doc.academic_term = academic_term
				frm.doc.academic_year = academic_year
				frm.doc.department = department
				frm.doc.total_marks = total_marks
				frm.doc.earned_marks = earned_marks

				frappe.model.clear_table(frm.doc, 'applicant_rank');

				let c = frm.add_child('applicant_rank')

				c.general_rank = general_rank
				c.category_based_rank = category_based_rank
				c.pwd_based_rank = pwd_based_rank

				frm.refresh();
				frm.refresh_field("deallotted_applicant_list")
			}
		})
	},
});
