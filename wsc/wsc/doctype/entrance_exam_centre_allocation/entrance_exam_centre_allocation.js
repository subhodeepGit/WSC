// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Centre Allocation', {
	// refresh:function(frm){
		// if(!frm.is_new()){
		// 	frappe.call({
		// 		method:'wsc.wsc.doctype.entrance_exam_centre_allocation.entrance_exam_centre_allocation.get_centers',
		// 		args:{
		// 			center_selection:frm.doc.center_selection
		// 		},
		// 		callback: function(result){
					
		// 			const res = result.message
		// 			let arr= ['']
		// 			res.map((r) => {
		// 				const { center } = r
		// 				arr.push(center)
		// 				// frm.set_df_property('centre', 'options', arr)
						
		// 			})
		// 			set_field_options("centre" , arr)
		// 		}
		// 	})	
		// }
	// },
	setup:function(frm){
		frm.set_query("entrance_exam_declaration", function() {
            return {
                query: "wsc.wsc.doctype.entrance_exam_centre_allocation.entrance_exam_centre_allocation.ra_query"
            }
        })

		frm.set_query("centre" , function() {
			return {
				filters:{
					'academic_year':frm.doc.academic_year,
					'academic_term':frm.doc.academic_term,
					'available_center': 1,
					"docstatus":1
				}
			}
		})

	}
	// entrance_exam_declaration:function(frm){
	// 	let arr = [" "]
	// 	// frm.set_df_property('centre', 'options', arr)
	// 	if(frm.doc.center_selection){
	// 		frappe.call({
	// 			method:'wsc.wsc.doctype.entrance_exam_centre_allocation.entrance_exam_centre_allocation.get_centers',
	// 			args:{
	// 				center_selection:frm.doc.center_selection
	// 			},
	// 			callback: function(result){
					
	// 				const res = result.message
					
	// 				res.map((r) => {
	// 					const { center } = r
	// 					arr.push(center)
	// 					// frm.set_df_property('centre', 'options', arr)
						
	// 				})
	// 				// console.log(arr);
	// 				// set_field_options("centre" , arr)
	// 			}
	// 		})
	// 	}
	// },
	// centre:function(frm){
	// 	console.log(1);
	// 	frappe.call({
	// 		method:'wsc.wsc.doctype.entrance_exam_centre_allocation.entrance_exam_centre_allocation.get_centers_data',
	// 		args:{
	// 			center:frm.doc.centre
	// 		},
	// 		callback:function(result){
	// 			const res = result.message
	// 			if(res.length !== 0){
	// 				const { center_name , address , district , pincode , state} = res[0]
	// 				frm.doc.centre_name = center_name
	// 				frm.doc.address = address
	// 				frm.doc.district = district
	// 				frm.doc.state = state
	// 				frm.doc.pin_code = pincode

	// 				frm.refresh();
	// 			}
	// 		}
	// 	})
	// },
	// before_save:function(frm){
		
	// 	const exam_start_date = new Date(frm.doc.exam_start_date)
	// 	const exam_end_date = new Date(frm.doc.exam_end_date)

	// 	frm.doc.exam_slot_timings.map((item) => {
			
	// 		const start_time = new Date(item.slot_starting_time)
	// 		const end_time = new Date(item.slot_ending_time)
	
	// 		if((start_time >= exam_start_date && start_time < exam_end_date) && (end_time > exam_start_date && end_time <= exam_end_date)){
	// 			console.log("its within range of center booking timings");

	// 		} else {
	// 			// alert("its out of range of center booking timings")
	// 			frappe.throw("its out of range of center booking timings")
	// 		}
	// 	})
		
	// }
});


frappe.ui.form.on('Entrance Exam Invigilator', {
	entrance_exam_invigilator_add:function(frm){
		frm.fields_dict['entrance_exam_invigilator'].grid.get_field('invigilator_id').get_query = function(doc){
			var invigilator_id_list = [];
			if(!doc.__islocal) invigilator_id_list.push(doc.name);
			$.each(doc.entrance_exam_invigilator, function(idx, val){
				if (val.invigilator_id) invigilator_id_list.push(val.invigilator_id);
			});
			return { filters: [['Employee', 'name', 'not in', invigilator_id_list]] };
		}
	}
})