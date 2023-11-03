
frappe.ui.form.on('Course', {
	refresh: function(frm) {
		if (frm.doc.is_tot==0 && frm.doc.is_short_term_course=="No"){
			frm.remove_custom_button("Add to Programs","Action");
			frm.remove_custom_button("Add to Semester","Action");
			if (!cur_frm.doc.__islocal && (!frappe.user.has_role(["Student","Instructor"]) || frappe.user.has_role(["System Manager"]))) {
				frm.add_custom_button(__('Add to Semester'), function() {
					frm.trigger('add_course_to_semester')
				}, __('Action'));
			}
		}
		if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role('System Manager')){
		// if ((frappe.user.has_role("Student")) || (frappe.user.has_role("Instructor"))){
			frm.remove_custom_button("Add to Programs","Action");
			frm.remove_custom_button("Add to Semester","Action");
			frm.remove_custom_button("Add to ToT Course","Action");
		}
		if (frm.doc.is_tot==1 && frm.doc.is_short_term_course=="Yes"){
			frm.remove_custom_button("Add to Programs","Action");
			frm.remove_custom_button("Add to Semester","Action");
			if (!cur_frm.doc.__islocal && (!frappe.user.has_role(["Student","Instructor"]) || frappe.user.has_role(["System Manager"]))) {
				frm.add_custom_button(__('Add to ToT Course'), function() {
					frm.trigger('add_module_to_tot_course')
				}, __('Action'));
			}
		}
		if(frm.doc.is_tot==0 && frm.doc.is_short_term_course=="Yes"){
			frm.remove_custom_button("Add to Programs","Action");
			frm.remove_custom_button("Add to Semester","Action");
			if (!cur_frm.doc.__islocal && (!frappe.user.has_role(["Student","Instructor"]) || frappe.user.has_role(["System Manager"]))) {
				frm.add_custom_button(__('Add to Short Term Course'), function(){
					frm.trigger('add_to_short_term_course')
				}, __('Action'));
			}
		}
	},
	disable:function(frm){
        if(frm.doc.disable == 1){
        	frappe.call({
				method: "wsc.wsc.doctype.course.check_for_semester",
				args:{
					"course":frm.doc.name
				},
				callback: function(r) {
					if(r.message){
						// frappe.throw(__('Course <b>{0}</b> found in <b>{1}</b> to disable remove the course from semester.',[frm.doc.name, r.message]));
					}
				}
			});
        }
	},
	setup:function(frm){
		frm.remove_custom_button("Add to Programs","Action");
		frm.set_query("program", function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
	},
	total_marks:function(frm){
		(frm.doc.credit_distribution).forEach(data=>{
			var d = locals[data.doctype][data.name];
			d.total_marks=(frm.doc.total_marks*(d.weightage/100))
			refresh_field("total_marks", d.name, d.parentfield);	
		})
	},
	add_course_to_semester: function(frm) {
		
		get_semester_without_course(frm.doc.name).then(r => {
			if (r.message.length) {
				frappe.prompt([
					{
						fieldname: 'programs',
						label: __('Semester'),
						fieldtype: 'MultiSelectPills',
						get_data: function() {
							return r.message;
						}
					}
				],
				function(data) {
					frappe.call({
						
						method: 'wsc.wsc.validations.course.add_course_to_programs',
						args: {
							'course': frm.doc.name,
							'programs': data.programs,
						},
						callback: function(r) {
							if (!r.exc) {
								frm.reload_doc();
							}
						},
						freeze: true,
						freeze_message: __('...Adding Course to Semester')
					})
				}, __('Add Course to Semester'), __('Add'));
			} else {
				frappe.msgprint(__('This course is already added to the existing semester'));
			}
		});
	},
	add_module_to_tot_course: function(frm) {
		get_course_without_module(frm.doc.name).then(r => {
			if (r.message.length) {
				frappe.prompt([
					{
						fieldname: 'programs',
						label: __('Course'),
						fieldtype: 'MultiSelectPills',
						get_data: function() {
							return r.message;
						}
					}
				],
				function(data) {
					frappe.call({
						method: 'wsc.wsc.validations.course.add_module_to_tot_course',
						args: {
							'course': frm.doc.name,
							'programs': data.programs,
							'is_short_term_course':frm.doc.is_short_term_course,
							'is_tot':frm.doc.is_tot
						},
						callback: function(r) {
							if (!r.exc) {
								frm.reload_doc();
							}
						},
						freeze: true,
						freeze_message: __('...Adding Module to Tot Course')
					})
				}, __('Add Module to Course'), __('Add'));
			} else {
				frappe.msgprint(__('This Module is already added to the existing Course'));
			}
		});
	},
	add_to_short_term_course:function(frm){
		get_course_short_term(frm.doc.name).then(r=>{
			if (r.message.length) {
				frappe.prompt([
					{
						fieldname: 'programs',
						label: __('Course'),
						fieldtype: 'MultiSelectPills',
						get_data: function() {
							return r.message;
						}
					}
				],
				function(data) {
					frappe.call({
						method: 'wsc.wsc.validations.course.add_module_to_tot_course',
						args: {
							'course': frm.doc.name,
							'programs': data.programs,
							'is_short_term_course':frm.doc.is_short_term_course,
							'is_tot':frm.doc.is_tot
						},
						callback: function(r) {
							if (!r.exc) {
								frm.reload_doc();
							}
						},
						freeze: true,
						freeze_message: __('...Adding Module to Tot Course')
					})
				}, __('Add Module to Course'), __('Add'));
			} else {
				frappe.msgprint(__('This Module is already added to the existing Course'));
			}
		})

	}
});
let get_semester_without_course = function(course) {
	return frappe.call({
		args:{"course":course},
		method: 'wsc.wsc.validations.course.get_semesters_name',
		// /home/erpnext/frappe-bench/apps/wsc/wsc/wsc/validations/course.py
	});
}

