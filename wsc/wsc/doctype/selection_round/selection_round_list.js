frappe.listview_settings['Selection Round'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}
