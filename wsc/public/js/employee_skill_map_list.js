frappe.listview_settings['Employee Skill Map'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}