// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant Group', {
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
	program:function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_group.participant_group.get_courses',
			args: {
				program_name : frm.doc.program
			},
			callback: function(result){
				frm.set_df_property('course', 'options', result.message) // courses in the program
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
	get_participants : function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_group.participant_group.get_participants',
			args:{
				academic_year : frm.doc.academic_year,
				academic_term : frm.doc.academic_term,
				participant_category : frm.doc.participant_category,
				program: frm.doc.program,
				course: frm.doc.course
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'participants')
					result.message.forEach(element => {
						var childTable = frm.add_child('participants')
						childTable.participant = element.student
						childTable.participant_name = element.student_name
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
