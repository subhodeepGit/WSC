// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Class Schedule', {
	setup: function(frm) {
		frm.set_query('participant_group_id', function(){
			return{
				filters:{
					"disabled":0
				}
			}
		}),
		frm.set_query('course_id', function(){
			return{
				filters:{
					'is_tot' : 1
				}
			}
		})
	},
	semester: function(frm){
		frm.set_query("module_id", function() {
			return {
				query: 'wsc.wsc.validations.student_group.filter_courses',
				filters:{"semester":frm.doc.semester,"disable":0}
				
			};
		});
	},
	refresh:function(frm){
		frm.set_query("trainers",function(){
			return{
				query: 'wsc.wsc.doctype.tot_class_schedule.tot_class_schedule.get_instructor',
				filters:{
					"academic_year":frm.doc.academic_year,
					"course":frm.doc.course_id,
					"semester":frm.doc.semester
				}
			};
		});
	}
});
