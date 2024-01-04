frappe.listview_settings['Department'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}