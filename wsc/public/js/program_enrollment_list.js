frappe.listview_settings['Program Enrollment'] = { 
    
    add_fields: [ "admission_status"],
	has_indicator_for_draft: 1,
	get_indicator: function(doc) {
        if (doc.admission_status=="Admitted" && doc.docstatus==1) {
            return [__("Admitted"), "green", "admission_status,=,Green"];
		}
        else if (doc.admission_status=="Provisional Admission" && doc.docstatus==1) {
			return [__("Provisional Admission"), "orange", "admission_status,=,Provisional Admission"];
		}
		else if (doc.docstatus==0) {
			return [__("Draft"), "yellow", "admission_status,=,Draft"];
		}
	}
};
