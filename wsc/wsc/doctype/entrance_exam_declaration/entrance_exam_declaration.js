// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Declaration', {
	setup:function(frm){
		frm.set_query("academic_term", function() {
			return{
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		})
		frm.set_query("center_selection" , function() { 
			return {
				filters:{
					 "docstatus":1,
					 "academic_year":frm.doc.academic_year,
					 "academic_term":frm.doc.academic_term
				}
			}
		})
		frm.set_query("department", function(){
	        return{
	            filters:{
	                "is_group":0,
	                // "is_stream": 1
	            }
	        }
	    });
	}, 
	get_applicants:function(frm){
		if(!frm.is_new()){
			let body = JSON.stringify({
				academic_year:frm.doc.academic_year,
				academic_term:frm.doc.academic_term,
				department:frm.doc.department
			})
			// console.log(body);
			frappe.call({
				method:'wsc.wsc.doctype.entrance_exam_declaration.entrance_exam_declaration.get_applicants',
				args:{
					'body':body
				},
				callback:function(result){
					const res = result.message
					frappe.model.clear_table(frm.doc, 'applicant_list');
					
					if(res.length !== 0){
						res.map((values) => {
							const { name , title , gender , student_category , physically_disabled} = values
							let c =frm.add_child('applicant_list')
							c.applicant_id = name
							c.applicant_name = title
							c.gender = gender
							c.student_category = student_category
							c.physical_disability = physically_disabled
						})
						frm.refresh();
						frm.refresh_field("applicant_list")
					} else {
						alert("No Applicants found")
						frappe.model.clear_table(frm.doc, 'applicant_list');
						frm.refresh();
						frm.refresh_field("applicant_list")
					}
					
				}
			})
		}
	},
	refresh:function(frm){
		if(!frm.is_new()){
			frm.set_df_property('get_applicants' , 'hidden' , 0)
		}
		else{
			frm.set_df_property('get_applicants' , 'hidden' , 1)
		}
		if(frm.doc.docstatus==1){
			frm.set_df_property('get_applicants' , 'hidden' , 1)
		}
		frm.set_df_property("applicant_list", "cannot_add_rows", true);
	},
	before_submit:function(frm){
		if(frm.doc.applicant_list.length === 0){
			frm.set_df_property("applicant_list" , 'reqd' , 1)
			frm.refresh()
		} else {
			frm.set_df_property("applicant_list" , 'reqd' , 0)
			frm.refresh()
		}
	}
});
