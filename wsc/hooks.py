from . import __version__ as app_version

app_name = "wsc"
app_title = "WSC"
app_publisher = "SOUL Limited"
app_description = "SOUL Limited"
app_email = "soul@soulunileaders.com"
app_license = "MIT"
# required_apps = ["education","hrms"]
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/wsc/css/wsc_ui.css"
app_include_js = "/assets/wsc/js/wsc_ui.js"

app_include_js = "wsc.bundle.js"

# include js, css files in header of web template
web_include_css = "/assets/wsc/css/wsc_ui.css"
web_include_js = "/assets/wsc/js/wsc_ui.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "wsc/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
                "Account":"public/js/account.js",
                "Course":"public/js/course.js",
                "Course Enrollment":"public/js/course_enrollment.js",
                "Course Schedule": "public/js/course_schedule.js",
                "Course Scheduling Tool": "public/js/course_scheduling_tool.js",
                "Fees" : "public/js/fees.js",
                "Fee Schedule":"public/js/fee_schedule.js",
                "Fee Structure" : "public/js/fee_structure.js",
                "Instructor":"public/js/instructor.js",
                "Payment Entry" : "public/js/payment_entry.js",
                "Program Enrollment":"public/js/program_enrollment.js",
                "Program":"public/js/program.js",
                "Student":"public/js/student.js",
                "Student Admission":"public/js/student_admission.js",
                "Student Applicant":"public/js/student_applicant.js",
                "Student Attendance":"public/js/student_attendance.js",
                "Student Attendance Tool":"public/js/student_attendance_tool.js",
                "Student Group": "public/js/student_group.js",
                "Student Leave Application":"public/js/student_leave_application.js",
                "Student Log":"public/js/student_log.js",
                "Topic":"public/js/topic.js",
                "User":"public/js/user.js",
                "Job Opening":"public/js/job_opening.js",
                "Item":"public/js/item.js",
                "Job Applicant":"public/js/job_applicant.js",
                "Employee":"public/js/employee.js",
                "Shift Request":"public/js/shift_request.js",
                "Leave Application":"public/js/leave_application.js",
                "Employee Separation":"public/js/employee_separation.js",
                "Bank Guarantee":"public/js/bank_guarantee.js"
            }
