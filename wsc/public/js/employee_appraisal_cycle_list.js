frappe.listview_settings['Employee Appraisal Cycle'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}