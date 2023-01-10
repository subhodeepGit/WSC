frappe.ui.form.on('Student Attendance',{
    setup(frm){
        frm.set_query("student", function() {
            if (frm.doc.attendance_for == 'Hosteler'){
                return {
                    query: 'wsc.wsc.doctype.student_attendance.get_hostel_students',
                    filters: {
                        "is_hosteller":1,
                        "deallotment":0
                    }
                };
            }
        });
    },
    setup(frm){
        frm.set_query("topic", function() {
            return {
                query:"wsc.wsc.doctype.student_attendance.get_topic",
                filters: {
                    "course":frm.doc.course
                }
            };
        });
        frm.set_query("instructor", function() {
            return {
                 filters: {
                   "course":frm.doc.course
                 }
             };
         });
         frm.set_query("course_schedule", function() {
            return {
                 filters: {
                   "course":frm.doc.course
                 }
             };
         });
    },
    refresh(frm){
        cur_frm.dashboard.hide()
    },
    student(frm){
        if(frm.doc.student){
            frm.set_query("course_schedule", function() {
                return {
                    filters: {
                        "course":frm.doc.course
                    }
                };
            });
            frm.set_query("course", function() {
                return {
                    query: 'wsc.wsc.doctype.student_attendance.get_course',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
            if (frm.doc.attendance_for == 'Hosteler'){
                if(frm.doc.student){
                    frappe.call({
                        args: {
                        "student":frm.doc.student
                        },
                        method: "wsc.wsc.doctype.student_attendance.get_student_details",
                        callback: function(r) { 
                            if(r.message){
                                frm.set_value("building",r.message["building"])
                                frm.set_value("hostel_room",r.message["to_room"])
                            }
                            
                        } 
                    });
                }
            }
        }
    }
    // attendance_for:function(frm){
        
    // }

})

