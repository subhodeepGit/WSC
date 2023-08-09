frappe.listview_settings['Student Group'] = {
    refresh: function(listview) {
        listview.page.actions.find('[data-label="Edit"],[data-label="Assign To"]').parent().parent().remove()

    }
};