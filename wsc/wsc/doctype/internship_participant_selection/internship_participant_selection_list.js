frappe.listview_settings['Internship Participant Selection'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}
