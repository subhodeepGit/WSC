frappe.listview_settings['Employee Grade'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}