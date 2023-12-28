frappe.listview_settings['ToT Class Schedule'] = {
    refresh: function(listview) {
        $('.primary-action').hide();
        },
    add_fields: ["re_scheduled", "is_canceled"],
    get_indicator: function(doc) {
        if (doc.re_scheduled === 0 && doc.is_canceled === 0) {
            return [__("Scheduled"), "green"];
        } else if (doc.re_scheduled === 1 && doc.is_canceled === 0) {
            return [__("Rescheduled"), "purple"];
        } else if (doc.is_canceled === 1) {
            return [__("Cancelled"), "red"];
        }
    }
    }