// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on("Hostel Attendance Tool", {
	refresh: function(frm) {
		frm.disable_save();
	},

	onload: function(frm) {
		frm.set_value("date", frappe.datetime.get_today());
		frm.set_query("department", function() {
			return {
				query: "wsc.wsc.doctype.room_allotment.room_allotment.test_query"
			};
		});
		frm.set_query("branch", function () {
			return {
				filters: [
					["Room Masters", "hostel_id", "=", frm.doc.department],
					["Room Masters", "validity", "=", "Approved"],
					["Room Masters", "status", "=", "Allotted"],
				]
			}
		});
		erpnext.employee_attendance_tool.load_employees(frm);
	},

	date: function(frm) {
		erpnext.employee_attendance_tool.load_employees(frm);
	},

	department: function(frm) {
		erpnext.employee_attendance_tool.load_employees(frm);
	},

	branch: function(frm) {
		erpnext.employee_attendance_tool.load_employees(frm);
	},

	// company: function(frm) {
	// 	erpnext.employee_attendance_tool.load_employees(frm);
	// }

});


erpnext.employee_attendance_tool = {
	load_employees: function(frm) {
		if(frm.doc.date) {
			frappe.call({
				method: "wsc.wsc.doctype.hostel_attendance_tool.hostel_attendance_tool.get_employees",
				args: {
					//input data
					date: frm.doc.date,
					department: frm.doc.department,
					branch: frm.doc.branch,
					//company: frm.doc.company
				},
				callback: function(r) {
					if(r.message['unmarked'].length > 0) {
						unhide_field('unarmked_attendance_section')
						if(!frm.employee_area) {
							frm.employee_area = $('<div>')
							.appendTo(frm.fields_dict.employees_html.wrapper);
						}
						frm.EmployeeSelector = new erpnext.EmployeeSelector(frm, frm.employee_area, r.message['unmarked'])
					}
					else{
						hide_field('unmarked_attendance_section')
					}

					if(r.message['marked'].length > 0) {

						unhide_field('marked_attendance_section')
						if(!frm.marked_employee_area) {
							frm.marked_employee_area = $('<div>')
								.appendTo(frm.fields_dict.marked_attendance_html.wrapper);
						}
						frm.marked_employee = new erpnext.MarkedEmployee(frm, frm.marked_employee_area, r.message['marked'])
					}
					else{
						hide_field('marked_attendance_section')
					}
				}
			});
		}
	}
}

erpnext.MarkedEmployee = class MarkedEmployee {
	constructor(frm, wrapper, employee) {
		this.wrapper = wrapper;
		this.frm = frm;
		this.make(frm, employee);
	}
	make(frm, employee) {
		var me = this;
		$(this.wrapper).empty();

		var row;
		$.each(employee, function(i, m) {
			var attendance_icon = "fa fa-check";
			var color_class = "";
			if(m.status == "Absent") {
				attendance_icon = "fa fa-check-empty"
				color_class = "text-muted";
			}
			else if(m.status == "Half Day") {
				attendance_icon = "fa fa-check-minus"
			}

			if (i===0 || i % 4===0) {
				row = $('<div class="row"></div>').appendTo(me.wrapper);
			}

			$(repl('<div class="col-sm-3 %(color_class)s">\
				<label class="marked-employee-label"><span class="%(icon)s"></span>\
				%(employee)s</label>\
				</div>', {
					employee: m.student_name,
					icon: attendance_icon,
					color_class: color_class
				})).appendTo(row);
		});
	}
};