let get_course_without_module = function(course) {
	return frappe.call({
		args:{"course":course},
		method: 'wsc.wsc.validations.course.get_course_name',
		// /home/erpnext/frappe-bench/apps/wsc/wsc/wsc/validations/course.py
	});
}

let get_course_short_term = function(course) {
	return frappe.call({
		args:{"course":course},
		method: 'wsc.wsc.validations.course.get_short_term_name',
		// /home/erpnext/frappe-bench/apps/wsc/wsc/wsc/validations/course.py
	});
}

// frappe.ui.form.on("Course Credit", "lectures", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
// 	d.total=((d.lectures||0)+(d.tutorials||0)+(d.practicals||0))
// 	refresh_field("total", d.name, d.parentfield);
// });
// frappe.ui.form.on("Course Credit", "tutorials", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
// 	d.total=((d.lectures||0)+(d.tutorials||0)+(d.practicals||0))
// 	refresh_field("total", d.name, d.parentfield);
// });
// frappe.ui.form.on("Course Credit", "practicals", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
// 	d.total=((d.lectures||0)+(d.tutorials||0)+(d.practicals||0))
// 	refresh_field("total", d.name, d.parentfield);
// });
// frappe.ui.form.on('Course Credit', {
// 	course_credit_add: function(frm, cdt, cdn){
// 		cur_frm.fields_dict['course_credit'].grid.wrapper.find('.grid-add-row').hide();
// 	}
// })
frappe.ui.form.on("Credit distribution List", "weightage", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.total_marks=(frm.doc.total_marks*(d.weightage/100))
	refresh_field("total_marks", d.name, d.parentfield);
});

frappe.ui.form.on('Credit distribution List', {
	credit_distribution_add: function(frm){
		frm.fields_dict['credit_distribution'].grid.get_field('assessment_criteria').get_query = function(doc){
			var assessment_criteria_list = [];
			$.each(doc.credit_distribution, function(idx, val){
				if (val.assessment_criteria) assessment_criteria_list.push(val.assessment_criteria);
			});
			return { filters: [['Assessment Criteria', 'name', 'not in', assessment_criteria_list]] };
		};
	}
});
// passing_marks
frappe.ui.form.on('Credit distribution List', {	
	passing_marks:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.credit_distribution.forEach(function(d)  { a = a+ d.passing_marks; });
	frm.set_value("passing_marks", a);
	refresh_field("passing_marks");
  },
  credit_distribution_remove:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.credit_distribution.forEach(function(d) { a += d.passing_marks; });
	frm.set_value("passing_marks", a);
	refresh_field("passing_marks");
	}
});