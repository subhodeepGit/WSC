// Copyright (c) 2022, SOUL LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('Upload Material', {
	refresh: function(frm) {
		frm.set_query("emp_code", function() {
			return {
				query: "wsc.wsc.doctype.upload_material.upload_material.Teacher_query"
			};
		});
	},

	emp_code: function(frm) {
		frappe.call({
			method:"wsc.wsc.doctype.upload_material.upload_material.emp_id_call",
			args:{
				"emp_code":frm.doc.emp_code,
				"teacher_name":frm.doc.teacher_name
			}
		})
	},
	student_group: function(frm) {
		frappe.call({
			method:"wsc.wsc.doctype.upload_material.upload_material.student_group_call",
			args:{
				"Group":frm.doc.student_group,
			}
		})
	},

	setup: function(frm) {
		frm.set_query("student_group", function() {
			return {
				query: "wsc.wsc.doctype.upload_material.upload_material.Student_group_query"
			};
		});
		frm.set_query("subject_code", function() {
			return {
				query: "wsc.wsc.doctype.upload_material.upload_material.Course_query"
			};
		});
	},

})

// frappe.ui.form.on("Upload Material", "student_group", function(frm){
// 	frappe.model.with_doc("Student Group", frm.doc.student_group, function(){
// 		var tabletransfer = frappe.model.get_doc("Student Group", frm.doc.student_group);
// 		cur_frm.doc.students = "";
// 		cur_frm.refresh_field("students");
// 		$.each(tabletransfer.students, function(index, row){
// 			var d = frappe.model.add_child(cur_frm.doc, "Student Group Student", "students");
// 			d.student = row.student;
// 			d.student_name = row.student_name;
// 			d.student_name = row.student_name;
// 			d.group_roll_number = row.group_roll_number;
// 			cur_frm.refresh_field("students");
// 		});
// 	});
// });

frappe.ui.form.on("Upload Material", {
    refresh: function(frm) {
		// alert(frappe.datetime.nowdate())
		// && (frm.doc.start_date )
		if(frm.doc.receivable_by_students==1 && cur_frm.doc.docstatus==1 &&
			 (frm.doc.start_date<=frappe.datetime.nowdate() && frm.doc.end_date>=frappe.datetime.nowdate())) {
        frm.add_custom_button(__("Submission of task"), function() {
            frm.events.Submission_of_task(frm);
        }, __('Create'));   
		frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
	 },
		
    Submission_of_task: function(frm) {
            frappe.call({
                method:"wsc.wsc.doctype.upload_material.upload_material.Submission_of_task",
                args: {
                    "name": frm.doc.name,
					"student":frappe.session.user,
                },
                callback: function(r) {
                    if(!r.exc){
						var doc=r.message
						frappe.set_route("Form", "Assignment Upload",{"assignment_question":doc['Doc_id'],"student":doc['Student_id']});

                    }
                }
            });
    },
});

frappe.ui.form.on("Upload Material", "refresh", function(frm){
	if(cur_frm.doc.docstatus==1){
    frm.add_custom_button("Attachemnet of File/Video", function(){
		frappe.call({
			method:"wsc.wsc.doctype.upload_material.upload_material.download_file",
			args:{
				"doc_id":frm.doc.name
			},
			callback:function(r){
				if(!r.exc){
					var myWin = window.open(r.message);
				}
			}
		})
			
	});
	}
})