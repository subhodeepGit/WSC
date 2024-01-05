frappe.listview_settings['Employee Appraisal Portal'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}