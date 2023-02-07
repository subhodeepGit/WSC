// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Drive Calendar', {
	onload: function(frm){
		frm.trigger('placement_drive')
		// console.log(frm.doc.placement_drive)
	},
	refresh: function(frm) {
		if(!frm.is_new()){
			frm.add_custom_button(__("Show Calendar") , ()=> {
				// console.log("Hello")
				frappe.set_route("List", frm.doc.placement_drive, "Calendar", frm.doc.round_of_placement)
			})
		}
	},
	placement_drive: function(frm) {
		const { placement_drive } = frm.doc
		if(!placement_drive) return

		// frappe.call({
		// 	method:'wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_rounds',
		// 	args: {
		// 			'placement_drive':frm.doc.placement_drive
		// 		},
			// callback: function(result){
			// 	let arr = Object.values(result)
			// 	let value = Object.values(arr[0])
			// 	// console.log(arr[0]);
			// 	// console.log(value[0].round_name)
			// 	frm.doc.round_of_placement = value[0].round_name
				
			// 	refresh_field("frm.doc.round_of_placement")
			// 	console.log(frm.doc.round_of_placement);
			// }
		// })
		// const meta = frappe.get_meta(placement_drive)
		// console.log(frm.doc.placement_drive);
		// frappe.model.with_doctype(placement_drive , ()=> {
		// 	const meta = frappe.get_meta(placement_drive);

		// 	console.log(meta);
		// })
	},
	round_of_placement: function(frm){
		// frappe.call({
		// 	// method:'wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_rounds',
		// 	method:'wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_rounds',
		// 	args: {
		// 		'placement_drive':frm.doc.placement_drive
		// 	}
		// })
	}

});
// wsc.wsc.doctype.placement_drive_calendar.placement_drive_calendar.get_rounds