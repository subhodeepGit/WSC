// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Students Attendance Tool', {
// 	// refresh: function(frm) {

// 	// }
// });
// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.provide("wsc");

frappe.ui.form.on('Students Attendance Tool', {
	setup: (frm) => {
		frm.students_area = $('<div>')
			.appendTo(frm.fields_dict.students_html.wrapper);
	},
	onload: function(frm) {
		frm.set_query("student_group", function() {
			return {
				"filters": {
					"group_based_on": frm.doc.group_based_on,
					"disabled": 0
				}
			};
		});
	},

	refresh: function(frm) {
		if (frappe.route_options) {
			frm.set_value("based_on", frappe.route_options.based_on);
			frm.set_value("student_group", frappe.route_options.student_group);
			frm.set_value("course_schedule", frappe.route_options.course_schedule);
			frappe.route_options = null;
		}
		frm.disable_save();
	},

	based_on: function(frm) {
		if (frm.doc.based_on == "Student Group") {
			frm.set_value("course_schedule", "");
		} else {
			frm.set_value("student_group", "");
		}
		if (frm.doc.based_on == "Course Schedule"){
			frm.set_query("course_schedule", function () {
				return {
					filters: {
						"schedule_date":frm.doc.date
					}
				}
			});
		}
	},

	sg: function(frm) {
		if(frm.doc.based_on == "Student Group"){
		if ((frm.doc.student_group && frm.doc.date) || (frm.doc.course_schedule && frm.doc.date)) {
			frm.students_area.find('.student-attendance-checks').html(`<div style='padding: 2rem 0'>Fetching...</div>`);
			var method = "wsc.wsc.doctype.students_attendance_tool.students_attendance_tool.get_student_attendance_records";

			frappe.call({
				method: method,
				args: {
					based_on: frm.doc.based_on,
					student_group: frm.doc.student_group,
					date: frm.doc.date,
					course_schedule: frm.doc.course_schedule
				},
				callback: function(r) {
					frm.events.get_students(frm, r.message);
				}
			})
		}}
	},

	cs: function(frm) {
		if(frm.doc.based_on == "Course Schedule"){
		if ((frm.doc.student_group && frm.doc.date) || (frm.doc.course_schedule && frm.doc.date)) {
			frm.students_area.find('.student-attendance-checks').html(`<div style='padding: 2rem 0'>Fetching...</div>`);
			var method = "wsc.wsc.doctype.students_attendance_tool.students_attendance_tool.get_student_attendance_records";

			frappe.call({
				method: method,
				args: {
					based_on: frm.doc.based_on,
					student_group: frm.doc.student_group,
					date: frm.doc.date,
					course_schedule: frm.doc.course_schedule
				},
				callback: function(r) {
					frm.events.get_students(frm, r.message);
				}
			})
		}}
	},

	date: function(frm) {
		frm.set_value('course_schedule',"");
		if (frm.doc.date > frappe.datetime.get_today())
			frappe.throw(__("Cannot mark attendance for future dates."));
		if (frm.doc.based_on == "Student Group") {
			frm.trigger("sg");
		} else if (frm.doc.based_on == "Course Schedule") {
			frm.trigger("cs")
		}
	},

	course_schedule: function(frm) {
		frm.trigger("cs");
	},

	get_students: function(frm, students) {
		students = students || [];
		frm.students_editor = new wsc.StudentsEditor(frm, frm.students_area, students);
	}
});


