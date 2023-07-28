// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment Exam Center', {
	setup:function(frm)
    {
        frm.set_query("district", function() {
            return {
                filters: {
                    "state":frm.doc.state
                }
            };
        });
        frm.set_query("block", function() {
            return {
                filters: {
                    "districts":frm.doc.district
                }
            };
		});
	}
});
