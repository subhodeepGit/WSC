frappe.listview_settings['Price List'] = {
    onload: function(listview) {
        // listview.page.menu.find('[data-label=""]').parent().parent().remove();
        $('[data-label="Edit"]').parent().parent().remove(); 
    }
}