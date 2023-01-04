// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Allotment', {
	setup: function (frm) {
		frm.set_query("room_id", function () {
			return {
				filters: [
					["Room Masters", "hostel_id", "=", frm.doc.hostel_id],
					["Room Masters", "validity", "=", "Approved"],
					["Room Masters", "status", "=", "Allotted"],
					["Room Masters", "vacancy", ">", 0],
					["Room Masters", "actual_room_type", "=", frm.doc.room_type_reference]
				]
			}
		});
		frm.set_query("hostel_id", function() {
			return {
				query: "wsc.wsc.doctype.room_allotment.room_allotment.test_query",
			};
		});
		frm.set_query("student", function() {
			return {
				query: "wsc.wsc.doctype.room_allotment.room_allotment.hostel_req_query"
			};
		});
		frappe.call({
            method: "wsc.wsc.doctype.room_allotment.room_allotment.employee",
            // args: {
            //     employee: frm.doc.employee,
            // },
            callback: function(r) { 
                if (r.message){
                    frm.set_value("employee",r.message)
                }
            } 
            
        });    
			
		
	},
	student(frm) {
        frappe.call({
            method: "wsc.wsc.doctype.room_allotment.room_allotment.allotment",
            args: {
                student: frm.doc.student,
            },
            callback: function(r) { 
                if (r.message){
                    frm.set_value("hostel_registration_no",r.message['name'])
                }
            } 
            
        });    
        
	},
})




// frappe.ui.form.on('Room Allotment', {
// 	setup: function (frm) {
// 		frm.set_query("room_id", function () {
// 			return {
// 				//query: "wsc.wsc.doctype.room_allotment.room_allotment.vacancy_query",
// 				filters: frm.doc.hostel_id == "Room Masters"  ?
// 					// ["Room Masters", "hostel_id", "=", frm.doc.hostel_id]
// 					{"hostel_id": frm.doc.hostel_id} : {"hostel_id": frm.doc.hostel_id}
// 			}
// 		});
// 		frm.set_query("hostel_id", function() {
// 			return {
// 				query: "wsc.wsc.doctype.room_allotment.room_allotment.test_query"
// 			};
// 		});
// 	}
// })

// frappe.ui.form.on("Room Allotment", "student", function(frm){
// 	frappe.model.with_doc("Student", frm.doc.student, function(){
// 		var tabletransfer = frappe.model.get_doc("Student", frm.doc.student);
// 		cur_frm.doc.guardians = "";
// 		cur_frm.refresh_field("guardians");
// 		$.each(tabletransfer.guardians, function(index, row){
// 			var d = frappe.model.add_child(cur_frm.doc, "Student Guardian", "guardians");
// 			d.guardian = row.guardian;
// 			d.guardian_name = row.guardian_name;
// 			d.relation = row.relation;
// 			cur_frm.refresh_field("guardians");
// 		});
// 	});
// });