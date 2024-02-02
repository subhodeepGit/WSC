frappe.ui.form.on('Purchase Invoice', {
    setup: function(frm){
    frm.set_df_property('advances', 'cannot_add_rows', true)
    frm.set_df_property('advances', 'cannot_delete_rows', true)
    },          
    refresh(frm) {
        if(!window.location.hash) {
            window.location = window.location + '#';
            window.location.reload();
        }
    },                
    onload_post_render: function(frm){                      
        frm.page.remove_inner_button('Subscription', 'Create')
        frm.page.remove_inner_button('Purchase Receipt', 'Create')
        frm.page.remove_inner_button('Block Invoice', 'Create')
        frm.page.remove_inner_button('Payment Request', 'Create')
        frm.page.remove_inner_button('Purchase Receipt','Get Items From')
        frm.page.remove_inner_button('Purchase Order','Get Items From')
        frm.page.remove_inner_button('Accounting Ledger','View')
        }
    }
);