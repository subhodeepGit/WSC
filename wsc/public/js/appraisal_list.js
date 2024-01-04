frappe.listview_settings['Appraisal'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}