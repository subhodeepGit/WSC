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
                "Bank Reconciliation Tool":"public/js/bank_reconciliation_tool.js",
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
                "Stock Settings":"public/js/stock_settings.js",
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
                "Bank Guarantee":"public/js/bank_guarantee.js",
                "Material Request":"public/js/material_request.js",
                "Attendance":"public/js/attendance.js",
                "Tax Category":"public/js/tax_category.js",
                "Employee Grievance":"public/js/employee_grievance.js",
                "Employee Onboarding":"public/js/employee_onboarding.js",
                "Job Offer":"public/js/job_offer.js",
                "Compensatory Leave Request":"public/js/compensatory_leave_request.js",
                "Task":"public/js/task.js",
                "Price List":"public/js/price_list.js",
                "Supplier":"public/js/supplier.js",
                "Request for Quotation":"public/js/request_for_quotation.js",
                "Purchase Order":"public/js/purchase_order.js",
                "Purchase Receipt":"public/js/purchase_receipt.js",
                "Purchase Invoice":"public/js/purchase_invoice.js",
                "Warehouse":"public/js/warehouse.js",
                "Asset":"public/js/asset.js",
                "Job Requisition":"public/js/job_requisition.js",
                "Project":"public/js/project.js",
                "Supplier Quotation":"public/js/supplier_quotation.js",
                "Stock Entry":"public/js/stock_entry.js",
                "Topic":"public/js/topic.js"
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
    "Student":"public/js/student_list.js",
    "Student Group":"public/js/student_group_list.js",
    "Employee Grievance":"public/js/employee_grievance_list.js",
    "Item Price":"public/js/item_price_list.js",
    "Material Request":"public/js/material_request_list.js",
    "Price List":"public/js/price_list_list.js",
    "Course Schedule":"public/js/course_schedule_list.js",
    "Program":"public/js/program_list.js",
    "Employment Type":"public/js/employment_type_list.js",
    "Branch":"public/js/branch_list.js",
    "Employee Grade":"public/js/employee_grade_list.js",
    "Department":"public/js/department_list.js",
    "Designation":"public/js/designation_list.js",
    "Employee Group":"public/js/employee_group_list.js",
    "Shift Request":"public/js/shift_request_list.js",
    "Employee Skill Map":"public/js/employee_skill_map_list.js",
    "Employee Appraisal Portal":"public/js/employee_appraisal_portal_list.js",
    "Employee Appraisal Cycle":"public/js/employee_appraisal_cycle_list.js",
    "Employee Appraisal Evaluation Template":"public/js/employee_appraisal_evalaution_template_list.js",
    "Dimenssions for Appraisal":"public/js/dimenssions_for_appraisal_list.js",
    "Appraisal":"public/js/appraisal_list.js",
    "Staffing Plan":"public/js/staffing_plan.js"
}

