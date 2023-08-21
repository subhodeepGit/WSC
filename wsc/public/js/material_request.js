frappe.ui.form.on('Material Request', {
	refresh: function(frm) {
		if (!frm.is_new() && frm.doc.material_request_type === 'Purchase') {
            frappe.call({
				method: 'wsc.wsc.doctype.material_request.get_next_state',
				args: {
					grand_total: frm.doc.grand_total,
					current_state: frm.doc.workflow_state,
					item_code: frm.doc.items[0].item_code,
					doc:frm.doc
				},
				callback: function(response) {
					var nextWorkflowState = response.message;
					if(!nextWorkflowState){
						frm.remove_custom_button("Purchase Order", "Create");
						frm.remove_custom_button("Request for Quotation", "Create");
						frm.remove_custom_button("Supplier Quotation", "Create");
					}
				}
			});
        }
		if (frm.doc.material_request_type ==='Material Transfer' && frm.doc.workflow_state !== 'Approved by GM-Procurement & Contract Management'){
            frm.remove_custom_button("Material Transfer","Create");
			frm.remove_custom_button("Material Transfer (In Transit)","Create");
			frm.remove_custom_button("Pick List","Create");
        }
		if (frm.doc.material_request_type ==="Material Issue" && frm.doc.workflow_state !== 'Approved by GM-Procurement & Contract Management'){
            frm.remove_custom_button("Issue Material","Create");
        }
    }
});

frappe.ui.form.on("Material Request Item", "qty", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
        d.total_amount = d.price * d.qty
        refresh_field("total_amount", d.total_amount);
});

// Child table Calculation
frappe.ui.form.on('Material Request Item', {	//Child table Name
	qty:function(frm, cdt, cdn){	//Child table field Name where you data enter
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.items.forEach(function(d) { a = a+ d.total_amount; }); //Child table name and field name
	frm.set_value("grand_total", a);			// Parent field name where calculation going to fetch
	refresh_field("grand_total");
  },
  // When field is deleted from child table on that time calculation going to happend to the accordingly
  items_remove:function(frm, cdt, cdn){ //Child table name
	var d = locals[cdt][cdn];
	var total = 0;
	let a= parseInt(total)
	frm.doc.items.forEach(function(d) { a += d.total_amount; });
	frm.set_value("grand_total", a);
	refresh_field("grand_total");
	}
});