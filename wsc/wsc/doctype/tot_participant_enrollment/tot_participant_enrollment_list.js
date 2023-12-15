frappe.listview_settings['ToT Participant Enrollment'] = {
    add_fields: ["docstatus"],
    get_indicator: function(doc) {
        if (doc.docstatus === 0) {
            return [__("Draft"), ""];
        } else if (doc.docstatus === 1 && doc.status==="Completed") {
            return [__("Participant Enrolled"), "green","status,=,Completed"];
        } else if (doc.docstatus === 1 && doc.status==="Not Completed ") {
            return [__("Participant Not Enrolled"), "purple","status,=,Completed "];
        } else if (doc.docstatus === 2 ) {
            return [__("Cancelled"), "red"];
        }
    }
};