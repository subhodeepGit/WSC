frappe.listview_settings['Academic Events'] = {
	onload: function(listview) {
        $('[data-label="Edit"]').parent().parent().remove();
        // $('[data-toggle="dropdown"]').parent().parent().remove();
        // listview.$page.find(`div[class='filter-selector']`).css('display','none')
        // listview.$page.find('.custom-actions, .hidden-xs, .hidden-md').css('display','none')
    },
};
