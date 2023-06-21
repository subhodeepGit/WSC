// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
let flag = 0
frappe.ui.form.on('Entrance Exam Admit Card Tool', {
	setup:function(frm){
		// var childTableRecords = frm.doc.deallotted_applicant_list || []

		// var filterValues = childTableRecords.map(function(record){
		// 	return record.center_allocated_status
		// })

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
		// const flag = 0;
		frm.add_custom_button(__('Admit Card Generation'), function(){
			
			if(flag == 0){
				console.log("normal call");
				const body = JSON.stringify({
					declaration:frm.doc.entrance_exam_declaration,
					de_allocated_student:frm.doc.deallotted_applicant_list
				})
				frappe.call({
					method:'wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.student_allotment',
					args:{
						body:body
					},
					callback:function(result){
						const options = [" "]
						frm.refresh()
						frm.refresh_field("deallotted_applicant_list")
						frm.refresh_field("centre")
						const { leftovers } = result.message
						const { available_centers } = result.message
			
						if (leftovers.length !== 0) {
							available_centers.map((i) => {
								
								const date = i.slot_starting_time.split(" ")
								options.push(`${i.centre_name} - ${i.slot_name} - ${i.district} - ${date[0]}`)
							})
	
							set_field_options("centre" , options)
							alert(`Number of Unalloted Students is ${leftovers.length}`)
							flag = 1
						}
						else {
							alert("All Students Alloted")
						}
					}	
				}) 
			} else {
				  console.log("special call");
				  const res = frm.doc.deallotted_applicant_list.filter((i) => i.center_allocated_status === 0)
				  let center_detail = frm.doc.centre.split(" - ")
				  const body = JSON.stringify({
					declaration:frm.doc.entrance_exam_declaration,
					leftovers:res,
					center:center_detail,
				  })
				  frappe.call({
					method:'wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.leftovers_allotment',
					args:{
						body:body
					},
					callback:function(result){
						frm.refresh()
						frm.refresh_field("deallotted_applicant_list")
						frm.refresh_field("centre")
						const options = [" "]
						const { leftovers } = result.message
						const { available_centers } = result.message
			
						if (leftovers.length !== 0) {
							available_centers.map((i) => {
								const date = i.slot_starting_time.split(" ")
								options.push(`${i.centre_name} - ${i.slot_name} - ${i.district} - ${date[0]}`)
							})
	
							set_field_options("centre" , options)
							alert(`Number of Unalloted Students is ${leftovers.length}`)
							flag = 1
						}
						else {
							alert("All Students Alloted")
						}
					}
				  })
			}
			
		}).addClass('btn-primary');
	},
	// centre:function(frm){
		
	// },
	get_applicants:function(frm){
		if(frm.doc.entrance_exam_declaration.length !== 0){
			
			frappe.call({
				method:'wsc.wsc.doctype.entrance_exam_admit_card_tool.entrance_exam_admit_card_tool.get_applicants',
				args:{
					declaration:frm.doc.entrance_exam_declaration,
				},
				callback:function(result){
					console.log(result.message);
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
