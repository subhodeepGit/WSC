frappe.ui.form.on('Instructor',{
    refresh: function(frm) {
        frm.remove_custom_button("As Examiner","Assessment Plan");
        frm.remove_custom_button("As Supervisor","Assessment Plan");
      
        // if (!frm.doc.__islocal && frappe.user.has_role(["System Manager"])) {
		// 	frm.add_custom_button(__("As Examiner"), function() {
		// 		frappe.new_doc("Course Assessment Plan", {
		// 			examiner: frm.doc.name
		// 		});
		// 	}, __("Course Assessment Plan"));
		// 	frm.add_custom_button(__("As Supervisor"), function() {
		// 		frappe.new_doc("Course Assessment Plan", {
		// 			supervisor: frm.doc.name
		// 		});
		// 	}, __("Course Assessment Plan"));
		// }
        if(frm.doc.docstatus == 0 && frm.doc.employee!=null) {
            // alert("Hello")
			frm.add_custom_button(__('Trainer Workload'), function() {
				frappe.route_options = {
					instructor: frm.doc.name,
                };
				frappe.set_route("query-report", "Instructor Workload");
            },
            );
        }

        frm.set_query("program","instructor_log", function(_doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                filters: {
                    "programs":d.programs
                }
            };
        });
        frm.set_query("programs","instructor_log", function(_doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                filters: {
                    "department":d.department,
                    "program_grade":d.course_type
                }
            };
        });
        frm.set_query("student_group","instructor_log", function(_doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                filters: {
                    "program":d.program,
                    "academic_term":d.academic_term
                }
            };
        });
    },

    //     if(frm.doc.docstatus > 0) {
	// 		frm.add_custom_button(__('Instructor Workload'), function() {
	// 			frappe.route_options = {
	// 				instructor: frm.doc.name,
    //             };
	// 			frappe.set_route("query-report", "Instructor Workload");
    //         },
    //         );
    //     }
    // },  
                
    employee:function(frm){
        if(!frm.doc.employee){
            frm.set_value('instructor_name', '')
            frm.set_value('department', '')
            frm.set_value('gender', '')
        }
     },

    create_user: function(frm) {
        if (!frm.doc.email_id_for_guest_trainers) {
			frappe.throw(__("Please enter Email ID for Guest Trainers"));
		}
		frappe.call({
			method: "wsc.wsc.validations.instructor.create_user",
			args: {
				trainer: frm.doc.name,
				email: frm.doc.email_id_for_guest_trainers
			},
			callback: function (r) {
				frm.set_value("email_id_for_guest_trainers", r.message);
			}
		});
	},



})