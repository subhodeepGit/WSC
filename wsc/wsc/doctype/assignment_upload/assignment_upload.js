// Copyright (c) 2022, SOUL LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment Upload', {
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
	}
});

frappe.ui.form.on("Assignment Upload", "refresh", function(frm){
	if(cur_frm.doc.docstatus==1){
    frm.add_custom_button("Uploded Answers", function(){
		frappe.call({
			method:"wsc.wsc.doctype.assignment_upload.assignment_upload.download_file",
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

frappe.ui.form.on("Assignment Upload", "refresh", function(frm){
	if(cur_frm.doc.docstatus==1){
    frm.add_custom_button("Question Paper", function(){
		frappe.call({
			method:"wsc.wsc.doctype.assignment_upload.assignment_upload.Question",
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