frappe.ui.form.on('Student Attendance Tool', {
    refresh:function(frm){
        frm.set_df_property('based_on', 'options', ['Student Group', 'Course Schedule', 'Hostel']);
        frm.set_df_property('date', 'depends_on','eval:(["Student Group","Hostel"].includes(doc.based_on))');
		// frm.set_df_property('attendance', 'depends_on','eval: (doc.course_schedule || (doc.student_group && doc.date) || (doc.building && doc.date))');
		frm.set_df_property('attendance', 'depends_on','eval: (doc.course_schedule || (doc.student_group && doc.date))');
    },
    based_on:function(frm){
		
        if (frm.doc.based_on=="Hostel" && frm.doc.date){
			frm.set_value("course_schedule", "");
			frm.set_value("student_group", "");
            frm.trigger("hostel_fields");
        }
		if (frm.doc.based_on=="Course Schedule"){
			var dialog = new frappe.ui.Dialog({
				fields: [
					{
						"label" : "Date",
                        "fieldname": "course_schedule_date",
                        "fieldtype": "Date",
                        "reqd":1,
					}
				],
				primary_action: function() {
					var data = dialog.get_values();
						frm.set_query("course_schedule", function () {
							return {
								filters: {
									"schedule_date":data.course_schedule_date
								}
							}
						});
					dialog.hide(); 
				}
			});
			dialog.show();	
		}
    },
    hostel_fields:function(frm){
        var dialog = new frappe.ui.Dialog({
			title: __('Hostel Details'),
			fields: [
				{
					"label" : "Hostel",
					"fieldname": "hostel",
					"fieldtype": "Link",
					"options": "Hostel Masters"
				},
				{
					"label" : "Hostel Room",
					"fieldname": "hostel_room",
					"fieldtype": "Link",
					"options": "Room Masters",
					get_query: function () {
						return {
							filters:{
								"hostel_id":dialog.get_value("hostel"),
								"validity":"Approved",
								"status":"Allotted"
							}
						}						
					}
				},
			],
			primary_action: function() {
				var data = dialog.get_values();
				frm.doc.hostel=dialog.get_value("hostel");
				frm.doc.hostel_room=dialog.get_value("hostel_room");
                if (data.hostel_room) {
					frm.trigger("hostel_room")
                    dialog.hide();
                }
			},
			primary_action_label: __('Get Students')
		});
		dialog.show();
    },
	hostel_room:function(frm){		
		var method = "wsc.wsc.validations.student_attendance_tool.get_employees";
		frm.set_df_property('attendance', 'depends_on','eval: (doc.course_schedule || (doc.student_group && doc.date) || doc.date)');
		frappe.call({
			method: method,
			args: {
					date: frm.doc.date,
					department: frm.doc.hostel,
					branch: frm.doc.hostel_room,
			},
			callback: function(r) {
				if (!frm.students_area) {
					frm.students_area = $('<div>')
						.appendTo(frm.fields_dict.students_html.wrapper);
				}
				var students = r.message || [];
				frm.students_editor = new education.StudentsEditor(frm, frm.students_area, students);
			}
		})
	},
    date:function(frm){
        if (frm.doc.based_on=="Hostel" && frm.doc.date){
            frm.trigger("hostel_fields")
        }
    },
    
    student_group:function(frm){
        if (frm.doc.based_on=="Student Group" && !frm.doc.date){
            // if (frm.doc.group_based_on == 'Batch' || frm.doc.group_based_on == 'Course'){
			if (frm.doc.group_based_on == 'Course' & frm.doc.student_group != Null){
	            var dialog = new frappe.ui.Dialog({
					fields: [
		                {
							"label" : "Course Schedule",
							"fieldname": "course_schedule",
							"fieldtype": "Link",
							"options" : "Course Schedule",
							"reqd":1,
							get_query: function () {
							   if (frm.doc.student_group){
									return {
										filters:{"student_group":frm.doc.student_group}
									}
								}
						    }
						}
					],
					primary_action: function() {
						var data = dialog.get_values();
						frappe.db.get_value('Course Schedule', {'name':data.course_schedule},'schedule_date', resp => {
			        		frm.set_value('date', resp.schedule_date)
			        	});
		                dialog.hide(); 
					}
				});
				dialog.show();
			}
        }
    }
});


education.StudentsEditor = Class.extend({
	init: function(frm, wrapper, students) {
		this.wrapper = wrapper;
		this.frm = frm;
		if(students.length > 0) {
			this.make(frm, students);
		} else {
			this.show_empty_state();
		}
	},
	make: function(frm, students) {
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
						disabled: $check.prop("disabled"),
						checked: $check.is(":checked")
					});
					
				});
				var students_present = studs.filter(function(stud) {
					return !stud.disabled && stud.checked;
				});

				var students_absent = studs.filter(function(stud) {
					return !stud.disabled && !stud.checked;
				});

				frappe.confirm(__("Do you want to update attendance? <br> Present: {0} <br> Absent: {1}",
					[students_present.length, students_absent.length]),
					function() {	//ifyes
						if(!frappe.request.ajax_count) {
							frappe.call({
								method: "education.education.api.mark_attendance",
								freeze: true,
								freeze_message: __("Marking attendance"),
								args: {
									"students_present": students_present,
									"students_absent": students_absent,
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
								}
							});
						}
					},
					function() {	//ifno
						$(me.wrapper.find(".btn-mark-att")).attr("disabled", false);
					}
				);
			});

		var htmls = students.map(function(student) {
			return frappe.render_template("student_button_custom", {
				student: student.student,
				roll_no: student.roll_no,
				student_name: student.student_name,
				group_roll_number: student.group_roll_number,
				status: student.status
			})
			
		});
		$(htmls.join("")).appendTo(me.wrapper);
	},

	show_empty_state: function() {
		$(this.wrapper).html(
			`<div class="text-center text-muted" style="line-height: 100px;">
				${__("No Students in")} ${this.frm.doc.student_group}
			</div>`
		);
	}
});