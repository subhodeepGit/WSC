frappe.ui.form.on('Stock Entry', {                          
    refresh: function(frm){                      
        frm.remove_custom_button('Purchase Invoice','Get Items From')
        frm.remove_custom_button('Purchase Requisition','Get Items From');
        frm.remove_custom_button('Expired Batches','Get Items From');
        frm.remove_custom_button('Bill of Materials','Get Items From');
        frm.remove_custom_button('Transit Entry','Get Items From');
        frm.remove_custom_button('Purchase Requisition','Create');
        }
    }
);