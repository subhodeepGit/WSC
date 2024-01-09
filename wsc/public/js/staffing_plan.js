frappe.ui.form.on('Staffing Plan', {
    refresh: function(frm) {
        var userRoles = frappe.user_roles;
        var restrictedRole = 'HR Assistant';
        var isRestrictedRole = userRoles.includes(restrictedRole);
        frm.set_df_property('get_job_requisitions', 'hidden', isRestrictedRole);
    }
});
