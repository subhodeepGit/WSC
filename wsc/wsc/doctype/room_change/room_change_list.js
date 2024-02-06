frappe.listview_settings['Room Change'] = {
    onload: function(listview) {
        $('[data-label="Approve"]').parent().parent().remove(); 
        $('[data-label="Review"]').parent().parent().remove();   
        $('[data-label="Reject"]').parent().parent().remove(); 
        $('[data-label="Reporting"]').parent().parent().remove();
        $('[data-label="Not%20Reported"]').parent().parent().remove(); 
        $('[data-label="Withdrawl"]').parent().parent().remove();
        $('[data-label="Edit"]').parent().parent().remove();
        $('[data-label="Delete"]').parent().parent().remove();
    }
}