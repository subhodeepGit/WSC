frappe.listview_settings['Dimenssions for Appraisal'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}