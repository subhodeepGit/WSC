frappe.listview_settings['Students Grievance'] = {
	get_indicator: function(doc) {
		if (doc.status==="Issue Posted By Student") {
            return [__(doc.status), "green","status,=,Issue Posted By Student"];
		}
        if (doc.status==="Issue Posted By the Student") {
            return [__(doc.status), "green","status,=,Issue Posted By the Student"];
		}
        else if (doc.status==="Issue Received By Grievance Cell") {
            return [__(doc.status), "orange","status,=,Issue Received By Grievance Cell"];
		}
        else if (doc.status==="Issue Forwarded to Competent Authority") {
            return [__(doc.status), "grey","status,=,Issue Forwarded to Competent Authority"];
		}
        else if (doc.status==="Issue pending from Competent Authority") {
            return [__(doc.status), "yellow","status,=,Issue pending from Competent Authority"];
		}
        else if (doc.status==="Issue Closed") {
            return [__(doc.status), "purple","status,=,Issue Closed"];
		}
    }
};