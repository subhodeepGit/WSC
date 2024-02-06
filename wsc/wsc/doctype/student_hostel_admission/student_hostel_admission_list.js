frappe.listview_settings['Student Hostel Admission'] = {
	get_indicator: function(doc) {
         
		if (doc.allotment_status==="Allotted") {
            return [__(doc.allotment_status), "green","allotment_status,=,Allotted"];
		}
        else if (doc.allotment_status==="De-allotted") {
            return [__(doc.allotment_status), "orange","allotment_status,=,De-allotted"];
		}
        else if (doc.allotment_status==="Death-Deallotted") {
            return [__(doc.allotment_status), "grey","allotment_status,=,Death-Deallotted"];
		}
        else if (doc.allotment_status==="Not Reported") {
            return [__(doc.allotment_status), "cyan","allotment_status,=,Not Reported"];
		}
    }
};