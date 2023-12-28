frappe.listview_settings['Instructor'] = {
    onload: function(listview) {
        // $(".menu-btn-group").hide();
        if (frappe.user.has_role(["Instructor"]) && !frappe.user.has_role(["Department Head"]) && !frappe.user.has_role(["Course Manager"])){        
            if(frappe.route_options){
                frappe.route_options = {
                    "email_id": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
                
            }
        }
        if (frappe.user.has_role(["TOT Trainer"]) && !frappe.user.has_role(["Department Head"]) && !frappe.user.has_role(["Course Manager"])){
            if(frappe.route_options){
                frappe.route_options = {
                    "email_id_for_guest_trainers": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
                
            }
        }
    }      
};