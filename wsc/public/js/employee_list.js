frappe.listview_settings['Employee'] = {
    onload: function(listview) {
        if (frappe.user.has_role(["Employee"]) && !frappe.user.has_role(["HR Admin","HR Manager/CS Officer","System Manager"])){
            if(frappe.route_options){
                frappe.route_options = {
                    "user_id": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
            }
        }
    }
};
frappe.listview_settings['Employee'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}