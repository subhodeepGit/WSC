frappe.listview_settings['Bank'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}