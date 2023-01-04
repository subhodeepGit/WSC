// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Indisciplinary Complaint Registration', {
    setup: function (cur_frm) {
        cur_frm.set_query("allotment_number", "student", function() {
            return {
                query: "wsc.wsc.doctype.indisciplinary_complaint_registration.indisciplinary_complaint_registration.ra_query"
            };
        });
    }
})

    // Checking duplicate 
frappe.ui.form.on("Indisciplinary Complaint Registration Student", "allotment_number", function(frm, cdt, cdn){
    var al_no = frm.doc.student;
    var arr =[];
    for(var i in al_no){
        arr.push(al_no[i].allotment_number);
        
    }
    for (var j=0;j<arr.length-1;j++){
        for(var k=j+1;k<arr.length;k++){
            if(arr[j] == arr[k]){
                // frappe.show_alert('Duplicate Allotment number')
                // frappe.msgprint(arr[k])                            
                frappe.msgprint("Duplicate entry "+arr[k])
            }
        }
    }
})