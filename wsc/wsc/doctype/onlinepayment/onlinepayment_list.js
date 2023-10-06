frappe.listview_settings['OnlinePayment'] = {
    add_fields: ["docstatus"],
    get_indicator: function(doc) {
        if (doc.docstatus === 0) {
            return [__("Draft"), ""];
        } else if (doc.docstatus === 1 && doc.transaction_status==="Success") {
            return [__(doc.transaction_status), "green"];
        } else if (doc.docstatus === 1 && doc.transaction_status==="Aborted") {
            return [__(doc.transaction_status), "orange"];
        } else if (doc.docstatus === 1 && doc.transaction_status==="Timeout") {
            return [__(doc.transaction_status), "gray"];
        }  else if (doc.docstatus === 1 && doc.transaction_status==="Failure") {
            return [__(doc.transaction_status), "red"];
        }  else if (doc.docstatus === 1 && doc.transaction_status==="Rejected") {
            return [__(doc.transaction_status), "purple"];
        } else if (doc.docstatus === 2 ) {
            return [__("Cancelled"), "red"];
        }
    }
};