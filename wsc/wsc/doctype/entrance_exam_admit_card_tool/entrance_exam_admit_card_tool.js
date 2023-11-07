// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
// let flag = 0
frappe.ui.form.on('Entrance Exam Admit Card Tool', {
	setup:function(frm){
		// flag = 0
		
		frm.set_query("entrance_exam_declaration", function() {
            return {
                query: "wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.ra_query"
            }
        })	

		frm.set_query("center" , function(){
			return {
                query: "wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.ra_query2",
				filters:{
					'entrance_exam_declaration':frm.doc.entrance_exam_declaration
				}
            }
		})
	},
	refresh:function(frm){
		// frm.disable_save()
		frm.set_df_property('deallotted_applicant_list', 'cannot_add_rows', true)
		// frm.set_df_property('deallotted_applicant_list', 'cannot_delete_rows', true)
		frm.set_df_property('center' , 'hidden' , 0)
		frm.remove_custom_button('Admit Card Generation')

		console.log(frm.doc.flag);
		
		// if(frm.doc.docstatus === 1 && frm.doc.flag === 0){
		if(frm.doc.docstatus === 1){
			
			console.log("inside first if");

			if(frm.doc.flag === 1){  //For Leftover Applicants

				console.log("inside flag = 1");

				frm.set_df_property('center' , 'hidden' , 0)
				frm.add_custom_button(__('Admit Card Generation'), function(){
				
					console.log("flag = 1" , frm.doc.flag);
					const res = frm.doc.deallotted_applicant_list.filter((i) => i.center_allocated_status === 0)
				
					const body = JSON.stringify({
						name:frm.doc.name ,
						declaration:frm.doc.entrance_exam_declaration,
						leftovers:res,
						center:frm.doc.center,
					})
					frappe.call({
					method:'wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.leftovers_allotment',
					args:{
						body:body
					},
					callback:function(result){
						
						const options = [" "]
						const { leftovers } = result.message
			
						if (leftovers.length !== 0) {
							
							alert(`Number of Unalloted Students is ${leftovers.length}`)
							
						}
						else {
							
							alert("All Students Alloted")
							frm.remove_custom_button('Admit Card Generation')		
						}
						window.location.reload();
						frm.refresh()
						frm.refresh_field("deallotted_applicant_list")
						frm.refresh_field("center")
					}
				}) 
				}).addClass('btn-primary');

			}
	
			if(frm.doc.flag === 2){
				
				frm.set_df_property('center' , 'hidden' , 1)
				frm.remove_custom_button('Admit Card Generation')
			}

			if(frm.doc.flag === 0){  //First Itteration for

				console.log("inside flag = 0");

				frm.add_custom_button(__('Admit Card Generation'), function(){
				
					// if(frm.doc.flag === 0){
						console.log("flag = 0" , frm.doc.flag);

						const body = JSON.stringify({
							name:frm.doc.name ,
							declaration:frm.doc.entrance_exam_declaration,
							de_allocated_student:frm.doc.deallotted_applicant_list
						})
						frappe.call({
							method:'wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.student_allotment',
							args:{
								body:body
							},
							callback:function(result){
								console.log(result.message);
								
								const { leftovers } = result.message
								
								if (leftovers.length !== 0) {
									alert(`Number of Unalloted Students is ${leftovers.length}`)
									frm.set_value({'flag':1}) 
								}
								else {
									alert("All Students Alloted")
									frm.remove_custom_button('Admit Card Generation')
								}
								window.location.reload();
								frm.refresh()
								frm.refresh_field("deallotted_applicant_list")
								frm.refresh_field("center")
							}	
						}) 
					// } 
				}).addClass('btn-primary');
			}
		}
	},
	
	get_applicants:function(frm){
		if(frm.doc.entrance_exam_declaration.length !== 0){
			
			frappe.call({
				method:'wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.get_applicants',
				args:{
					declaration:frm.doc.entrance_exam_declaration,
				},
				callback:function(result){
					// console.log(result.message);
					frappe.model.clear_table(frm.doc, 'deallotted_applicant_list');
					if(result.message.length !== 0){
						result.message.map((r) => {
							const { applicant_id , applicant_name , student_category , gender , physical_disability } = r
							let c =frm.add_child('deallotted_applicant_list')
							c.applicant_id= applicant_id
							c.applicant_name = applicant_name
							c.student_category = student_category
							c.gender = gender
							c.physical_disability = physical_disability
						})
						frm.refresh();
						frm.refresh_field("deallotted_applicant_list")
						// alert("Students Alloted")
					} else {
						alert("All Students Alloted")
					}
				}
			})
		} 
	}
});
