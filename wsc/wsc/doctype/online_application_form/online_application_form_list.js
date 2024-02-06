frappe.listview_settings['Online Application Form'] = {
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
    add_fields: [ "application_status", "is_applicant_reported"],
	has_indicator_for_draft: 1,
	get_indicator: function(doc) {

        if (doc.is_applicant_reported==1 && doc.application_status=="Approved") {
            return [__("Forwarded"), "pink", "enrollment_status,=,Enrolled"];
		}
        else if (doc.docstatus==0) {
			return [__("Draft"), "yellow", "application_status,=,Applied"];
		}
		else if (doc.application_status=="Applied" && doc.docstatus==1) {
			return [__("Applied"), "cyan", "application_status,=,Applied"];
		}
		else if (doc.application_status=="Approved" && doc.is_applicant_reported==0) {
			return [__("Approved"), "green", "application_status,=,Approved"];
		}
		else if (doc.application_status=="Not Approved") {
			return [__("Not Approved"), "red", "application_status,=,Not Approved"];
		}
		// else if (doc.application_status=="Admitted") {
		// 	return [__("Admitted"), "blue", "application_status,=,Admitted"];
		// }
       
	}
};
frappe.listview_settings['Online Application Form'].refresh = function(listview) {
    if (frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){
    	$('.btn-primary').hide();
    }
};
