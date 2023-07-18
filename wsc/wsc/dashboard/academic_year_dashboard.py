from frappe import _


def get_data(data):
	return {
		"fieldname": "academic_year",
		"transactions": [
			# {
			# 	"label": _("Student"),
			# 	"items": ["Student Admission", "Student Applicant", "Student Group", "Student Log"],
			# },
			# {"label": _("Fee"), "items": ["Fees", "Fee Schedule", "Fee Structure"]},
			{
				"label": _("Academic Term and Course"),
				"items": ["Academic Term", "Program Enrollment"],
			},
			# {"label": _("Assessment"), "items": ["Assessment Plan", "Assessment Result"]},
		],
	}