# calendars = ["Placement Drive Calendar",]
doctype_list_js = {
    "Branch Sliding Application": "wsc/wsc/doctype/branch_sliding_application/branch_sliding_application_list.js",
    "Fees":"public/js/fees_list.js",
    "Program Enrollment":"public/js/program_enrollment_list.js",
    "Student Attendance":"public/js/student_attendance_list.js",
    "Instructor" :"public/js/instructor_list.js",
    "Student Applicant" :"public/js/student_applicant_list.js",
    "Asset Maintenance Log":"public/js/asset_maintenance_log_list.js",
    "Leave Application":"public/js/leave_application_list.js",
    "Employee":"public/js/employee_list.js",
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------
after_migrate = [
        'wsc.patches.migrate_patch.set_translation',
        'wsc.patches.migrate_patch.add_roles',
        'wsc.patches.migrate_patch.set_custom_role_permission',
        'wsc.wsc.delete_doc_if_linked.execute',
        'wsc.patches.migrate_patch.set_custom_role_permission_remove_duplicate',
]

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "wsc.utils.jinja_methods",
#	"filters": "wsc.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "wsc.install.before_install"
after_install = "wsc.patches.get_phone_codes.execute"

# Uninstallation
# ------------

# before_uninstall = "wsc.uninstall.before_uninstall"
# after_uninstall = "wsc.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "wsc.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes



# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Academic Calendar Template": {
        "validate": "wsc.wsc.validations.academic_calender_template.validate"
    },
    "Academic Calender": {
        "validate": "wsc.wsc.validations.academic_calender.validate"
    },
    "Branch Sliding Application": {
        "validate": "wsc.wsc.validations.branch_sliding_application.validate"
    },
    "Branch sliding Declaration": {
        "validate": "wsc.wsc.validations.branch_sliding_declaration.validate"
    },
    "Counselling Structure":{
        "validate":"wsc.wsc.validations.counselling_structure.validate"
    },
    "Course Assessment Result": {
        "validate": "wsc.wsc.validations.course_assessment_result.validate"
    },
    "Course Assessment": {
        "validate": "wsc.wsc.validations.course_assessment.validate"
    },
    "Course Enrollment":{
       "after_insert":"wsc.wsc.validations.course_enrollment.after_insert",
       "validate":"wsc.wsc.validations.course_enrollment.validate",
       "on_trash":"wsc.wsc.validations.course_enrollment.on_trash"
    },
    "Course": {
        "validate": "wsc.wsc.validations.course.validate"
    },
	# "Course Schedule": {
	# 	"on_update": "wsc.wsc.doctype.course_schedule.on_change"
	# },
    "Exam Application":{
        "validate":"wsc.wsc.validations.exam_application.validate"
    },
    "Exam Assessment Plan": {
        "validate": "wsc.wsc.validations.exam_assesment_plan.validate"
    },
    "Exam Declaration":{
        "validate":"wsc.wsc.validations.exam_declaration.validate"
    },
    "Exam Paper Setting":{
        "validate":"wsc.wsc.validations.exam_paper_setting.validate"
    },
    "Exchange Program Declaration":{
        "validate":"wsc.wsc.validations.exchange_program_declaration.validate"
    },
    "Fee Schedule":{
        "validate":"wsc.wsc.validations.fee_schedule.validate"
    },
    "Feedback":{
        "validate":"wsc.wsc.validations.feedback.validate"
    },
    # "Course Schedule": {
    #     "on_update": "wsc.wsc.doctype.course_schedule.validate"
    # },
    # "Fees":{
    #     "on_submit":"wsc.wsc.doctype.fees.on_submit",
    #     "validate":"wsc.wsc.doctype.fees.validate",
    #     "on_cancel":"wsc.wsc.doctype.fees.on_cancel"
    # },
    # "Fee Structure":{
    #     "validate":"wsc.wsc.validations.fee_structure.validate"
    # },
    "File": {
		"validate": "wsc.wsc.validations.file.validate",
	},
    "Final Result Declaration":{
        "validate":"wsc.wsc.validations.final_result_declaration.validate"
    },
    "Instructor":{
        "validate":"wsc.wsc.validations.instructor.validate",
        "on_trash":"wsc.wsc.validations.instructor.on_trash"
    },
    "Mentor Allocation": {
        "validate": "wsc.wsc.validations.mentor_allocation.validate"
    },
    "Mentor Initiation": {
        "validate":"wsc.wsc.doctype.mentor_initiation.mentor_initiation.create_mentee_communications"
    },
    "Photocopy Application":{
        "validate":"wsc.wsc.validations.photocopy_application.validate"
    },
    "Placement Drive Application":{
        "validate":"wsc.wsc.validations.placement_drive_application.validate"
    },
    "Placement Drive":{
        "validate":"wsc.wsc.validations.placement_drive.validate"
    },
    "Post Exam Declaration":{
        "validate":"wsc.wsc.validations.post_exam_declaration.validate"
    },
    "Program":{
        "after_insert":"wsc.wsc.validations.program.after_insert",
        "validate":"wsc.wsc.validations.program.validate",
        "on_trash":"wsc.wsc.validations.program.on_trash"
    },
    "Programs":{
        "validate":"wsc.wsc.validations.programs.validate"
    },
    "Program Enrollment":{
        "on_submit":["wsc.wsc.validations.program_enrollment.on_submit"],
        "on_cancel":["wsc.wsc.validations.program_enrollment.on_cancel"],
        "on_change":"wsc.wsc.validations.program_enrollment.on_change",
        "validate":["wsc.wsc.validations.program_enrollment.validate",
                    "wsc.wsc.validations.program_enrollment.validate"]
    },
    "Reevaluation Application":{
        "validate":"wsc.wsc.validations.reevalution_application.validate"
    },
    "Student":{
        "after_insert":"wsc.wsc.validations.student.after_insert",
        "on_trash":"wsc.wsc.validations.student.on_trash",
        "on_change":["wsc.wsc.validations.student.on_update","wsc.wsc.validations.student.on_change"],
        "validate":"wsc.wsc.validations.student.validate"
    },
    "Student Admit Card":{
        "validate":"wsc.wsc.validations.student_admit_card.validate"
    },
    "Student Group":{
        "validate":["wsc.wsc.validations.student_group.validate","wsc.wsc.validations.student_group.validate"],
        "after_insert":"wsc.wsc.validations.student_group.after_insert",
        "on_trash":"wsc.wsc.validations.student_group.on_trash"
    },
    "Student Log":{
        "validate":"wsc.wsc.validations.student_log.validate"
    },
    "Student Exchange Applicant":{
        "validate":"wsc.wsc.validations.student_exchange_applicant.validate"
    },
    "Student Exam Block List":{
        "validate":"wsc.wsc.validations.student_exam_block_list.validate"
    },
    "Student Leave Application":{
        "validate":"wsc.wsc.validations.student_leave_application.validate"
    },
    "Student Applicant":{
    #     "validate":"wsc.wsc.doctype.student_applicant.validate",
        "on_change":"wsc.wsc.doctype.student_applicant.on_update"
    },
    "Student Admission":{
        "validate":"wsc.wsc.validations.student_admission.validate"
    },
    # "Student Attendance":{
    #     "validate":["wsc.wsc.doctype.student_attendance.validate"]
    # },
    ("Student Admit Card"):{
        "after_insert":"wsc.wsc.doctype.user_permission.after_insert",
        "on_trash":"wsc.wsc.doctype.user_permission.on_trash"
    },
    "Payment Entry": {
        "on_submit":["wsc.wsc.validations.fees_extention.on_submit",
					"wsc.wsc.validations.online_fees.on_submit"],
		"on_cancel":"wsc.wsc.validations.fees_extention.on_cancel",
		"validate": "wsc.wsc.validations.fees_extention.validate"
	},
    "Item Price":{
        "validate":"wsc.wsc.validations.item_price.validate"
    },
    "Shift Request":{
        "after_insert":"wsc.wsc.validations.shift_request.after_insert",
        "validate":"wsc.wsc.validations.shift_request.validate"
    },
    "Employee Grievance":{
        "validate":"wsc.wsc.validations.employee_grievance.validate",
    },
    "Employee Separation":{
        "validate":"wsc.wsc.validations.employee_separation.validate",
    },
    "Asset Maintenance" : {
        "validate" :"wsc.wsc.doctype.asset_maintenance.validate"
    } 

    # "User":{
    #     "validate":"wsc.wsc.validations.user.validate",
    # }
    # "Department":{
    #     "validate": "wsc.wsc.doctype.department.validate"
    # },
}

