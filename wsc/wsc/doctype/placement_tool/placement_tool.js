// frappe.ui.form.on('Placement tool',{
// 	refresh:function(frm){
// 		// disabling features in the tool (save, add row, delete row)
// 		frm.disable_save();
// 		frm.set_df_property('student_child_table', 'cannot_add_rows', true);
// 		frm.set_df_property('student_child_table', 'cannot_delete_rows', true);
// 		// setting filters
// 		frm.set_query('placement_drive_name', function(){
// 			return{
// 				filters:{
// 					"placement_company":frm.doc.company_name,
// 					"academic_year": frm.doc.placement_batch_year
// 				}
// 			}
// 		})
// 		frm.set_query('round_of_placement', function(){
// 			return{
// 				query: "wsc.wsc.doctype.Placement tool.Placement tool.get_round_of_placement",
// 				filters:{
// 					"parent":frm.doc.placement_drive_name	
// 				}
// 			}
// 		})
// 	},
// 	// placement_drive_name: function(frm){
// 	// 	// test code
// 	// 	if(1){
// 	// 		frappe.call({
// 	// 			method: 'wsc.wsc.doctype.Placement tool.Placement tool.get_placement_rounds.get_round_names',
// 	// 			args:{
// 	// 				drive_name: frm.doc.placement_drive_name,
// 	// 			},
// 	// 			callback: function(result){
// 	// 				if(result.message){
// 	// 					console.log(result);
// 	// 				}
// 	// 			}
// 	// 		})
// 	// 	}
// 	// },
// 	get_student: function(frm){
// 		if(frm.doc.company_name && frm.doc.placement_batch_year && frm.doc.placement_drive_name && frm.doc.round_of_placement && frm.doc.date_of_round){
// 			frappe.call({
// 				method:"wsc.wsc.doctype.Placement tool.Placement tool.get_student",
// 				args:{
// 					company_name: frm.doc.company_name,
// 					placement_year: frm.doc.placement_batch_year,
// 					drive_name: frm.doc.placement_drive_name,
// 					round_of_placement: frm.doc.round_of_placement,
// 					date_of_round: frm.doc.date_of_round
// 				},
// 				callback: function(result){
// 					if(result.message){
// 						alert(result.message);
// 						frappe.model.clear_table(frm.doc,'student_child_table')
// 						(result.message).forEach(element => {
// 							var childTable = frm.add_child('student_child_table')
// 							childTable.ref_no;
// 							childTable.student_no;
// 							childTable.student_name;
// 							childTable.program_name;
// 							childTable.academic_year;
// 							childTable.semesters;
// 						})
// 					}
// 					frm.refresh()
//                 	frm.refresh_field("student_child_table")
// 				}
// 			})
// 		}
// 	},

// 	// test button code
// 	test_btn: function(frm){
// 		if(frm.doc.placement_drive_name){
// 			frappe.call({
// 				method: 'wsc.wsc.doctype.Placement tool.Placement tool.test_Student_Data',
// 				args:{
// 					drive_name: frm.doc.placement_drive_name
// 				},
// 				callback: function(result){
// 					alert(result.message);
// 					if(result.message){
						
// 					}
// 				}
// 			})
// 		}
// 	}
// })


frappe.ui.form.on('Placement tool',{
    refresh: function(frm){
        // disabling features
        frm.disable_save()
        frm.set_df_property('student_child_table', 'cannot_add_rows', true)
        frm.set_df_property('student_child_table', 'cannot_delete_rows', true)

        // setting filters
        frm.set_query('placement_drive_name', function(){
            return{
                filters:{
                    'placement_company': frm.doc.company_name,
                    'academic_year': frm.doc.placement_batch_year
                }
            }
        })
    },
    get_student: function(frm){
        if(frm.doc.company_name && frm.doc.placement_batch_year && frm.doc.placement_drive_name){
            frappe.call({
                method: 'wsc.wsc.doctype.Placement tool.Placement tool.get_student',
                args:{
                    drive_name:frm.doc.placement_drive_name
                },
                callback: function(result){
                    if(result.message){
                        alert(result.message)
                    }
                }
            })
        }
    },
    test_button: function(frm){
        if(frm.doc.company_name && frm.doc.placement_batch_year && frm.doc.placement_drive_name){
            frappe.call({
                method:'wsc.wsc.doctype.Placement tool.Placement tool.test_button',
                args:{
                    drive_name : frm.doc.placement_drive_name
                },
                callback: function(result){
                    alert(result)
                }
            })
        }
    }
})