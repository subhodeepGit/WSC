
frappe.listview_settings['Employee Grievance'] = {
    onload: function(listview) {
        if (frappe.user.has_role(["Employee"]) && !frappe.user.has_role(["HR Admin","HR Manager/CS Officer","System Manager","Grievance Cell Member","Director"])){
            if(frappe.route_options){
                frappe.route_options = {
                    "employee_email": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
            }
        }
}
 };
