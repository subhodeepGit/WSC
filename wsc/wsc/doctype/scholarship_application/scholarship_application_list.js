frappe.listview_settings['Scholarship Application'] = {
	refresh: function(listview) {
		if(!frappe.user.has_role(["Administrator","Student"])){
        	$('.primary-action').hide();
		}
    }
};
