import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, date_diff, getdate

from erpnext.setup.doctype.employee.employee import is_holiday

from hrms.hr.utils import validate_active_employee, validate_dates
# from wsc.wsc.notification.custom_notification import send_mail_to_reporting,send_mail_to_hr_updation
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions


def on_submit(doc,method):
		print("\n\n\n\nMy code")
		create_new_attendance(doc)

def create_new_attendance(doc):
		
		#First get the attendance and delete the record .
		doc_name = frappe.db.get_value("Attendance", {"attendance_request": doc.name})
		if doc_name:
		# Delete the document
			attendance_doc = frappe.get_doc("Attendance", doc_name)
			attendance_doc.cancel()
			frappe.delete_doc("Attendance", doc_name)

		request_days = date_diff(doc.to_date, doc.from_date) + 1
		for number in range(request_days):
			attendance_date = add_days(doc.from_date, number)
			skip_attendance = doc.validate_if_attendance_not_applicable(attendance_date)
			if not skip_attendance:
				attendance = frappe.new_doc("Attendance")
				attendance.employee = doc.employee
				attendance.employee_name = doc.employee_name
				if doc.half_day and date_diff(getdate(doc.half_day_date), getdate(attendance_date)) == 0:
					attendance.status = "Half Day"
				elif doc.reason == "Work From Home":
					attendance.status = "Work From Home"
				else:
					attendance.status = "Present"
				# if doc.late_entry == 1:
				# 	attendance.status="Present (Late Entry)"
				# if doc.early_exit==1:
				# 	attendance.status == "Present (Early Exit)"
				attendance.late_entry= doc.late_entry
				attendance.early_exit = doc.early_exit
				attendance.attendance_date = attendance_date
				attendance.company = doc.company
				attendance.attendance_request = doc.name
				attendance.save(ignore_permissions=True)
				attendance.submit()


def approver_mail(doc):
	reporting_auth_id = doc.reporting_authority_id
	print("reporting_auth_id",reporting_authority_id)
	if reporting_auth_id:
		data={}
		data["reporting_authority_email"]=reporting_auth_id
		data["employee_name"]=doc.employee_name
		data["current_status"]=doc.workflow_state
		data["name"]=doc.name
		send_mail_to_reporting(data)
	else :
		frappe.throw("Setup the user id of the reporting authority {}".format(doc.reporting_authority_id))

def validate(doc,method):
	pass
		
		# print(self.workflow_state)
		# if doc.workflow_state =="Pending Approval":
		# 	approver_mail(doc)
		# if doc.workflow_state=="Forwarded to HR":
		# 	send_mail_to_hr(doc)

def send_mail_to_hr(doc):
		hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
		if hr_mail:
			hr_mail_id = hr_mail[0]
			data = {}
			data["hr_mail"] = hr_mail_id
			data["employee_name"]=doc.employee_name
			data["current_status"]=doc.workflow_state
			data["name"]=doc.name
			send_mail_to_hr_updation(data)
			
		else :
			frappe.throw("Setup HR Admin User ID")

#Code for user restrictions for reporting authority.

def after_insert(doc,method):
	print("\n\n\nUser Permission")
	set_user_permission(doc)
def set_user_permission(doc):
	if doc.reporting_authority_id:
		set_attendance_request_permission_reporting_authority(doc)
	
def on_trash(doc):
	delete_permission(doc)
def delete_permission(doc):
	for d in frappe.get_all("User Permission",{"reference_doctype":doc.doctype,"reference_docname":doc.name}):
		frappe.delete_doc("User Permission",d.name)
def set_attendance_request_permission_reporting_authority(doc):
	for emp in frappe.get_all("Employee", {'reporting_authority_email':doc.reporting_authority_id}, ['reporting_authority_email']):
		if emp.get('reporting_authority_email'):
			print(emp.get('reporting_authority_email'))
			add_user_permission("Attendance Request",doc.name, emp.get('reporting_authority_email'), doc)
		else:
			frappe.msgprint("Reporting Authority Not Found")

#code to hide the action button

@frappe.whitelist()
def is_verified_user(docname):
	# if frappe.db.exists(docname):

	doc = frappe.get_doc("Attendance Request",docname)
	# emp_user_id = frappe.get_all("Employee",{"name":doc.employee},["user_id"])
	# if emp_user_id:
	# 	employee_user_id = emp_user_id[0]["user_id"]
	reporting_auth_id = doc.reporting_auth_id
	roles = frappe.get_roles(frappe.session.user)

	if "HR Manager/CS Officer" in roles or "HR Admin" in roles or "Director" in roles or "Admin" in roles or "Administrator" in roles:
		return True
	if doc.workflow_state == "Pending Approval" and frappe.session.user ==reporting_authority_id:
		return True
	else :
		return False