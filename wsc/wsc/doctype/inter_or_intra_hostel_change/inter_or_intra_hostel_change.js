// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Inter or Intra Hostel Change', {
	setup: function (frm) {
		frm.set_query("allotment_no", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query",
				filters: [
					["Room Allotment", "name", "!=", frm.doc.second_allotment_no]
				]
			};
		});
		frm.set_query("second_allotment_no", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query",
				filters: [
					["Room Allotment", "name", "!=", frm.doc.allotment_no]
				]
			};
		});
	},
	allotment_no:function(frm){
		if(frm.doc.allotment_no){
			frappe.call({
				method:"wsc.wsc.doctype.inter_or_intra_hostel_change.inter_or_intra_hostel_change.get_allotment_data",
				args: {
					"allotment_no": frm.doc.allotment_no,
				},
				callback: function(r) {
					if(r.message){
                        // if(r.message['student']!=null){
                        //     frm.set_value('student',r.message['student'])
                        //     frm.set_df_property('student','read_only',1)
                        // }
                        if(r.message['student_name']!=null){
                            frm.set_value('1st_student_name',r.message['student_name'])
                            frm.set_df_property('1st_student_name','read_only',1)
                        }
						if(r.message['hostel_id']!=null){
                            frm.set_value('hostel_name',r.message['hostel_id'])
                            frm.set_df_property('hostel_name','read_only',1)
                        }
						if(r.message['room_number']!=null){
                            frm.set_value('room_no',r.message['room_number'])
                            frm.set_df_property('room_no','read_only',1)
                        }
						if(r.message['room_type']!=null){
                            frm.set_value('room_type',r.message['room_type'])
                            frm.set_df_property('room_type','read_only',1)
                        }
						if(r.message['allotment_type']!=null){
                            frm.set_value('allotment_type',r.message['allotment_type'])
                            frm.set_df_property('allotment_type','read_only',1)
                        }
						if(r.message['room_id']!=null){
                            frm.set_value('first_rid',r.message['room_id'])
                            // frm.set_df_property('room_no','read_only',1)
                        }
					}
				}
			});
		}
	},
	second_allotment_no:function(frm){
		if(frm.doc.second_allotment_no){
			frappe.call({
				method:"wsc.wsc.doctype.inter_or_intra_hostel_change.inter_or_intra_hostel_change.get_second_allotment_data",
				args: {
					"second_allotment_no": frm.doc.second_allotment_no,
				},
				callback: function(r) {
					if(r.message){
                        // if(r.message['student']!=null){
                        //     frm.set_value('student',r.message['student'])
                        //     frm.set_df_property('student','read_only',1)
                        // }
                        if(r.message['student_name']!=null){
                            frm.set_value('second_studnet_name',r.message['student_name'])
                            frm.set_df_property('second_studnet_name','read_only',1)
                        }
						if(r.message['hostel_id']!=null){
                            frm.set_value('second_hostel_name',r.message['hostel_id'])
                            frm.set_df_property('second_hostel_name','read_only',1)
                        }
						if(r.message['room_number']!=null){
                            frm.set_value('second_room_no',r.message['room_number'])
                            frm.set_df_property('second_room_no','read_only',1)
                        }
						if(r.message['room_type']!=null){
                            frm.set_value('second_room_type',r.message['room_type'])
                            frm.set_df_property('second_room_type','read_only',1)
                        }
						if(r.message['allotment_type']!=null){
                            frm.set_value('second_allotment_type',r.message['allotment_type'])
                            frm.set_df_property('second_allotment_type','read_only',1)
                        }
						if(r.message['room_id']!=null){
                            frm.set_value('second_rid',r.message['room_id'])
                            // frm.set_df_property('second_allotment_type','read_only',1)
                        }
					}
				}
			});
		}
	}

});
