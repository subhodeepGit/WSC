// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt


frappe.ui.form.on('Class Scheduling Tool', {
	setup(frm) {
		frm.add_fetch('student_group', 'program', 'program');
		frm.set_df_property('instructor', 'hidden', 1);
		frm.add_fetch('student_group', 'course', 'course');
		frm.add_fetch('student_group', 'academic_year', 'academic_year');
		frm.add_fetch('student_group', 'academic_term', 'academic_term');
		frm.set_query("instructor", function() {
			return {
				query: 'wsc.wsc.doctype.class_scheduling_tool.class_scheduling_tool.get_instructor',
				filters: {
					"course":frm.doc.course,
					"academic_term":frm.doc.academic_term,
					"school_house":frm.doc.school_house
				}
			};
		});
	
		// frm.fields_dict['additional_trainer'].grid.get_field('instructor').get_query = function(doc){
		// 	var courses_list = [];
		// 	$.each(doc.additional_trainer, function(idx, val){
		// 		if (val.instructor) courses_list.push(val.instructor);
		// 	});
		// 	return { filters: [['Instructor', 'name', 'not in', courses_list]] };
		// };
		// frm.set_query("instructor", "additional_trainer", function() {
		frm.fields_dict['additional_trainer'].grid.get_field('instructor').get_query = function(doc){
		var courses_list = [];
		$.each(doc.additional_trainer, function(idx, val){
			if (val.instructor) courses_list.push(val.instructor);
		});
		// alert(courses_list)
        return {
			query: 'wsc.wsc.doctype.class_scheduling_tool.class_scheduling_tool.get_instructor',
			filters:{
					"course":frm.doc.course,
					"student_group":frm.doc.student_group,
			}
		};
	};
		// courses_add: function(frm){
		// 	frm.fields_dict['additional_trainer'].grid.get_field('instructor').get_query = function(doc){
		// 		var courses_list = [];
		// 		$.each(doc.additional_trainer, function(idx, val){
		// 			if (val.instructor) courses_list.push(val.instructor);
		// 		});
		// 		return { filters: [['Instructor', 'name', 'not in', courses_list]] };
		// 	};
		// }
		frm.set_query("course", function() {
			return {
				query: 'wsc.wsc.doctype.class_scheduling_tool.class_scheduling_tool.get_course',
				filters: {
					"program":frm.doc.program
				}
			};
		});
	},
	refresh(frm) {
		frm.disable_save();
		frm.trigger("render_days");
		frm.page.set_primary_action(__('Schedule Classes'), () => {
			frappe.dom.freeze(__("Scheduling..."));
			frm.call('schedule_course', { days: frm.days.get_checked_options() })
				.fail(() => {
					frappe.dom.unfreeze();
					frappe.msgprint(__("Class Scheduling Failed"));
				})
				.then(r => {
					frappe.dom.unfreeze();
					if (!r.message) {
						frappe.throw(__('There were errors creating Class Schedule'));
					}
					const { course_schedules } = r.message;
					if (course_schedules) {
						const course_schedules_html = course_schedules.map(c => `
							<tr>
								<td><a href="/app/course-schedule/${c.name}">${c.name}</a></td>
								<td>${c.schedule_date}</td>
							</tr>
						`).join('');

						const html = `
							<table class="table table-bordered">
								<caption>${__('Following class schedules were created')}</caption>
								<thead><tr><th>${__("Course")}</th><th>${__("Date")}</th></tr></thead>
								<tbody>
									${course_schedules_html}
								</tbody>
							</table>
						`;

						frappe.msgprint(html);
					}
				});
		});
	},
	//Code for Additional instructor dialogue box popup
	// instructor:function(frm){
	// 	frappe.confirm(
	// 		'Do You Want To Add <b>Additional Trainers</b>?',
	// 		function(){
	// 			frm.trigger("additional_instructor")
	// 		},
	// 		function(){
	// 			// window.close();
	// 		}
	// 	)
	// },
	// additional_instructor:function(frm){
	// 	var d = new frappe.ui.Dialog({
	// 		title: __('Additional Trainers'),
	// 		fields:[{fieldtype:'Table', fieldname: 'instructor_list',label:"Trainer List",
	// 		fields: [
	// 			{
	// 				"label" : "Trainer",
	// 				"fieldname": "instructor",
	// 				"fieldtype": "Link",
	// 				"options":"Instructor",
	// 				"in_list_view":1,
	// 				get_query: function () {
	// 					return {
	// 						query: 'wsc.wsc.doctype.course_schedule.get_instructor',
    //             			filters:{"course":frm.doc.course,"student_group":frm.doc.student_group}
	// 					}
	// 				},
	// 				onchange: function() {
	// 					Object.values(d.get_value('instructor_list')).forEach(i=>{
	// 						frappe.db.get_value('Instructor', {name: i.instructor}, ['instructor_name'], (r) => {
	// 							i['instructor_name']=r.instructor_name
	// 							d.fields_dict.instructor_list.grid.refresh();
	// 						})
	// 						})
	// 						d.fields_dict.instructor_list.grid.refresh();
	// 				}
	// 			},
	// 			{
	// 				"label" : "Trainer Name",
	// 				"fieldname": "instructor_name",
	// 				"fieldtype": "Data",
	// 				"in_list_view":1
	// 			}
	// 		]
	// 		}],
	// 		primary_action: function() {
	// 			(frm.doc)["additional_instructors"]=d.get_values();
	// 			d.hide();
	// 		},
	// 		primary_action_label: __('Add')
	// 	});
	// 	d.show();
	// },
	//end//

	render_days: function(frm) {
		const days_html = $('<div class="days-editor">').appendTo(
			frm.fields_dict.days_html.wrapper
		);

		if (!frm.days) {
			frm.days = frappe.ui.form.make_control({
				parent: days_html,
				df: {
					fieldname: "days",
					fieldtype: "MultiCheck",
					select_all: true,
					columns: 4,
					options: [
						{
							label: __("Monday"),
							value: "Monday",
							checked: 0,
						},
						{
							label: __("Tuesday"),
							value: "Tuesday",
							checked: 0,
						},
						{
							label: __("Wednesday"),
							value: "Wednesday",
							checked: 0,
						},
						{
							label: __("Thursday"),
							value: "Thursday",
							checked: 0,
						},
						{
							label: __("Friday"),
							value: "Friday",
							checked: 0,
						},
						{
							label: __("Saturday"),
							value: "Saturday",
							checked: 0,
						},
						{
							label: __("Sunday"),
							value: "Sunday",
							checked: 0,
						},
					],
				},
				render_input: true,
			});
		}
	}
});
// frappe.ui.form.on("Exam Centre Preference" , "center_name" , function(frm , cdt , cdn){
// 	var d = locals[cdt][cdn];
// 	var a = 0;
// 	// if (d.programs && frappe.user.has_role(["Student Applicant"])){
// 	if (d.center_name){
// 		a=frm.doc.exam_center_locations.length;
// 		// frm.set_value("count_programs", a);
// 		if(a>=3){
// 			frm.set_df_property('exam_center_locations', 'cannot_add_rows', true);
// 			frm.set_df_property('exam_center_locations', 'cannot_delete_rows', true);
// 			// frm.set_df_property('program_priority', 'cannot_insert_below', true);
// 		}
// 	}
// })
frappe.ui.form.on("Additional Instructor", "instructor", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
   
    frappe.model.set_value(cdt, cdn, "instructor_name",'');
    if (!frm.doc.student_group){
        frappe.msgprint("Please Fill Student Group First")
        d.instructor=''
    }

    if (d.instructor){
        frappe.call({
            method: "wsc.wsc.doctype.class_scheduling_tool.class_scheduling_tool.get_trainer_list",
            args: {
                instructor:d.instructor,
            },
            callback: function(r) { 
                if (r.message && frm.doc.instructor==undefined){
                    console.log(r.message);
                        frm.set_value("instructor",r.message['name'])
                        frm.set_value("instructor_name",r.message['instructor_name'])
                    frappe.model.set_value(cdt, cdn, "instructor", r.message['name']);
                    frappe.model.set_value(cdt, cdn, "instructor_name", r.message['instructor_name']);
                }
                if (r.message && frm.doc.instructor){
                    console.log(r.message);
                    frappe.model.set_value(cdt, cdn, "instructor", r.message['name']);
                    frappe.model.set_value(cdt, cdn, "instructor_name", r.message['instructor_name']);
                }
            } 
        }); 
    }
});
cur_frm.add_fetch('student_group','class_room','room');
	