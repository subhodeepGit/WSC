frappe.ui.form.on("Material Request Item", "qty", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
        d.total_amount = d.price * d.qty
        refresh_field("total_amount", d.total_amount);
});