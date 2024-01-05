frappe.listview_settings['Event feedback'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}
