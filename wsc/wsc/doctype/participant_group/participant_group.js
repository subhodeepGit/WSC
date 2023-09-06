// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant Group', {
	setup: function(frm){
		frm.set_query("participant_id", function() {
			return {
				query: 'wsc.wsc.doctype.participant_group.participant_group.participant',
				filters:{"participant_enrollment_id":frm.doc.participant_enrollment_id}
				
			};
		});
	},
	refresh: function(frm) {
		frm.set_query('academic_term', function(){
			return{
				filters:{
					'academic_year' : frm.doc.academic_year
				}
			}
		})
		
		frm.set_query('program', function(){
			return{
				filters:{
					'is_tot': 1
				}
			}
		})
	},

	participant_enrollment_id: function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.participant_group.participant_group.get_enrollment_details',
			args: {
				enrollment_id : frm.doc.participant_enrollment_id
			},
			callback: function(result){
				frm.set_value("academic_year", result.message[0])
				frm.set_value("academic_term", result.message[1])
				frm.set_value("program", result.message[2])
				frm.set_value("semester", result.message[3])
				// frm.set_df_property('course', 'options', result.message[3])
			}
		})
	},
	course: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_group.participant_group.get_module_name',
			args:{
				module_id : frm.doc.course
			},
			callback: function(result){
				if(result.message){
					frm.set_value("module_name", result.message)
				}
			}
		})
	},
	semester: function(frm){
		frm.set_query("course", function() {
			return {
				query: 'wsc.wsc.validations.student_group.filter_courses',
				filters:{"semester":frm.doc.semester,"disable":0}
				
			};
		});
	},
	get_participants : function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_group.participant_group.get_participants',
			args:{
				enrollment_id : frm.doc.participant_enrollment_id
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participants')
					result.message.forEach(element => {
						var childTable = frm.add_child('participants')
						childTable.participant = element.participant
						childTable.participant_name = element.participant_name
					})
				}
				frm.refresh()
				frm.refresh_field('participants')
			}
		})
	},
});

frappe.ui.form.on('Instructor Table', {
	instructor_add: function(frm){
		frm.fields_dict['instructor'].grid.get_field('instructors').get_query = function(doc){
			var trainers = [];
			$.each(doc.instructor, function(idx, val){
				if (val.instructors) trainers.push(val.instructors);
			});
			return { filters: [['Instructor', 'name', 'not in', trainers]] };
		};
	}
});
