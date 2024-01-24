frappe.listview_settings['Employee Appraisal Portal'] = {
	get_indicator: function(doc) {
        console.log("Doc Status:", doc.approval_status);
		if (doc.approval_status=="Draft") {
            return [__(doc.approval_status), "red","approval_status,=,Draft"];
		}
        else if (doc.approval_status=="Submit") {
            return [__(doc.approval_status), "blue","approval_status,=,Submit"];
		}
        else if (doc.approval_status=="Rejected") {
            return [__(doc.approval_status), "grey","approval_status,=,Rejected"];
		}
        else if (doc.approval_status=="Approved") {
            return [__(doc.approval_status), "green","approval_status,=,${doc.approval_status}"];
		}
        else{
            return [__(doc.approval_status), "purple", "approval_status,=," + doc.approval_status];
		}
    }
};