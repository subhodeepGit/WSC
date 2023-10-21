frappe.ui.form.on('Item', "item_group", function(frm) {
	var group ="";
	group = cur_frm.doc.item_group.slice(0, 4).toUpperCase();
	frm.set_value("item_code",group);
	refresh_field("item_code");
});

frappe.ui.form.on('Item', {
    refresh:function(frm) {
		frm.remove_custom_button('Stock Projected Qty','View');
            frm.remove_custom_button('Publish in Website','Actions');
			frm.remove_custom_button('Add / Edit Prices','Actions');
	}
});