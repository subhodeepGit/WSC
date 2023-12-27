// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant Attendance Tool', {
	setup: function(frm){
		frappe.call({
            method: "wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.trainer",
            callback: function(r) { 
                if (r.message){
                    frm.set_value("instructor_id",r.message)
                }
            } 
        });    	
		frm.set_query("instructor_id", function() {
			return {
				query: 'wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.instructor',
				filters:{"participant_group_id":frm.doc.participant_group}
				
			};
		});
		frm.set_df_property('participants', 'cannot_add_rows', true);
        frm.set_df_property('participants', 'cannot_delete_rows', true);
		frm.set_query('select_class_schedule', function(){
			return{
				filters:{
					'participant_group_id' : frm.doc.participant_group,
					'course_id':frm.doc.select_course,
					'module_id':frm.doc.select_module,
					'attendance_taken':0
				}	
			}
		});
		frm.set_query('participant_group', function(){
			return{
				filters:{
					'disabled' : 0,
				}	
			}
		})
	},
	participant_group: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.get_details',
			args: {
				participant_group_id : frm.doc.participant_group
			},
			callback: function(result){
				console.log(result)
				frm.set_value("academic_year", result.message[0]) // academic year
				frm.set_value("academic_term", result.message[1]) // acadmic term
				frm.set_value("select_course", result.message[2]) // course
				frm.set_value("select_module", result.message[3]) // module
				// frm.set_df_property('instructor_id', 'options', result.message[4]) // instructor_id
				// frm.set_df_property('date', 'options', result.message[5]) // date
			}
		})
		frm.trigger("get_participants");
		frappe.call({
			"method": "wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.get_classes",
			args:{
				participant_group:frm.doc.participant_group
			},
			callback: function(r) {
				if (r.message){
					frappe.model.clear_table(frm.doc, 'classes');
					(r.message).forEach(element => {
						var c = frm.add_child("classes")
						c.scheduled_date=element.scheduled_date
						c.room_name=element.room_name
						c.room_number=element.room_number
						c.from_time=element.from_time
						c.to_time=element.to_time
						c.duration=element.duration
						c.re_scheduled=element.re_scheduled
						c.is_scheduled=element.is_scheduled
						c.is_canceled=element.is_canceled
						c.tot_class_schedule=element.tot_class_schedule
					});
					frm.refresh_field("classes")
				}
			}
		})
	},
	get_participants: function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.participant_attendance_tool.participant_attendance_tool.get_participants',
			args: {
				participant_group_id: frm.doc.participant_group
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participants')
					result.message.forEach(element => {
						var childTable = frm.add_child('participants')
						childTable.participant_id = element.participant
						childTable.participant_name = element.participant_name
					})
				} else {
					frappe.throw("Please select a participant group!!")
				}
				frm.refresh()
				frm.refresh_field('participants')
			}
		})
	},
});
