frappe.listview_settings['Material Request'] = {
    onload: function(listview) {
        // listview.page.menu.find('[data-label=""]').parent().parent().remove();
        $('[data-label="Approve"]').parent().parent().remove();
        $('[data-label="Reject"]').parent().parent().remove(); 
        $('[data-label="Cancel"]').parent().parent().remove(); 
        $('[data-label="Save"]').parent().parent().remove(); 
        $('[data-label="Submit"]').parent().parent().remove(); 
    }
}