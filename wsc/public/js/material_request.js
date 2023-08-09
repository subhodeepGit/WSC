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