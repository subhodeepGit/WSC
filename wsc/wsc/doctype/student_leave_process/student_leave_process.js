// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Leave Process', {
	setup: function (frm) {
		frm.set_query("allotment_number", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query"
			};
		});
	},
	allotment_number:function(frm){
        if(frm.doc.allotment_number){
            frappe.call({
                method:"wsc.wsc.doctype.room_change.room_change.get_allotment_data",
                args: {
                    "allotment_number": frm.doc.allotment_number,
                },
                callback: function(r) {
                    if(r.message){
                        frm.set_value('student', r.message.student);
                        frm.set_value('student_name', r.message.student_name);
                        frm.set_value('roll_no', r.message.roll_no);
                        frm.set_value('registration_number', r.message.registration_number);
                        frm.set_value('hostel', r.message.hostel_id);
                        frm.set_value('room_number', r.message.room_id);
                        frm.set_value('room_type', r.message.room_type);
                        frm.set_value('room_no', r.message.room_number);
                    }
                }
            });
        } else{
            frm.set_value('student', "");
            frm.set_value('student_name', "");
            frm.set_value('roll_no', "");
            frm.set_value('registration_number', "");
            frm.set_value('hostel', "");
            frm.set_value('room_number', "");
            frm.set_value('room_type', "");
            frm.set_value('room_no', "");
        }
    },
    refresh: function(frm) {
        if (frm.doc.workflow_state != "Submit"){
            Object.keys(cur_frm.fields_dict).forEach(field=>{
                frm.set_df_property(field,'read_only',1)
            })
        }
    }
})
