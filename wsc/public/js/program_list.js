frappe.listview_settings['Program'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}