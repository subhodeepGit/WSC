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
		
		frm.set_query("entrance_exam_declaration", function(){
			return {
				filters:{
					'docstatus':1
				}
			}
		})
		
		frm.set_query("applicant_id" , function(){
			return {
                query: "wsc.wsc.doctype.reporting_desk.reporting_desk.ra_query3",
				filters:{
					'entrance_exam_declaration':frm.doc.entrance_exam_declaration
				}
            }
		})
	},
	applicant_id: function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.reporting_desk.reporting_desk.reporting',
			args: {
				applicant_id:frm.doc.applicant_id
			},
			callback: function(result){
				
				const { applicant_name , gender , student_category , physically_disabled , academic_year , academic_term , department , total_marks , earned_marks} = result.message[0][0]
				
				frappe.model.clear_table(frm.doc, 'applicant_rank');

				frm.doc.applicant_name = applicant_name
				frm.doc.gender = gender
				frm.doc.student_category = student_category
				frm.doc.physically_disabled = physically_disabled
				frm.doc.academic_term = academic_term
				frm.doc.academic_year = academic_year
				frm.doc.department = department
				frm.doc.total_marks = total_marks
				frm.doc.earned_marks = earned_marks
				
				result.message[1].forEach((i) => {
					
					let c = frm.add_child('applicant_rank')
					const { rank_type , rank_obtained } = i
					c.rank_type = rank_type
					c.rank_obtained = rank_obtained

				})
				
				frm.refresh();
				frm.refresh_field("applicant_rank")

			}
		})
	},
});
