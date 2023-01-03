frappe.query_reports["Alloted Students based on Academic Year"] = {
    "filters": [
        {
            "fieldname":"building",
            "label": __("Building"),
            "fieldtype": "Link",
            "options": "Building",
            "default": "PG Hostel (Girls) University Campus",
        },
    ]
}