frappe.listview_settings['Room Allotment'] = {
	get_indicator: function(doc) {
		if (doc.allotment_type==="Allotted") {
            return [__(doc.allotment_type), "green","allotment_type,=,Allotted"];
		}
        else if (doc.allotment_type==="De-allotted") {
            return [__(doc.allotment_type), "orange","allotment_type,=,De-allotted"];
		}
        else if (doc.allotment_type==="De-allotted") {
            return [__(doc.allotment_type), "grey","allotment_type,=,Death-Deallotted"];
		}
    }
};