wsc.StudentsEditor = class StudentsEditor {
	constructor(frm, wrapper, students) {
		this.wrapper = wrapper;
		this.frm = frm;
		if(students.length > 0) {
			this.make(frm, students);
		} else {
			this.show_empty_state();
		}
	}
	make(frm, students) {
		var me = this;

		$(this.wrapper).empty();
		var student_toolbar = $('<p>\
			<button class="btn btn-default btn-add btn-xs" style="margin-right: 5px;"></button>\
			<button class="btn btn-xs btn-default btn-remove" style="margin-right: 5px;"></button>\
			<button class="btn btn-default btn-primary btn-mark-att btn-xs"></button></p>').appendTo($(this.wrapper));

		student_toolbar.find(".btn-add")
			.html(__('Check all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if (!$(check).prop("disabled")) {
						check.checked = true;
					}
				});
			});

		student_toolbar.find(".btn-remove")
			.html(__('Uncheck all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if (!$(check).prop("disabled")) {
						check.checked = false;
					}
				});
			});

		student_toolbar.find(".btn-mark-att")
			.html(__('Mark Attendance'))
			.on("click", function() {
				$(me.wrapper.find(".btn-mark-att")).attr("disabled", true);
				var studs = [];
				$(me.wrapper.find('input[type="checkbox"]')).each(function(i, check) {
					var $check = $(check);
					studs.push({
						student: $check.data().student,
						student_name: $check.data().student_name,
						roll_no: $check.data().roll_no,
						group_roll_number: $check.data().group_roll_number,
						leave_status: $check.data().leave_status,
						disabled: $check.prop("disabled"),
						checked: $check.is(":checked"),
					});
				});
				var students_present = studs.filter(function(stud) {
					return !stud.disabled && stud.checked;
				});

				var students_absent = studs.filter(function(stud) {
					return !stud.disabled && !stud.checked && (stud.leave_status=="Sent for Approval to Class Advisor" || stud.leave_status=="Sent for Approval to Course Manager" || stud.leave_status=="");
				});

				var students_on_leave = studs.filter(function(stud) {
					return !stud.disabled && !stud.checked && stud.leave_status=="Approved";
				});
				// console.log(students_present);
				// console.log(students_absent);
				// console.log(students_on_leave);
				frappe.confirm(__("Do you want to update attendance? <br> Present: {0} <br> Absent: {1} <br> On Leave: {2} ",
					[students_present.length, students_absent.length, students_on_leave.length]),
					function() {	//ifyes
						if(!frappe.request.ajax_count) {
							frappe.call({
								method: "wsc.wsc.doctype.students_attendance_tool.students_attendance_tool.mark_attendance",
								freeze: true,
								freeze_message: __("Marking attendance"),
								args: {
									"students_present": students_present,
									"students_absent": students_absent,
									"students_on_leave": students_on_leave,
									"student_group": frm.doc.student_group,
									"course_schedule": frm.doc.course_schedule,
									"building": frm.doc.hostel,
									"hostel_category": frm.doc.hostel_room,
									"attendance_for":frm.doc.based_on=="Hostel"?"Hosteler":"",
									"date": frm.doc.date
								},
								callback: function(r) {
									$(me.wrapper.find(".btn-mark-att")).attr("disabled", false);
									frm.trigger("student_group");
									setTimeout(function(){
										window.location.reload();
									 }, 5000);
								}
							});
						}
					},
					function() {	//ifno
						$(me.wrapper.find(".btn-mark-att")).attr("disabled", false);
					}
				);
			});
		$('<div class="col-sm-12"><div class="checkbox"><table class="table table-bordered table-sm"><tr class="abc"><th width="5%" style="text-align: center"></th><th width="10%" style="text-align: center">Group Roll No.</th><th width="10%" style="text-align: center">Roll No.</th><th width="15%" style="text-align: center">Student Name</th><th width="15%" style="text-align: center">Student ID</th><th width="15%" style="text-align: center">Leave Status</th><th width="15%" style="text-align: center">Leave Type</th><th width="15%" style="text-align: center">Leave Application ID</th></tr></table></div></div>').appendTo($(this.wrapper));
		var htmls = students.map(function(student) {
			return frappe.render_template("students_data_table", {
				student: student.student,
				roll_no: student.roll_no,
				student_name: student.student_name,
				group_roll_number: student.group_roll_number,
				status: student.status,
				leave_status: student.leave_status,
				reason_for_leave: student.reason_for_leave,
				leave_app_id: student.leave_app_id
			})

		});
		$(htmls.join("")).appendTo(me.wrapper);
	}

	show_empty_state() {
		$(this.wrapper).html(
			`<div class="text-center text-muted" style="line-height: 100px;">
				${__("No Students in")} ${this.frm.doc.student_group}
			</div>`
		);
	}
};

