// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
let c = 0;
frappe.ui.form.on('Rank Card Publication Tool', {
	refresh:function(frm){
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__('Generate Ranks') , function(){
				if(frm.doc.ranked_students_list.length != 0){
					frappe.call({
						method:'wsc.wsc.doctype.rank_card_publication_tool.rank_card_publication_tool.generate_rank_cards',
						args:{
							'doc':frm.doc
						}
					})
				}
			}).addClass("btn-primary")
		}
	},
	setup:function(frm){
		frm.set_query("academic_term", function() {
			return {
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		})
	
		frm.set_query("entrance_exam_declaration", function() {
            return {
                query: "wsc.wsc.doctype.rank_card_publication_tool.rank_card_publication_tool.ra_query"
            }
        })

		frm.set_query("department", function(){
	        return{
	            filters:{
	                "is_group":1,
	                "is_stream": 1
	            }
	        }
	    })

		frm.set_query("rank_card_masters" , function(){
			return {
				 filters: {
					"academic_year":frm.doc.academic_year,
					"department":frm.doc.department
				 }
			}
		})
		// frm.set_query("rank_card_masters" , function(){
		// 	return {
		// 		filters:{
		// 			"docstatus":1,
		// 		}
		// 	}
		// })
	},
	get_applicants:function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.rank_card_publication_tool.rank_card_publication_tool.get_qualified_applicants',
			args:{
				//add course type and filter as such
				 'declaration':frm.doc.entrance_exam_declaration,
				 'academic_year':frm.doc.academic_year,
				 'academic_term':frm.doc.academic_term,
				 'department':frm.doc.departments,
				 "rank_card_masters":frm.doc.rank_card_masters
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
					c.earned_marks = i.earned_marks
					c.rank_type = i.rank_type
					c.rank = i.Rank
				})
				frm.refresh();
				frm.refresh_field("ranked_students_list")
			}
		})
	}
});
