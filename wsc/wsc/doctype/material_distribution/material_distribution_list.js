frappe.listview_settings['Material Distribution'] = {
    add_fields: ["docstatus"],
    get_indicator: function(doc) {
        if (doc.docstatus === 0) {
            return [__("Draft"), "grey", "docstatus,=,0"];
        } else if (doc.docstatus === 1) {
            return [__("Material Distributed"), "green", "docstatus,=,1"];
        } else if (doc.docstatus === 2) {
            return [__("Distribution Cancelled"), "orange", "docstatus,=,2"];
        }
    }
};
