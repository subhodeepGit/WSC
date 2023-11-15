// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Floor', {
	refresh: function(frm) {
		frm.set_query("building_name", function() {
			return {
                query: "wsc.wsc.doctype.floor.floor.building_query",
			}
		});
	},
	building_name:function(frm){
		frappe.model.with_doc("Buildings", frm.doc.building_name, function () {
			var tabletransfer = frappe.model.get_doc("Buildings", frm.doc.building_name);
			cur_frm.doc.land_details = "";
			$.each(tabletransfer.land_details, function (index, row) {
				var d = frappe.model.add_child(cur_frm.doc, "Land Details", "land_details");
				d.land_plot_number = row.land_plot_number;
				d.land_address =row.land_address;
			});
			cur_frm.refresh_field("land_details");
		});
	} 
});
