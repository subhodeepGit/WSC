// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Selection Round', {
	// refresh: function(frm) {

	// }
	onsubmit: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.placement_tool.placement_tool.update_profile',
			args:{
				doc: frm.doc
			},
			callback: function(result){
				// alert(result.message)
			}
		})
	},
	oncancel: function(frm){
		// alert(1)
		frappe.call({
			method: 'wsc.wsc.doctype.selection_round.selection_round.update_application',
			args:{
				doc: frm.doc
			},
			callback: function(result){
				// alert(result.message)
			}
		})
	}
});