doctype_tree_js = {"doctype" : "public/js/tax_category_tree.js"}

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
        'wsc.patches.create_all_tax_category.execute',
        'wsc.wsc.wsc_patches.execute',
        # 'wsc.wsc.wsc_patches.execute_security_patches'
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
    "Company":{
        "validate":"wsc.wsc.validations.company.validate"
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
    "Grading Scale":{
        "validate":"wsc.wsc.validations.grading_scale.validate"
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
    # "Mentor Initiation": {
    #     "validate":"wsc.wsc.doctype.mentor_initiation.mentor_initiation.create_mentee_communications"
    # },
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
    "Room":{
        "validate":"wsc.wsc.validations.room.validate"
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
        "after_insert":"wsc.wsc.validations.employee_separation.after_insert",
        "on_cancel":"wsc.wsc.validations.employee_separation.on_cancel",
        "on_submit":"wsc.wsc.validations.employee_separation.on_submit"
        # "on_update_after_submit":"wsc.wsc.validations.employee_separation.on_update_after_submit"

        # "on_submit":"wsc.wsc.validations.employee_separation.on_submit"
    },
    "Asset Maintenance" : {
        "validate" :"wsc.wsc.doctype.asset_maintenance.validate"
    },
    "Attendance Request" :{
        "validate":"wsc.wsc.doctype.attendance_request.validate",
        "after_insert":"wsc.wsc.doctype.attendance_request.after_insert"
    },
    "Purchase Order": {
        "validate":"wsc.wsc.doctype.purchase_order.validate"
    },
    "Material Request": {
        "validate":"wsc.wsc.doctype.material_request.validate",
        "on_submit":"wsc.wsc.doctype.material_request.workflow_notification",
        "on_update_after_submit":"wsc.wsc.doctype.material_request.workflow_notification"
    },
    "Shift Type": {
        "validate":"wsc.wsc.validations.shift_type.validate"
    },
    "Shift Assignment": {
        "on_change":"wsc.wsc.validations.shift_assignment.on_change"
    },
    "Leave Type": {
        "validate":"wsc.wsc.validations.leave_type.validate"
    },
    "Leave Policy": {
        "validate":"wsc.wsc.doctype.leave_policy.validate"
    },
    "Leave Policy Assignment": {
        "validate":"wsc.wsc.validations.leave_policy_assignment.validate"
    },
    "Leave Allocation": {
        "validate":"wsc.wsc.doctype.leave_allocation.validate"
    },
    "Job Applicant": {
        "validate":"wsc.wsc.doctype.job_applicant.validate",
        "on_change":"wsc.wsc.doctype.job_applicant.on_change",
        "on_update":"wsc.wsc.doctype.job_applicant.on_update",
        "on_update_after_submit":"wsc.wsc.doctype.job_applicant.on_update_after_submit"
    },
    # "Task": {
    #     "validate":"wsc.task.validate"
    # },
    "Employee Onboarding": {
        "validate":"wsc.wsc.doctype.employee_onboarding.validate",
        "on_cancel" : "wsc.wsc.doctype.employee_onboarding.on_cancel",
        "on_submit":"wsc.wsc.doctype.employee_onboarding.on_submit"
        # "on_change" : "wsc.wsc.doctype.employee_onboarding.on_change",

    },
    "Compensatory Leave Request":{
        "validate":"wsc.wsc.doctype.compensatory_leave_request.validate",
        "on_change":"wsc.wsc.doctype.compensatory_leave_request.on_change",
    },
    "Task":
    {
        "validate":"wsc.wsc.doctype.task.validate"
    },
    "Job Requisition":{
        "validate":"wsc.wsc.doctype.job_requisition.validate"
    },
    "Item Group":{
        "validate":"wsc.wsc.validations.item_group.validate"
    },
    "Item":{
        "validate":"wsc.wsc.doctype.item.validate"
    },
    "Price List":{
        "validate":"wsc.wsc.validations.price_list.validate"
    },
    "Supplier":{
        "validate":"wsc.wsc.validations.supplier.validate"
    },
    "Quality Inspection Template":{
        "validate":"wsc.wsc.validations.quality_inspection_template.validate"
    },
    "Purchase Taxes and Charges Template":{
        "validate":"wsc.wsc.validations.purchase_taxes_and_charges_template.validate"
    },
    "Warehouse":{
    "validate":"wsc.wsc.validations.warehouse.validate"
    },
    "Tax Withholding Category":{
        "validate":"wsc.wsc.validations.tax_withholding_category.validate"
    },
    "Buying Settings":{
        "validate":"wsc.wsc.validations.buying_settings.validate"
    },
    "Batch":{
        "validate":"wsc.wsc.validations.batch.validate"
    },
    "Payment Term":{
        "validate":"wsc.wsc.validations.payment_term.validate"
    },
    "Payment Terms Template":{
        "validate":"wsc.wsc.validations.payment_terms_template.validate"
    },
    "Stock Entry":{
        "validate":"wsc.wsc.validations.stock_entry.validate"
    },
    "Request for Quotation":{
        "validate":"wsc.wsc.validations.request_for_quotation.validate"
    },
    "Supplier Quotation":{
        "validate":"wsc.wsc.validations.supplier_quotation.validate"
    },
    "Income Tax Slab":{
        "validate":"wsc.wsc.doctype.income_tax_slab.validate"
    },
    "Salary Structure Assignment":{
        "validate":"wsc.wsc.doctype.salary_structure_assignment.validate"
    },
    "Payroll Entry":{
        "validate":"wsc.wsc.doctype.payroll_entry.validate"
    },
    "Employee Tax Exemption Category":{
        "validate":"wsc.wsc.doctype.employee_tax_exemption_category.validate"
    },
    "Employee Tax Exemption Declaration":{
        "validate":"wsc.wsc.doctype.employee_tax_exemption_declaration.validate"
    },
    "Employee Benefit Claim":{
        "validate":"wsc.wsc.doctype.employee_benefit_claim.validate"
    },
    "Employee Benefit Application":{
        "validate":"wsc.wsc.doctype.employee_benefit_application.validate"
    },
    "Employee Incentive":{
        "validate":"wsc.wsc.doctype.employee_incentive.validate"
    },
    "Retention Bonus":{
        "validate":"wsc.wsc.doctype.retention_bonus.validate"
    },
    "Additional Salary":{
        "validate":"wsc.wsc.doctype.additional_salary.validate"
    },
    "Employee Other Income":{
        "validate":"wsc.wsc.doctype.employee_other_income.validate"
    },
    "Employee Tax Exemption Proof Submission":{
        "validate":"wsc.wsc.doctype.employee_tax_exemption_proof_submission.validate"
    },
    "Purchase Receipt":{
        "validate":"wsc.wsc.validations.purchase_receipt.validate"
    },
    "Purchase Invoice":{
        "validate":"wsc.wsc.validations.purchase_invoice.validate"
    },
    "Project":{
        "after_insert":"wsc.wsc.validations.project.after_insert"
    },
    "Salary Component": {
        "validate": "wsc.wsc.doctype.salary_component.validate"
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

    "cron":{
        "* * * * *" : [
            # "wsc.task.warranty_notification",
            # "wsc.task.safety_stock_reach",
            # "wsc.task.appraisal_reminder"
        ],
        "0 1 * * *" : [
            "wsc.task.await_transaction_update_status"
        ],
        "0 7 * * *" : [
            "wsc.task.await_transaction_update_status"
        ],
        # "0 3 * * *" : [
        #     "wsc.task.axis_transaction_update_status"       #AXIS Transaction status update
        # ]
    },

    "daily": [
		"wsc.wsc.validations.student_blocklist_check.student_blocklist_check",
        "wsc.task.warranty_notification",
        "wsc.task.safety_stock_reach",
        "wsc.task.student_disable_check",
        "wsc.task.employee_re_engagement_workFlow",
        "wsc.task.check_and_delete_exit_employee_permissions",
        "wsc.task.overdue_task",
        "wsc.task.status_update"
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
    "education.education.api.enroll_student": "wsc.wsc.doctype.student_applicant.enroll_student",
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
    "education.education.doctype.student_attendance_tool.student_attendance_tool.get_student_attendance_records":"wsc.wsc.doctype.student_attendance.get_student_attendance_records",
    # "frappe.core.doctype.data_import.data_import.download_template":"wsc.wsc.doctype.data_import.download_template"
	"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.auto_reconcile_vouchers":"wsc.wsc.validations.bank_reconciliation_tool.auto_reconcile_vouchers"
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
    "Leave Application":"wsc.wsc.doctype.leave_application.LeaveApplication",
    "Job Offer":"wsc.wsc.doctype.job_offer.JobOffer",
    "Appointment Letter":"wsc.wsc.doctype.appointment_letter.AppointmentLetter",
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
    "Item":"wsc.wsc.dashboard.item_dashboard.get_data",
    "Supplier":"wsc.wsc.dashboard.supplier_dashboard.get_data",
    "Payment Term":"wsc.wsc.dashboard.payment_term_dashboard.get_data",
    "Payment Terms Template":"wsc.wsc.dashboard.payment_term_template_dashboard.get_data",
    "Purchase Taxes and Charges Template": "wsc.wsc.dashboard.purchase_taxes_and_charges_template.get_data",
    "Tax Category":"wsc.wsc.dashboard.all_tax_category_dashboard.get_data",
    "Material Request":"wsc.wsc.dashboard.material_request.get_data",
    "Supplier Quotation":"wsc.wsc.dashboard.supplier_quotation_dashbord.get_data",
    "Purchase Order":"wsc.wsc.dashboard.purchase_order_dashboard.get_data",
    "Purchase Receipt":"wsc.wsc.dashboard.purchase_receipt_dashboard.get_data",
    "Purchase Invoice":"wsc.wsc.dashboard.purchase_invoice_dashboard.get_data",
    "Batch":"wsc.wsc.dashboard.batch_dashboard.get_data",
    # "Asset":"wsc.wsc.dashboard.asset_dashboard.get_data",
    "Project":"wsc.wsc.dashboard.project_dashboard.get_data",
    "Task":"wsc.wsc.dashboard.task_dashboard.get_data",
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
#         ["parent", "in", ["Entrance Exam Declaration"]],
#         ["role", "in", ["Applicant"]]
# 	]},
    # {"dt": "Role","filters": [
    #     ["name", "in", ["Project Manager"]]
    # ]},
    # # {"dt": "Role Profile"},
#     # # {"dt": "Module Profile"},
    # {"dt" : "Workflow","filters": [
    #     [
    #         "name", "in", ["Employee Separation Workflow"]
    #     ]
    # ]},
    # {"dt" : "Workflow"},
    # # {"dt": "Workflow Action Master"},
    # {"dt" : "Workflow State","filters": [
    #     [
    #         "name", "in", ["Resolved"]
    #     ]
    # ]},
#     {"dt" : "Translation","filters": [
#         [
#             "source_text", "in", ["Department Email ID"]
#         ]
    # ]}
#  ]
website_context = {
    "favicon": "/assets/wsc/images/wsc.png",
    "splash_image": "/assets/wsc/images/wsc.png"
}