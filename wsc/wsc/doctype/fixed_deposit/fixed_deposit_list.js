frappe.listview_settings['Fixed Deposit'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}