frappe.listview_settings['Employment Type'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}