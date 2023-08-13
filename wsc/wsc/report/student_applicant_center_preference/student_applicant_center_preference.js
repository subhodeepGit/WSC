frappe.query_reports["Student Applicant Center Preference"] = {
	"filters": [
        {
			"label":"Academic Year",
			"fieldname":"academic_year",
			"fieldtype":"Link",
			"options":"Academic Year",
            "reqd":1
		},
		{
			"label":"Academic Term",
			"fieldname":"academic_term",
			"fieldtype":"Link",
			"options":"Academic Term",
            "reqd":1,
			"get_query": function() {
				return {
					filters: {
						'academic_year': frappe.query_report.get_filter_value('academic_year')
					}
				}
			}
		},
        {
            "label":"Department",
			"fieldname":"department",
			"fieldtype":"Link",
			"options":"Department",
            "reqd":1,
			"get_query": function() {
				return {
					filters: {
						'is_group': 1,
                        'is_stream' : 1
					}
				}
			}
        },
        {
            "label":"Program Grade",
			"fieldname":"program_grade",
			"fieldtype":"Link",
			"options":"Program Grades",
            "reqd":1,
        }
	]
};
