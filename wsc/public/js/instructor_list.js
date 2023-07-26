frappe.listview_settings['Instructor'] = {
    onload: function(listview) {
        if (frappe.user.has_role(["Instructor"]) && !frappe.user.has_role(["System Manager"])){ 
            if(frappe.route_options){
                frappe.route_options = {
                    "email_id": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
            }
        }
    }      
};