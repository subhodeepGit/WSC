// frappe.ui.form.on('Purchase Order', {
//     refresh:function(frm) {
//         frm.remove_custom_button('Product Bundle','Get Items From');
// 	}
// });

frappe.ui.form.on('Purchase Order', {                          
    onload_post_render: function(frm){                      
        frm.page.remove_inner_button('Product Bundle','Get Items From')
        frm.page.remove_inner_button('Update Rate as per Last Purchase', 'Tools')
        frm.page.remove_inner_button('Link to Material Request', 'Tools')
        frm.page.remove_inner_button('Hold', 'Status')
        frm.page.remove_inner_button('Close', 'Status')
        frm.page.remove_inner_button('Subscription', 'Create')
		frm.page.remove_inner_button('Payment Request', 'Create')
		frm.page.remove_inner_button('Update Items')
        }
    }
);