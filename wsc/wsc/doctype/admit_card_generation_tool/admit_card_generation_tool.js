// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Admit Card Generation Tool', {
	setup:function(frm){
		frm.set_query("entrance_exam_allocation" , function(){
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
	
			const slot = frm.doc.slot.split(",")
			body = JSON.stringify({
				deallotted_applicant_list:frm.doc.deallotted_applicant_list,
				centre_name:frm.doc.centre_name,
				slot:slot[0],
				exam_start_time:frm.doc.exam_start_time,
				exam_end_time:frm.doc.exam_end_time
			})
			// console.log(body); 
			frappe.call({
				method:'wsc.wsc.doctype.admit_card_generation_tool.admit_card_generation_tool.student_allotment',
				args:{
					body:body
				}	
			})
		}).addClass('btn-primary');
	},
	entrance_exam_allocation: function(frm){
		let arr = ['']
		frappe.call({
			method:'wsc.wsc.doctype.admit_card_generation_tool.admit_card_generation_tool.get_slots',
			args:{
				center_allocation:frm.doc.entrance_exam_allocation
			},
			callback:function(result){
				const res = result.message
				res.map((r) => {
	
					const { slot_name , slot_starting_time , slot_ending_time } = r
					const slot_date = slot_starting_time.split(" ")
					
					arr.push(`${slot_name} , ${slot_date[0]}`)
				})
				set_field_options("slot" , arr)
			}
		})
		if(frm.doc.entrance_exam_allocation.length === 0){
			frappe.model.clear_table(frm.doc, 'deallotted_applicant_list');
			frm.refresh();
			frm.refresh_field("deallotted_applicant_list")	
		}
	},
	slot:function(frm){
		if(frm.doc.slot){
			const slot = frm.doc.slot.split(",")
			
			frappe.call({
			method:'wsc.wsc.doctype.admit_card_generation_tool.admit_card_generation_tool.slot_timings',
			args:{
				slot:slot[0],
				parent:frm.doc.entrance_exam_allocation
			},
			callback:function(res){
				
				if(res.message){
					res.message.map((r) => {
						console.log(r);
						const { slot_starting_time , slot_ending_time } = r
						
						const date_time_starting = slot_starting_time.split(" ")
						const date_time_ending = slot_ending_time.split(" ")
						frm.doc.exam_date = date_time_starting[0]
						frm.doc.exam_start_time = date_time_starting[1]
						frm.doc.exam_end_time = date_time_ending[1]
					})
					frm.refresh()
				}
			}
		})
		}
		
	},
	get_applicant_list:function(frm){
		if(frm.doc.entrance_exam_allocation.length !== 0){
			frappe.call({
				method:'wsc.wsc.doctype.admit_card_generation_tool.admit_card_generation_tool.get_applicants',
				args:{
					centre_allocation:frm.doc.entrance_exam_allocation,
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
