frappe.listview_settings['Student Clearance Application'] = {
	refresh: function(listview) {
		if(frappe.user.has_role(["Student"]) && !frappe.user.has_role(["Administrator"])){
			$('[data-label="Edit"]').parent().parent().remove();
			$('[data-label="Apply%20Assignment%20Rule"]').parent().parent().remove();
        	$('[data-label="Assign%20To"]').parent().parent().remove();
			$('[data-label="Add%20Tags"]').parent().parent().remove();
		}
    },
	get_indicator: function(doc) {
		if (doc.status==="Clearance Pending") {
            return [__(doc.status), "green","status,=,Clearance Pending"];
		}
        else if (doc.status==="Clearance Approved") {
            return [__(doc.status), "orange","status,=,Clearance Approved"];
		}
    }
};