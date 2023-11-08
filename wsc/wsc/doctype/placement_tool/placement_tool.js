// // Copyright (c) 2023, SOUL Limited and contributors
// // For license information, please see license.txt

frappe.ui.form.on('Placement Tool', {
	refresh: function(frm){
		frm.set_df_property('student_list', 'cannot_add_rows', true)
		// frm.set_df_property('student_list', 'cannot_delete_rows', true)
		frm.set_query('placement_drive_name', function(){
			return{
				filters:{
					'placement_company' : frm.doc.company_name,
					'academic_year' : frm.doc.placement_batch_year,
					'title' : frm.doc.drive_title,
					"docstatus":1
				}
			}
		})
		frm.set_query('company_name', function(){
			return{
				filters:[
					["black_list", "=", "0"],
					["visitor", "!=", "Internship"]
				]
			}
		})
	}, 

	round_status : function(frm){
		//  get rounds based on whether rounds are being scheduled or result is being declared
		frappe.call({
			method : 'wsc.wsc.doctype.placement_tool.placement_tool.get_placement_round_names',
			args : {
				self : frm.doc,
				drive_name : frm.doc.placement_drive_name,
				round_status : frm.doc.round_status
			},
			callback : function(result){
				frm.set_df_property('round_of_placement', 'options', result.message)
			}
		})
	},

	round_of_placement : function(frm){
		// based on the chosen round of the placement drive, the scheduled date, time and location of the round will be filled in the fields
		frappe.call({
			method : 'wsc.wsc.doctype.placement_tool.placement_tool.get_round_details',
			args : {
				doc : frm.doc,
				drive_name : frm.doc.placement_drive_name,
				round_name : frm.doc.round_of_placement
			},
			callback : function(result){
				frm.set_value("scheduled_date_of_round", result.message[0])
				frm.set_value("scheduled_time_of_round", result.message[1])
			}
		})
	},

	get_eligible_students_list : function(frm){
		// get the students from the placement drive and fill the fields of the student_list child table
		frappe.call({
			method : 'wsc.wsc.doctype.placement_tool.placement_tool.get_students',
			args: {
				drive_name : frm.doc.placement_drive_name
			},
			callback : function(result){
				// alert(JSON.stringify(result))
				if(result.message){
					frappe.model.clear_table(frm.doc, 'student_list')
					result.message.forEach(element => {
						var childTable = frm.add_child('student_list')
						childTable.ref_no = element.name
						childTable.student_no = element.student
						childTable.student_name = element.student_name
						childTable.program_name = element.programs
						childTable.academic_year = element.academic_year
						childTable.semesters = element.semesters
						childTable.last_round = element.status
					})
				}
				frm.refresh()
				frm.refresh_field('student_list')
			}
		})
	}
})