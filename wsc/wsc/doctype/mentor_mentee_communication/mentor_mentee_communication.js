// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Mentor Mentee Communication', {
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) { 
					if(r.message){
						// if (r.message['mentor']){
						// 	frm.set_value("mentor",r.message['mentor'])
						// }
						// else if (r.message['mentor_name']){
						// 	frm.set_value("mentor_name",r.message['mentor_name'])
						// }
						// else if (r.message['programs']){
						// 	frm.set_value("programs",r.message['programs'])
						// }
						frm.set_value("mentor",r.message['mentor'])
						frm.set_value("mentor_name",r.message['mentor_name'])
						frm.set_value("programs",r.message['programs'])
					}
				} 
			}); 
		}else{
			frm.set_value("mentor","")
			frm.set_value("programs","")
		}
	},
	setup: function(frm){
		if(frm.doc.mentor){
			frm.set_query("student", function() {
				return {
					query: 'wsc.wsc.doctype.mentor_mentee_communication.mentor_mentee_communication.get_students',
					filters: {
						"mentor":frm.doc.mentor
					}
				};
			});
		}
		
	},
	onload: function(frm) {
		if(!frm.is_new()){
			frm.set_df_property('student', 'read_only', 1)
			frm.set_df_property('date', 'read_only', 1)
		}
	}
});

frappe.ui.form.on('Mentor Mentee Communication', {
	refresh: function(frm) {
		var text = frm.doc.comment_message;
		if (!frm.doc.description) {
			frm.remove_custom_button(__('Comment'));
		} else if (!frm.doc.comment_button_generated) {
			frm.add_custom_button(__('Comment'), function() {
				frappe.prompt({
					label: __('Enter your comment'),
					fieldname: 'comment',
					fieldtype: 'Small Text',
					reqd: 1
				}, function(data) {
					if (text){
						frm.set_value('comment_message', text + "\n" + frappe.session.user + " : " + data.comment);
					}
					else{
						frm.set_value('comment_message', frappe.session.user + " : " + data.comment);
					}
					frm.refresh_field('comment_message');
					frm.save();
				}, __('Add Comment'), __('Comment'));
			});
		}}});