// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Material Distribution', {
	setup: function (frm) {
		frm.set_query("allotment_number", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query"
			};
		});
	},
	allotment_number:function fetchMaterial(frm) {
		var serverDate = frappe.datetime.nowdate(); 
	    frappe.call({
			method: "wsc.wsc.doctype.material_distribution.material_distribution.fetch_material",
			args: {
				server_date: serverDate
			},
			callback: function (response) {
				var materialRecords = response.message;
				if (materialRecords && materialRecords.length > 0) {
					(materialRecords).forEach(element => {
						var c = frm.add_child("materials_allotment")
						c.materials=element.material;
						c.mandatory_materials=element.mandatory_material
					});
					frm.refresh_field("materials_allotment")
				} else {
					frappe.msgprint("No Material Distribution Master record found for the given date.");
				}
			}
		});
	},
});