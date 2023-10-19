import frappe


def execute(filters=None):
	data = get_data(filters)
	columns = get_columns(filters)

	return columns,data									 
	
def get_columns(filters=None):
    return [
		{
			"label": ("Admission Status"),
			"fieldname": "admission_status",
			"fieldtype": "Data",
			"width": 180
		},

		{
			"label": ("Student"),
			"fieldname": "student",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": ("Student Application ID"),
			"fieldname": "student_application_id",
			"fieldtype": "Data",
			"width": 180
		},
		{			
			"label": ("Student Name"),
			"fieldname": "student_name",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": ("Department"),
			"fieldname": "department",
			"fieldtype": "Data",
			"width": 180
		},
		{			
			"label": ("Course Name"),
			"fieldname": "programs",
			"fieldtype": "Data",
			"width": 180
		},
		# {
		# 	"label": _("Gender"),
		# 	"fieldname": "gender",
		# 	"fieldtype": "Data",
		# 	"width": 180
		# },
	

		# {
		# 	"label": _("Email"),
		# 	"fieldname": "student_email_id",
		# 	"fieldtype": "Data",
		# 	"width": 180
		# },
		{
			"label": ("Academic Year"),
			"fieldname": "academic_year",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": ("Caste Category"),
			"fieldname": "student_category",
			"fieldtype": "Data",
			"width": 180
		},
	
	
		{
			"label": ("Transaction ID"),
			"fieldname": "transaction_id",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": ("Transaction Status"),
			"fieldname": "transaction_status",
			"fieldtype": "Data",
			"width": 180
		},
		
		
	]

def get_data(filters):
	data= []
	fltr, flt2 = {},[]
	if filters.get("student_category"):
		fltr.update({"student_category":filters.get("student_category")})
	if filters.get("academic_year"):
		fltr.update({"academic_year":filters.get("academic_year")})
	# if filters.get("program_grade"):
	# 	fltr.update({"program_grade":filters.get("program_grade")})
	if filters.get("department"):
		fltr.update({"department":filters.get("department")})
	# if filters.get("docstatus"):
	# 	fltr.update({"docstatus":filters.get("docstatus")})
	if filters.get("programs"):
		fltr.update({"programs":filters.get("programs")})
	if filters.get("transaction_status"):
		fltr.update({"transaction_status":filters.get("transaction_status")})


	data=frappe.db.sql(''' SELECT pe.admission_status,
    pe.student, pe.student_application_id, pe.student_name, pe.department, pe.programs, pe.academic_year, pe.student_category, op.transaction_id, op.transaction_status
	FROM `tabProgram Enrollment` as pe 
	LEFT JOIN `tabOnlinePayment` as op ON pe.student=op.party 
	WHERE pe.student_category = %s and pe.academic_year=%s and pe.programs=%s and pe.department=%s and op.transaction_status=%s and pe.docstatus=1 ORDER BY pe.student''',(filters.get("student_category"),filters.get("academic_year"),filters.get("programs"),filters.get("department"),filters.get("transaction_status")),as_dict=1)
	return data