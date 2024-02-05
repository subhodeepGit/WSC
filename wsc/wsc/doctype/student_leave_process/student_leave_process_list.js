frappe.listview_settings['Student Leave Process'] = {
    onload: function(listview) {
        $('[data-label="Submitted"]').parent().parent().remove(); 
        $('[data-label="Withdrawl"]').parent().parent().remove();   
        $('[data-label="Approve"]').parent().parent().remove(); 
        $('[data-label="Reject"]').parent().parent().remove();
        $('[data-label="Edit"]').parent().parent().remove();
        $('[data-label="Delete"]').parent().parent().remove();
    }
}