frappe.listview_settings['My Profile'] = {
    onload: function(listview) {
        // $(".menu-btn-group").hide();
        // if (frappe.user.has_role(["Instructor"]) && !frappe.user.has_role(["Department Head"])){ 
            if(frappe.route_options){
                frappe.route_options = {
                    "user_id": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
                
            }
        // }
    }      
};