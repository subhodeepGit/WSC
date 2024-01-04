frappe.listview_settings['Employee Appraisal Evaluation Template'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}