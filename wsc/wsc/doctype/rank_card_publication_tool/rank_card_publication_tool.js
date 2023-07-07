// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rank Card Publication Tool', {
	refresh:function(frm){
		frm.add_custom_button(__('Generate Ranks') , function(){
			// console.log(frm.doc.ranked_students_list)
			if(frm.doc.ranked_students_list.length != 0){
				const data = JSON.stringify(frm.doc.ranked_students_list)
				
				frappe.call({
					method:'wsc.wsc.doctype.rank_card_publication_tool.rank_card_publication_tool.generate_rank_cards',
					args:{
						data:data,
						posting_date:frm.doc.posting_date,
						total_marks:frm.doc.total_marks,
						department:frm.doc.department,
						academic_year:frm.doc.academic_year,
						rank_card_master:frm.doc.rank_card_master
					}
				})
			}
		}).addClass("btn-primary")
	},
	setup:function(frm){
		frm.set_query("academic_term", function() {
			return {
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		})
		frm.set_query("rank_card_masters" , function(){
			return {
				filters:{
					"docstatus":1,
				}
			}
		})
		frm.set_query("rank_card_masters" , function(){
			return {
				filters: {
					"docstatus":1,
				}
			}
		})
	},
	get_applicants:function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.rank_card_publication_tool.rank_card_publication_tool.get_qualified_applicants',
			args:{
				 'rank_card_master':frm.doc.rank_card_masters,
				 'academic_year':frm.doc.academic_year,
				 'academic_term':frm.doc.academic_term,
				 'department':frm.doc.departments
			},
			callback:function(result){
				frappe.model.clear_table(frm.doc, 'ranked_students_list');
				result.message.map((i) => {

					let c =frm.add_child('ranked_students_list')
					c.applicant_id = i.applicant_id
					c.applicant_name = i.applicant_name
					c.gender = i.gender
					c.student_category = i.student_category
					c.physical_disability = i.physically_disabled
					c.all_student_based_rank = i.Rank
					
					if (!i.Category_Rank){
						c.category_based_rank = "--"
					}
					else {
						c.category_based_rank = i.Category_Rank
					}

					if (!i.PWD_Rank){
						c.pwd_based_rank = "--"
					} else {
						c.pwd_based_rank = i.PWD_Rank
					}
				})
				frm.refresh();
				frm.refresh_field("ranked_students_list")
			}
		})
	}
});
