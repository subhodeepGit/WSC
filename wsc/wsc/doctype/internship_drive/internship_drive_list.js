frappe.listview_settings['Internship Drive'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}
