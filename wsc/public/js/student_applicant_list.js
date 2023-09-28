frappe.listview_settings['Student Applicant'] = {
    onload: function(listview) {   
        if (frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){        
            $('.primary-action').hide();
            $('.menu-btn-group').hide();
            if(frappe.route_options){
                frappe.route_options = {
                    "student_email_id": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
                
            }
            $('[data-label="Export"]').parent().parent().remove();  
            $('[data-label="Edit"]').parent().parent().remove(); 
            $('[data-label="Cancel"]').parent().parent().remove();
            $('[data-label="Delete"]').parent().parent().remove();
            $('[data-label="Submit"]').parent().parent().remove();
        }
    },  
    
    add_fields: [ "application_status", 'paid'],
	has_indicator_for_draft: 1,
	get_indicator: function(doc) {
		if (doc.paid) {
			return [__("Paid"), "green", "paid,=,Yes"];
		}
        else if (doc.application_status=="Applied" && doc.docstatus==0) {
			return [__("Draft"), "yellow", "application_status,=,Applied"];
		}
		else if (doc.application_status=="Applied" && doc.docstatus==1) {
			return [__("Applied"), "orange", "application_status,=,Applied"];
		}
		else if (doc.application_status=="Approved") {
			return [__("Approved"), "green", "application_status,=,Approved"];
		}
		else if (doc.application_status=="Rejected") {
			return [__("Rejected"), "red", "application_status,=,Rejected"];
		}
		else if (doc.application_status=="Admitted") {
			return [__("Admitted"), "blue", "application_status,=,Admitted"];
		}
	}
};
frappe.listview_settings['Student Applicant'].refresh = function(listview) {
    if (frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){
    	$('.btn-primary').hide();
    }
};
