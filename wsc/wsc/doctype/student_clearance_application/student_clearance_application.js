// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
frappe.ui.form.on("Student Clearance Application", {
    onload: function(frm) {
        frm.set_df_property('departments_clearance_status', 'cannot_add_rows', true);
        frm.set_query("fees_id", "departments_clearance_status", function(doc) {
			return {
				filters: {
					'student': doc.student_id,
				}
			};
        });
	},
    refresh: function(frm) {
        if(frappe.user.has_role(["Student"]) && !frappe.user.has_role(["Administrator"])){
            frm.set_df_property('departments_clearance_status', 'read_only', 1);
            frm.set_df_property('clearance_type', 'read_only', 1)
            frm.set_df_property('user_disable_date', 'read_only', 1) 
        }
        frm.fields_dict.user_disable_date.datepicker.update({
            minDate: new Date(frappe.datetime.get_today()),
        });
		if(frm.doc.docstatus===0 && frm.doc.total_dues!=0) {
			frm.add_custom_button(__("Fees Entry"), function() {
				frm.events.make_fees_entry(frm);
			}, __('Create Dues'));
			frm.page.set_inner_btn_group_as_primary(__('Create Dues'));
		}
        var current_user=frappe.session.user;
        frappe.call({
            method: 'wsc.wsc.doctype.student_clearance_application.student_clearance_application.is_student',
            args: {
               user: current_user
            },
            callback: function(response) {
                if (response.message && response.message.is_student) {
                    // frm.set_df_property('clearance_type', 'hidden', 1);
                    // frm.set_df_property('departments_clearance_status', 'read_only', 1);
                    frm.refresh_field('departments_clearance_status');
                }
            }
        });
        
    },

    student_id: function(frm) {
        fetchStudentDetails(frm.doc.student_id, function(studentDetails) {
            processStudentDetails(frm, studentDetails);
        });
    },

    attrition_id: function(frm) {
        fetchAttritionStudentId(frm.doc.attrition_id, function(studentDetails) {
            processStudentDetails(frm, studentDetails);
        });
    },

    make_fees_entry: function(frm) {
		return frappe.call({
			method: "wsc.wsc.doctype.fees.get_fees_entry",
			args: {
				"dt": frm.doc.doctype,
				"dn": frm.doc.name,
                'student_id': frm.doc.student_id
			},
			callback: function(r) {
				var doc = frappe.model.sync(r.message);
				frappe.set_route("Form", doc[0].doctype, doc[0].name);
			}
		});
    },
    calculate_total_amount: function(frm) {
		var grand_total = 0;
		for(var i=0;i<frm.doc.departments_clearance_status.length;i++) {
			grand_total += frm.doc.departments_clearance_status[i].amount;
		}
        frm.set_value("total_dues", grand_total);
	}
});

frappe.ui.form.on("Departments Clearance Status", {
    amount: function(frm) {
		frm.trigger("calculate_total_amount");
	}
});

frappe.ui.form.on("Departments Clearance Status", "clearance_status", function(frm, cdt, cdn) {
    var cal=locals[cdt][cdn];
    if (cal.clearance_status!='Dues') {
        cal.amount = 0;
        cal.comment= '';
    }
    cur_frm.refresh_field ("departments_clearance_status");
    frm.trigger("calculate_total_amount");	 
});

function processStudentDetails(frm, r) {
    var studentData=r.message.current_student_attrition_data
    var currentEducation=r.message.current_education_data
    var userDisableDate=r.message.user_disable_date
    var departmentClearance=r.message.department_clearance
        if (currentEducation) {
            frappe.model.clear_table(frm.doc, 'current_education');
            (currentEducation).forEach(element => {
                        var c = frm.add_child("current_education")
                        c.programs=element.programs
                        c.semesters=element.semesters
                        c.academic_year=element.academic_year
                        c.academic_term=element.academic_term
                    });
                    frm.refresh_field("current_education")
            }
        if (studentData) {
            frm.set_value("student_id",studentData[0][0]);
        }
        if (userDisableDate) {
                frm.set_value("user_disable_date",userDisableDate);
                frappe.model.clear_table(frm.doc, 'departments_clearance_status');
                (departmentClearance).forEach(element => {
                    var c = frm.add_child("departments_clearance_status")
                    c.department=element.department
                    c.department_email_id=element.department_email_id
                });
                frm.refresh_field("departments_clearance_status")
        }else{
                frm.set_value("user_disable_date",'');
                frm.set_value("departments_clearance_status",'');
        }
    
}
function fetchStudentDetails(studentId, callback) {
    frappe.call({
        method: 'wsc.wsc.doctype.student_clearance_application.student_clearance_application.current_student_detail',
        args: {
            'student_id': studentId,
        },
        callback: callback
    });
}
function fetchAttritionStudentId(attritionId, callback) {
    frappe.call({
        method: 'wsc.wsc.doctype.student_clearance_application.student_clearance_application.get_attrition_student_id',
        args: {
            'attrition_id': attritionId,
        },
        callback: callback
    });
}