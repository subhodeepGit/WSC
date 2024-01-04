frappe.listview_settings['Shift Request'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}