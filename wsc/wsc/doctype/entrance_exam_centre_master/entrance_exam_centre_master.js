// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Centre Master', {
	setup: function(frm){
		frm.set_query("district", function() {
			return{
				filters:[
					["Districts","state","=",frm.doc.state]
				]
			}
		});
		frm.set_query("block", function() {
			return{
				filters:[
					["Blocks","districts","=",frm.doc.district]
				]
			}
		});

	},
	district(frm){
        frm.set_value("block",[]);
	}
});
