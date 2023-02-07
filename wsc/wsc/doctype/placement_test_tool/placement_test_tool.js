// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Test Tool', {
	refresh: function(frm) {
		frm.disable_save()
		frm.set_df_property('student_records', 'cannot_add_rows', true)
		frm.set_df_property('student_records', 'cannot_remove_rows', true)
		frm.set_query('placement_drive_name', function(){
			return{
				filters: {
					'placement_company' : frm.doc.company_name,
					'academic_year' : frm.doc.placement_batch_year
				}
			}
		})
		if(!frm.doc.__isLocal){
			frm.add_custom_button(__('Create Selection Round'), function(){
				frappe.call({
					method : 'create_selection_rounds',
					doc: frm.doc,
					callback: function(result){
						
					}
				})
			}).addClass('btn-primary');
		}
	},
	get_student: function(frm){
		if(frm.doc.company_name && frm.doc.placement_batch_year && frm.doc.placement_drive_name){
			frappe.call({
				method: 'wsc.wsc.doctype.placement_test_tool.placement_test_tool.get_student',
				args:{
					drive_name: frm.doc.placement_drive_name
				},
				callback: function(result){
					if(result.message){
						
						frappe.model.clear_table(frm.doc, 'student_records')
						result.message.forEach(element => {
							var childTable = frm.add_child('student_records')
							childTable.ref_no = element.name
							childTable.student_no = element.student
							childTable.student_name = element.student_name
							childTable.program_name = element.programs
							childTable.academic_year = element.academic_year
							childTable.semesters = element.semesters
						})
					}
					frm.refresh()
					frm.refresh_field('student_records')
				}
			})
		}
	},
	placement_drive_name: function(frm){
		if(frm.doc.company_name && frm.doc.placement_batch_year && frm.doc.placement_drive_name){
			frappe.call({
				method:'wsc.wsc.doctype.placement_test_tool.placement_test_tool.rounds_of_placement',
				args:{
					drive_name: frm.doc.placement_drive_name
				},
				callback: function(result){
					let arr = [];
					for(let x in result.message){
						arr.push(result.message[x]);
					}

					frm.set_df_property('round_of_placement', 'options', arr)
					
				}
			})
		}	
	},
	round_of_placement: function(frm){
		if(frm.doc.company_name && frm.doc.placement_batch_year && frm.doc.placement_drive_name){
			frappe.call({
				method: 'wsc.wsc.doctype.placement_test_tool.placement_test_tool.date_of_placement',
				args:{
					doc: frm.doc,
					drive_name : frm.doc.placement_drive_name,
					round_name: frm.doc.round_of_placement
				},
				callback: function(result){
					for(let x in result.message){
						alert(result.message[x])
					}
					
				}
			})
		}
	}
});
