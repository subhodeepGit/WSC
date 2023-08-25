frappe.listview_settings['My Profile'] = {
    onload: function(listview) {
        // $(".menu-btn-group").hide();
        if (!frappe.user.has_role(["Admin"]) || !frappe.user.has_role(["Education Administrator"])){ 
            if(frappe.route_options){
                frappe.route_options = {
                    "user_id": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
                
            }
        }
    }      
    
};