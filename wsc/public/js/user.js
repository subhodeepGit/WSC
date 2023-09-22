frappe.ui.form.on('User',{
    refresh: function(frm) {
        if (frappe.user.has_role(["Student","Instructor"])){
            frm.set_df_property('api_access', 'hidden', 1);
            frm.remove_custom_button("Create User Email");
        }
        if (frappe.user.has_role(["Student"]) && !frappe.user.has_role(["System Manager"])){ 
            Object.keys(cur_frm.fields_dict).forEach(field=>{
                if (['email','new_password','logout_all_sessions','phone','mobile_no','interest','bio','mute_sounds','desk_theme'].includes(field)){
                    frm.set_df_property(field,'read_only',0)
                }
                else{
                    frm.set_df_property(field,'read_only',1)
                }
            })
        }
        
    }
})

frappe.ui.form.on('User',{
    refresh: function(frm) {
        if (frappe.session.user != "Administrator"){
            if (frm.doc.full_name=="Administrator" || frm.doc.email == "admin@soulunileaders.com"){
            Object.keys(cur_frm.fields_dict).forEach(field=>{
                frm.set_df_property(field,'hidden',1)
            })
            frm.remove_custom_button('Reset Password', 'Password');
            frm.remove_custom_button('Reset OTP Secret', 'Password');
        }
        frm.remove_custom_button('Set User Permissions', 'Permissions');
        frm.remove_custom_button('View Permitted Documents', 'Permissions');
    }  
    }
})
