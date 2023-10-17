// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Result Declaration Tool', {
	refresh: function(frm) {
		frm.set_query("tot_participant_enrollment", function() {
            return {
                filters: {
                    'docstatus': 1,
                }
            };
        });
	},

	tot_participant_enrollment: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.participant_group',
			args: {
				tot_participant_enrollment : frm.doc.tot_participant_enrollment
			},
			callback: function(r) {
				if (r.message){
					frappe.model.clear_table(frm.doc, 'participant_group');
					(r.message).forEach(element => {
						var c = frm.add_child("participant_group")
						c.participant_group=element.name
						c.participant_group_name=element.participant_group
						c.course_type=element.course_type
						c.course=element.course
						c.module_name=element.module_name
						c.module_code=element.module_code
						c.mode=element.mode
					})
					frm.refresh_field("participant_group")
				}
			}
		}),
		frappe.call({
			method: 'wsc.wsc.doctype.final_assignment_result.final_assignment_result.module',
			args: {
				course : frm.doc.programs
			},
			callback: function(r) {
				if (r.message){
					frappe.model.clear_table(frm.doc, 'modules');
					(r.message).forEach(element => {
						var c = frm.add_child("modules")
						c.course=element.course
						c.course_name=element.course_name
						c.course_code=element.course_code
						c.required=element.required
						c.modes=element.modes
						c.year_end_date=element.year_end_date
						c.is_disable=element.is_disable
					})
					frm.refresh_field("modules")
				}
			}
		})
	},


	get_participants : function(frm){
		frappe.call({
			
			method: 'wsc.wsc.doctype.final_result_declaration_tool.final_result_declaration_tool.get_participants',
			args: {
				frm:frm.doc
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participants')
					result.message['participant_list'].forEach(element => {
						var childTable = frm.add_child('participants')
						childTable.participant_id = element.participant_id
						childTable.participant_name = element.participant_name
						childTable.participant_attendance = element.participant_attendance
					})
				}
				frm.refresh()
				frm.refresh_field('participants')
				frm.set_value("no_of_participants", result.message["count"])
				frm.save()
			}
		})
	},
});
