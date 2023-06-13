// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Admit Card Tool', {
	setup:function(frm){
		frm.set_query("entrance_exam_declaration" , function(){
			return {
				filters: {
					docstatus:1
				}
			}
		})
	},
	refresh:function(frm){
		// frm.disable_save()
		// frm.set_df_property('deallotted_applicant_list', 'cannot_add_rows', true)
		// frm.set_df_property('deallotted_applicant_list', 'cannot_delete_rows', true)

		frm.add_custom_button(__('Admit Card Generation'), function(){

			console.log(frm.doc.entrance_exam_declaration);
			frappe.call({
				method:'wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.student_allotment',
				args:{
					declaration:frm.doc.entrance_exam_declaration,
				}	
			})
		}).addClass('btn-primary');
	},
	get_applicants:function(frm){
		if(frm.doc.entrance_exam_declaration.length !== 0){
			console.log(frm.doc.entrance_exam_declaration);
			frappe.call({
				method:'wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.get_applicants',
				args:{
					declaration:frm.doc.entrance_exam_declaration,
				},
				callback:function(result){
					const res = result.message
					frappe.model.clear_table(frm.doc, 'deallotted_applicant_list');
					res.map((r) => {
						const { applicant_id , applicant_name , student_category , gender  , physical_disability , center_allocated_status} = r
						let c =frm.add_child('deallotted_applicant_list')
						c.applicant_id= applicant_id
						c.applicant_name = applicant_name
						c.student_category = student_category
						c.gender = gender
						c.physical_disability = physical_disability
						c.center_allocated_status = center_allocated_status
					})
					frm.refresh();
					frm.refresh_field("deallotted_applicant_list")
				}
			})
		} 
	}
});
