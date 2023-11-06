frappe.listview_settings['TnP Program'] = {
    onload: function(listview) {
        // listview.page.menu.find('[data-label=""]').parent().parent().remove();
        $('[data-label="Edit"]').parent().parent().remove();  
    }
}