erpnext.EmployeeSelector = class EmployeeSelector {
	constructor(frm, wrapper, employee) {
		this.wrapper = wrapper;
		this.frm = frm;
		this.make(frm, employee);
	}
	make(frm, employee) {
		var me = this;

		$(this.wrapper).empty();
		var employee_toolbar = $('<div class="col-sm-12 top-toolbar">\
			<button class="btn btn-default btn-add btn-xs"></button>\
			<button class="btn btn-xs btn-default btn-remove"></button>\
			</div>').appendTo($(this.wrapper));

		var mark_employee_toolbar = $('<div class="col-sm-12 bottom-toolbar">\
			<button class="btn btn-primary btn-mark-present btn-xs"></button>\
			\
			\
			<button class="btn btn-danger btn-mark-absent btn-xs"></button>\
			</div>');

		employee_toolbar.find(".btn-add")
			.html(__('Check all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if(!$(check).is(":checked")) {
						check.checked = true;
					}
				});
			});

		employee_toolbar.find(".btn-remove")
			.html(__('Uncheck all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if($(check).is(":checked")) {
						check.checked = false;
					}
				});
			});

		mark_employee_toolbar.find(".btn-mark-present")
			.html(__('Mark Present'))
			.on("click", function() {
				var employee_present = [];
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if($(check).is(":checked")) {
						//output Data data
						// alert(JSON.stringify(employee[i]));
						employee_present.push(employee[i]);
						//alert(employee[i]);
					}
				});
				frappe.call({
					method: "wsc.wsc.doctype.hostel_attendance_tool.hostel_attendance_tool.mark_employee_attendance",
					args:{
						"employee_list":employee_present,
						"status":"Present",
						"date":frm.doc.date,
						//"company":frm.doc.company
					},

					callback: function(r) {
						erpnext.employee_attendance_tool.load_employees(frm);

					}
				});
			});

		mark_employee_toolbar.find(".btn-mark-absent")
			.html(__('Mark Absent'))
			.on("click", function() {
				var employee_absent = [];
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if($(check).is(":checked")) {
						employee_absent.push(employee[i]);
					}
				});
				frappe.call({
					method: "wsc.wsc.doctype.hostel_attendance_tool.hostel_attendance_tool.mark_employee_attendance",
					args:{
						"employee_list":employee_absent,
						"status":"Absent",
						"date":frm.doc.date,
						//"company":frm.doc.company
					},

					callback: function(r) {
						erpnext.employee_attendance_tool.load_employees(frm);

					}
				});
			});


		// mark_employee_toolbar.find(".btn-mark-half-day")
		// 	.html(__('Mark Half Day'))
		// 	.on("click", function() {
		// 		var employee_half_day = [];
		// 		$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
		// 			if($(check).is(":checked")) {
		// 				employee_half_day.push(employee[i]);
		// 			}
		// 		});
		// 		frappe.call({
		// 			method: "wsc.wsc.doctype.hostel_attendance_tool.hostel_attendance_tool.mark_employee_attendance",
		// 			args:{
		// 				"employee_list":employee_half_day,
		// 				"status":"Half Day",
		// 				"date":frm.doc.date,
		// 				"company":frm.doc.company
		// 			},

		// 			callback: function(r) {
		// 				erpnext.employee_attendance_tool.load_employees(frm);

		// 			}
		// 		});
		// 	});


		// mark_employee_toolbar.find(".btn-mark-work-from-home")
		// 	.html(__('Mark Work From Home'))
		// 	.on("click", function() {
		// 		var employee_work_from_home = [];
		// 		$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
		// 			if($(check).is(":checked")) {
		// 				employee_work_from_home.push(employee[i]);
		// 			}
		// 		});
		// 		frappe.call({
		// 			method: "wsc.wsc.doctype.hostel_attendance_tool.hostel_attendance_tool.mark_employee_attendance",
		// 			args:{
		// 				"employee_list":employee_work_from_home,
		// 				"status":"Work From Home",
		// 				"date":frm.doc.date,
		// 				"company":frm.doc.company
		// 			},

		// 			callback: function(r) {
		// 				erpnext.employee_attendance_tool.load_employees(frm);

		// 			}
		// 		});
		// 	});

		var row;
		$.each(employee, function(i, m) {
			if (i===0 || (i % 4) === 0) {
				row = $('<div class="row"></div>').appendTo(me.wrapper);
			}

			$(repl('<div class="col-sm-3 unmarked-employee-checkbox">\
				<div class="checkbox">\
				<label><input type="checkbox" class="employee-check" employee="%(employee)s"/>\
				%(employee)s</label>\
				</div></div>', {employee: m.student_name})).appendTo(row);
		});

		mark_employee_toolbar.appendTo($(this.wrapper));
	}
};
