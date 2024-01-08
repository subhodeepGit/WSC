frappe.listview_settings['Designation'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}