frappe.listview_settings['Employee Group'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}