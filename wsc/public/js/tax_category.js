frappe.ui.form.on("Tax Category", {
    onload: function(frm) {
		frm.set_query("parent_tax_category", function() {
			return {"filters": [["Tax Category", "is_group", "=", 1]]};
		});
	},
	refresh: function(frm) {
		// read-only for root department	
		if(!frm.doc.parent_tax_category && !frm.is_new()) {
			frm.set_read_only();
			frm.set_intro(__("This is a root department and cannot be edited."));
		}
	},
	validate: function(frm) {
		if(frm.doc.name=="All Tax Category") {
			frappe.throw(__("You cannot edit root node."));
		}
		if(!frm.doc.parent_tax_category) {
			frm.set_value("parent_tax_category","All Tax Category");
		}
	}
	
});