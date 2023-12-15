frappe.ui.form.on('Purchase Invoice', {                          
    onload_post_render: function(frm){                      
        frm.page.remove_inner_button('Subscription', 'Create')
        frm.page.remove_inner_button('Purchase Receipt', 'Create')
        frm.page.remove_inner_button('Block Invoice', 'Create')
        frm.page.remove_inner_button('Payment Request', 'Create')
        frm.page.remove_inner_button('Purchase Receipt','Get Items From')
        frm.page.remove_inner_button('Purchase Order','Get Items From');
        }
    }
);