# Scheduled Tasks
# ---------------

scheduler_events = {

    # "cron":{
    #     "0 10 * * *" : [
    #         "wsc.task.warranty_notification",
    #         "wsc.task.safety_stock_reach"
    #     ]
    # },

    "daily": [
		"wsc.wsc.validations.student_blocklist_check.student_blocklist_check",
        "wsc.task.warranty_notification",
        "wsc.task.safety_stock_reach",
        "wsc.wsc.doctype.student_clearance_application.student_clearance_application.student_disable_check"
        # "wsc.wsc.validations.exam_assessment_plan.make_exam_paper_setting_by_paper_setting_date"
	]

}

# Testing
# -------

# before_tests = "wsc.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"education.education.api.get_course_schedule_events": "wsc.wsc.doctype.course_schedule.get_course_schedule_events",
    "education.education.api.mark_attendance": "wsc.wsc.doctype.student_attendance.mark_attendance",
    "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry":"wsc.wsc.doctype.payment_entry.get_payment_entry",	
	"erpnext.accounts.doctype.payment_entry.payment_entry.get_party_details":"wsc.wsc.doctype.payment_entry.get_party_details",
	"erpnext.accounts.doctype.payment_entry.payment_entry.get_account_details":"wsc.wsc.doctype.payment_entry.get_account_details",
	"erpnext.accounts.doctype.payment_entry.payment_entry.get_outstanding_reference_documents":"wsc.wsc.doctype.payment_entry.get_outstanding_reference_documents",
	"erpnext.accounts.doctype.payment_entry.payment_entry.get_company_defaults":"wsc.wsc.doctype.payment_entry.get_company_defaults",
	"erpnext.accounts.doctype.payment_entry.payment_entry.get_reference_details":"wsc.wsc.doctype.payment_entry.get_reference_details",
	"erpnext.accounts.doctype.payment_entry.payment_entry.get_party_and_account_balance":"wsc.wsc.doctype.payment_entry.get_party_and_account_balance",
	"education.education.api.get_fee_components":"wsc.wsc.validations.api.get_fee_components",
	"education.education.doctype.fee_structure.fee_structure.make_fee_schedule":"wsc.wsc.doctype.fee_structure.make_fee_schedule",
    "education.education.doctype.student_attendance_tool.student_attendance_tool.get_student_attendance_records":"wsc.wsc.doctype.student_attendance.get_student_attendance_records"
    # "frappe.core.doctype.data_import.data_import.download_template":"wsc.wsc.doctype.data_import.download_template"
	# "kp_edtec.kp_edtec.doctype.fees.make_refund_fees":"wsc.wsc.validations.fees.make_refund_fees",
}
override_doctype_class = {
    "Course Schedule":"wsc.wsc.doctype.course_schedule.CourseSchedule",
	"Course Scheduling Tool": "wsc.wsc.doctype.course_scheduling_tool.CourseSchedulingTool",
    "Employee":"wsc.wsc.doctype.employee.Employee",
    "Fee Structure":"wsc.wsc.doctype.fee_structure.FeeStructure",
    "Fees":"wsc.wsc.doctype.fees.Fees",
    "Payment Entry":"wsc.wsc.doctype.payment_entry.PaymentEntry",
    "Student Applicant": "wsc.wsc.doctype.student_applicant.StudentApplicant",
    "Student Attendance": "wsc.wsc.doctype.student_attendance.StudentAttendance",
    "User Permission": "wsc.wsc.doctype.user_permission.UserPermission",
    "Item": "wsc.wsc.validations.item.Item",
    "Leave Application":"wsc.wsc.doctype.leave_application.LeaveApplication"
    # "Job Applicant": "wsc.wsc.doctype.job_applicant.Job Applicant"
    # "Data Import": "wsc.wsc.doctype.data_import.DataImport"
}
override_doctype_dashboards = {
    "Program": "wsc.wsc.dashboard.program_dashboard.get_data",
    "Student Group": "wsc.wsc.dashboard.student_group_dashboard.get_data",
    "Academic Year": "wsc.wsc.dashboard.academic_year_dashboard.get_data",
    "Room": "wsc.wsc.dashboard.room_dashboard.get_data",
    "Instructor": "wsc.wsc.dashboard.instructor_dashboard.get_data",
    "Academic Term": "wsc.wsc.dashboard.academic_term_dashboard.get_data",
    "Course": "wsc.wsc.dashboard.course_dashboard.get_data",
    "Program Enrollment": "wsc.wsc.dashboard.program_enrollment_dashboard.get_data",
    "Student": "wsc.wsc.dashboard.student_dashboard.get_data",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"wsc.auth.validate"
# ]

# fixtures = [
# 	{"dt": "Custom DocPerm", "filters": [
# 		["parent", "not in", ["DocType"]],
#         ["role", '=', 'Education Admission Head']
# 	]},
    # {"dt": "Role","filters": [
    #     [
    #         "name", "in", ["Shift Approver","Grievance Cell Member"]
    #     ]
    # ]},
    # # {"dt": "Role Profile"},
    # # {"dt": "Module Profile"},
    # {"dt" : "Workflow","filters": [
    #     [
    #         "name", "in", ["Employee Shift Request Workflow","Job Requisition"]
    #     ]
    # ]},
    # # {"dt" : "Workflow"},
    # # {"dt": "Workflow Action Master"},
    # {"dt" : "Workflow State","filters": [
    #     [
    #         "name", "in", ["Resolved"]
    #     ]
    # ]},
    # {"dt" : "Translation"}
# ]
website_context = {
    "favicon": "/assets/wsc/images/wsc.png",
    "splash_image": "/assets/wsc/images/wsc.png"
}