// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Psychometric Test', {
// 	refresh: function(frm) {
// 		frm.set_query('designation', function() {
// 			return{
// 				filters: {
// 					"name":frm.doc.name
// 				}
// 			}
// 		});
// 	}
// });

frappe.ui.form.on('Psychometric Test', {
    start_section1: function(frm) {
        frappe.call({
            method: 'wsc.wsc.doctype.psychometric_test.psychometric_test.get_competencies',
            

           callback: function(r) {
                if(r.message){
                    frappe.model.clear_table(frm.doc, 'section1');
                    (r.message).forEach(element => {
                        var c = frm.add_child("section1")
                        c.competencies=element.competencies
                    });
                }
                frm.refresh();
                frm.refresh_field("section1")
            }
        })
    },
    start_section2: function(frm) {
        frappe.call({
            method: 'wsc.wsc.doctype.psychometric_test.psychometric_test.get_skills',


           callback: function(r) {
                if(r.message){
                    frappe.model.clear_table(frm.doc, 'section2');
                    (r.message).forEach(element => {
                        var c = frm.add_child("section2")
                        c.skill=element.skills
                    });
                }
                frm.refresh();
                frm.refresh_field("section2")
            }
        })
    },
})