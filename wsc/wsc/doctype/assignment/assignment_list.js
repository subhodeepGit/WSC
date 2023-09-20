frappe.listview_settings['Assignment'] = {
	add_fields: [ "assignment_creation_status"],
	get_indicator: function(doc) {
		if (doc.assignment_creation_status=="Pending") {
			return [__("Pending"), "orange", "assignment_creation_status,=,Pending"];
		}
		else if (doc.assignment_creation_status=="Completed") {
			return [__("Completed"), "green", "assignment_creation_status,=,Completed"];
		}
	}
};