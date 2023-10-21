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
		if (frm.doc.material_request_type ==='Material Transfer' && frm.doc.workflow_state !== 'Approved by Purchase Manager'){
            frm.remove_custom_button("Material Transfer","Create");
			frm.remove_custom_button("Material Transfer (In Transit)","Create");
			frm.remove_custom_button("Pick List","Create");
        }
		if (frm.doc.material_request_type ==="Material Issue" && frm.doc.workflow_state !== 'Approved by Purchase Manager'){
            frm.remove_custom_button("Issue Material","Create");
        }
    },
	calculate_grand_total: function(frm) {
		var grandTotal = 0;
    	frm.doc.items.forEach(function(item) {
        	grandTotal += (item.qty || 1) * (item.price || 0);
    	});
    	frm.set_value('grand_total', grandTotal);
	}
});

frappe.ui.form.on('Material Request', {
	refresh: function(frm) {
		frm.set_df_property('material_request_type', 'options', ['Purchase', 'Material Transfer','Material Issue']);
	}
});	
frappe.ui.form.on('Material Request', {
	onload: function(frm) {
	frm.set_df_property('status', 'options', ['Draft', 'Submitted','Hold','Cancelled','Pending','Partially Ordered']);
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
		frm.trigger("calculate_grand_total");
  	},
  // When field is deleted from child table on that time calculation going to happend to the accordingly
  	items_remove:function(frm, cdt, cdn){ //Child table name
		frm.trigger("calculate_grand_total");
	},
	item_code: function(frm, cdt, cdn) {
		frm.trigger("calculate_grand_total");
        var child = locals[cdt][cdn];
        if (child.idx === 1) {
            var product_item_group = child.item_group;
            frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
                var row = locals[cdt][cdn];
                var existing_items = [];
                frm.doc.items.forEach(function(item) {
                    if (item.item_code && item.item_code !== row.item_code) {
                        existing_items.push(item.item_code);
                    }
                });
                
                return {
                    filters: {
                        item_group: product_item_group,
                        name: ['not in', existing_items]
                    }
                };
            };
            
            frm.fields_dict['items'].grid.refresh();
        }
    }
	
	
});