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
		}),
		
		frm.set_query('program', function(){
			return{
				filters:{
					'is_tot': 1
				}
			}
		}),
		frm.set_query('participant_enrollment_id', function(){
			return{
				filters:{
					'docstatus': 1
				}
			}
		}),
		frm.set_df_property('participants', 'cannot_add_rows', true);
		frm.set_df_property('participants', 'cannot_delete_rows', true);
		frm.set_df_property('classes', 'cannot_delete_rows', true);

		// frm.set_query('course', function(){
		// 	return{
		// 		filters:{
		// 			'name': frm.doc.program
		// 		}
		// 	}
		// })

		// frm.set_query('course', function(){
		// 	return{
		// 		filters:{
		// 			'is_tot': 1
		// 		}
		// 	}
		// })
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
				// frm.save();
			}
		})
	},
});

// frappe.ui.form.on('Instructor Table', {
// 	instructor_add: function(frm){
// 		frm.fields_dict['instructor'].grid.get_field('instructors').get_query = function(doc){
// 			var trainers = [];
// 			$.each(doc.instructor, function(idx, val){
// 				if (val.instructors) trainers.push(val.instructors);
// 			});
// 			return { filters: [['Instructor', 'name', 'not in', trainers]] };
// 		};
// 	}
// });

frappe.ui.form.on('Instructor Table', {
	instructor_add: function(frm, cdt, cdn){
		var course_options="\n"
		var instructor_options=''
		var semesters=[]
		if (frm.doc.group_based_on == 'Course'){
			course_options=frm.doc.course
			semesters.push(frm.doc.program)
		}
		var d = new frappe.ui.Dialog({
			title: __('Add Trainer'),
			fields: [
				{
					"label" : "Course",
					"fieldname": "course",
					"fieldtype": "Select",
					"reqd":1,
					"options": course_options,
					onchange: function() {
						var course=d.get_value('course');
						d.set_value("instructor","");
						if (course){
							frappe.call({
								method: 'wsc.wsc.validations.student_group.get_instructor',
								args: {
									filters:
										{
											academic_year: frm.doc.academic_year,
											course:course,
											semesters:semesters,
											apply_semester_filter:frm.doc.group_based_on=="Combined Course"?0:1
										}
								},
								callback: function(resp){
									if(resp.message){
										instructor_options=resp.message
										d.set_df_property('instructor', 'options', instructor_options);
									}
								}
							})
						}
					}
				},
				{
					"label" : "Trainer",
					"fieldname": "instructor",
					"fieldtype": "Select",
					"reqd":1,
					"options": instructor_options
				}
			],
			primary_action: function() {
				var values = d.get_values();
				console.log(cdt, cdn)
				var row = frappe.get_doc(cdt, cdn);
				console.log(row)
				row.instructors=values.instructor
				frappe.db.get_value("Instructor",{"name":values.instructor},['instructor_name'], resp =>{
					row.instructor_name=resp.instructor_name
					frm.refresh_field('instructor')
				})
				frm.refresh_field('instructor')
				d.hide();
			},
			primary_action_label: __('Add Values')
		});
		d.show();
	}
});
