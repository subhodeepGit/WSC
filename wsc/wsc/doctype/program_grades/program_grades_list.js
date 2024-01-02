frappe.listview_settings['Program Grades'] = {
    onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
    }
}