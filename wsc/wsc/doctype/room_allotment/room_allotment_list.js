frappe.listview_settings['Room Allotment'] = {
	get_indicator: function(doc) {
		if (doc.allotment_type==="Allotted") {
            return [__(doc.allotment_type), "green","allotment_type,=,Allotted"];
		}
        else if (doc.allotment_type==="De-Allotted") {
            return [__(doc.allotment_type), "orange","allotment_type,=,De-Allotted"];
		}
        else if (doc.allotment_type==="Death") {
            return [__(doc.allotment_type), "grey","allotment_type,=,Death"];
		}
        else if (doc.allotment_type==="Long Leave De-allotment") {
            return [__(doc.allotment_type), "yellow","allotment_type,=,Long Leave De-allotment"];
		}
    }
};
