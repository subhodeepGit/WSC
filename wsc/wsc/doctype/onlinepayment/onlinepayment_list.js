frappe.listview_settings['OnlinePayment'] = {
    add_fields: ["docstatus"],
    get_indicator: function(doc) {
        if (doc.docstatus === 0) {
            return [__("Draft"), ""];
        } else if (doc.docstatus === 1 && doc.transaction_status==="Success") {
            return [__(doc.transaction_status), "green","transaction_status,=,Success"];
        } else if (doc.docstatus === 1 && doc.transaction_status==="Shipped") {
            return [__(doc.transaction_status), "green","transaction_status,=,Shipped"];
        }else if (doc.docstatus === 1 && doc.transaction_status==="Aborted") {
            return [__(doc.transaction_status), "orange","transaction_status,=,Aborted"];
        } else if (doc.docstatus === 1 && doc.transaction_status==="Timeout") {
            return [__(doc.transaction_status), "gray","transaction_status,=,Timeout"];
        }  else if (doc.docstatus === 1 && doc.transaction_status==="Failure") {
            return [__(doc.transaction_status), "red","transaction_status,=,Failure"];
        }  else if (doc.docstatus === 1 && doc.transaction_status==="Rejected") {
            return [__(doc.transaction_status), "purple","transaction_status,=,Rejected"];
        }else if (doc.docstatus === 1 && doc.transaction_status==="Awaited") {
            return [__(doc.transaction_status), "yellow","transaction_status,=,Awaited"];
        }else if (doc.docstatus === 1 && doc.transaction_status==="Initiated") {
            return [__(doc.transaction_status), "cyan","transaction_status,=,Initiated"];          
         
        } else if (doc.docstatus === 2 ) {
            return [__("Cancelled"), "red"];
        }
    }
};

