frappe.listview_settings['Student'] = {
    onload: function(listview) {
        if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role(["System Manager"])){ 
            $(".menu-btn-group").hide();
        }
    }      
};