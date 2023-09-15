frappe.listview_settings['Deallotment Process'] = {
    onload: function(listview) {
        // listview.page.menu.find('[data-label=""]').parent().parent().remove();
        $('[data-label="Review"]').parent().parent().remove(); 
        $('[data-label="Reject"]').parent().parent().remove();   
    }
}