// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Selection Round', {
	onsubmit: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.placement_tool.placement_tool.update_profile',
			args:{
				doc: frm.doc
			},
			callback: function(result){
			}
		})
	},
	oncancel: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.selection_round.selection_round.update_application',
			args:{
				doc: frm.doc
			},
			callback: function(result){
			}
		})
	}
});
