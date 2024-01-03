frappe.listview_settings['Branch'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}