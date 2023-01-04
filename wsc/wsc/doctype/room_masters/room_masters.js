// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Masters', {
	setup: function (frm) {
		frm.set_query("room_type_id", function () {
			return {
				query: "wsc.wsc.doctype.room_masters.room_masters.room_type_query",
			}
		});
		frm.set_query("actual_room_type", function() {
			return {
				query: "wsc.wsc.doctype.room_masters.room_masters.room_type_query"
			};
		});
		frm.set_query("room_description", function() {
			return {
				query: "wsc.wsc.doctype.room_masters.room_masters.room_description_query"
			};
		});
	}
})


frappe.ui.form.on('Room Masters', 'actual_capacity', function(frm, cdt, cdn) {
    var op = frm.doc.actual_capacity;
    var change = 0;
    if (frm.doc.vacancy == null && frm.doc.previous_room_capacity == null){     
        frm.doc.vacancy = op
        frm.set_value("vacancy",frm.doc.vacancy)
        frm.doc.previous_room_capacity = op
        frm.set_value("previous_room_capacity",frm.doc.previous_room_capacity)
        frm.refresh();
    }
    else if(parseInt(op) != frm.doc.previous_room_capacity && frm.doc.vacancy == frm.doc.previous_room_capacity){
        frm.doc.vacancy = op
        frm.set_value("vacancy",frm.doc.vacancy)
        frm.doc.previous_room_capacity = op
        frm.set_value("previous_room_capacity",frm.doc.previous_room_capacity)
        frm.refresh();
    }
    else{
        if(parseInt(op) > frm.doc.previous_room_capacity){
            change = parseInt(op) - frm.doc.previous_room_capacity
            frm.doc.vacancy = parseInt(frm.doc.vacancy) + parseInt(change)
            frm.set_value("vacancy",frm.doc.vacancy)
            frm.set_value("previous_room_capacity",op)
            frm.refresh();
        }
        else if(parseInt(op) < frm.doc.previous_room_capacity){
            change = parseInt(op) - frm.doc.previous_room_capacity
            frm.refresh();
            if(change <= frm.doc.vacancy && change > 0){
                frm.doc.vacancy = parseInt(frm.doc.vacancy) - parseInt(change)
                frm.set_value("vacancy",frm.doc.vacancy)
                frm.set_value("previous_room_capacity",op)
                frm.refresh();
            }
            else{
                frappe.throw("Room is not vacant")
            }
        }
        else if(parseInt(op) == frm.doc.previous_room_capacity)
        {
            pass
        }
    }
});