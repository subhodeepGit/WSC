frappe.listview_settings['TnP Event'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}
