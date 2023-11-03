frappe.listview_settings['Item Price'] = {
    onload: function(listview) {
        // listview.page.menu.find('[data-label=""]').parent().parent().remove();
        $('[data-label="Approve"]').parent().parent().remove(); 
        $('[data-label="Cancel"]').parent().parent().remove(); 
        $('[data-label="Save"]').parent().parent().remove();  
    }
}