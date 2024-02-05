// frappe.ui.form.on('Purchase Receipt', {
//     refresh:function(frm) {
//         frm.remove_custom_button('Close', 'Status');
// 	}
// });

frappe.ui.form.on('Purchase Receipt', {  
    refresh(frm) {
        if(!window.location.hash) {
            window.location = window.location + '#';
            window.location.reload();
        }
    },                        
    onload_post_render: function(frm){                      
        frm.page.remove_inner_button('Asset', 'View')
        frm.page.remove_inner_button('Asset Movement', 'View')
        frm.page.remove_inner_button('Close', 'Status')
        frm.page.remove_inner_button('Subscription', 'Create')
        frm.page.remove_inner_button('Retention Stock Entry', 'Create')
        frm.page.remove_inner_button('Make Stock Entry', 'Create')
        frm.page.remove_inner_button('Purchase Invoice','Get Items From')
        frm.page.remove_inner_button('Purchase Order','Get Items From')
        frm.page.remove_inner_button('Accounting Ledger','View')
        }
    }
);