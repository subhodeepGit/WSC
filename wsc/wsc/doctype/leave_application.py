import datetime
from typing import Dict, Optional, Tuple, Union

import frappe
from frappe import _
from frappe.query_builder.functions import Max, Min, Sum
from frappe.utils import (
	add_days,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_fullname,
	get_link_to_form,
	getdate,
	nowdate,
)

from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import daterange
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee

from hrms.hr.doctype.leave_block_list.leave_block_list import get_applicable_block_dates
from hrms.hr.doctype.leave_ledger_entry.leave_ledger_entry import create_leave_ledger_entry
from hrms.hr.utils import (
	get_holiday_dates_for_employee,
	get_leave_period,
	set_employee_name,
	share_doc_with_approver,
	validate_active_employee,
)
from wsc.wsc.notification.custom_notification import employee_reporting_aproverr
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions


class LeaveDayBlockedError(frappe.ValidationError):
	pass


class OverlapError(frappe.ValidationError):
	pass


class AttendanceAlreadyMarkedError(frappe.ValidationError):
	pass


class NotAnOptionalHoliday(frappe.ValidationError):
	pass


class InsufficientLeaveBalanceError(frappe.ValidationError):
	pass


class LeaveAcrossAllocationsError(frappe.ValidationError):
	pass


from frappe.model.document import Document


class LeaveApplication(Document):
	def get_feed(self):
		return _("{0}: From {0} of type {1}").format(self.employee_name, self.leave_type)

	def approver_mail(self):
		data={}
		data["reporting_authority_email"]=self.reporting_authority_email
		data["employee_name"]=self.employee_name
		data["leave_type"]=self.leave_type
		data["current_status"]=self.current_status
		data["from_date"]=self.from_date
		data["to_date"]=self.to_date
		data["name"]=self.name
		employee_reporting_aproverr(data)
	def after_insert(self):
		print("\n\n\nHello Workld")
		self.set_shift_request_permission_reporting_authority()
	def validate(self):
		validate_active_employee(self.employee)
		set_employee_name(self)
		# set_user_permission(self)
		
		# self.validate_dates()
		# self.validate_balance_leaves()
		self.validate_leave_overlap()
		# self.set_shift_request_permission_reporting_authority()
		self.set_shift_request_permission_approver()
		if self.current_status == "Open":
			self.approver_mail()
		self.show_block_day_warning()
		self.validate_block_days()
		self.validate_salary_processed_days()
		self.validate_attendance()
		self.set_half_day_date()
		if frappe.db.get_value("Leave Type", self.leave_type, "is_optional_leave"):
			self.validate_optional_leave()
		self.validate_applicable_after()
		# session_user_employee_code = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")
		# if session_user_employee_code == self.employee:
		# 	pass
		# else:
		# 	raise frappe.throw("You are not allowed to create leave applications for other employees.")
		print("\n\n\nCurrent Status",self.current_status)
	
	def on_update(self):
		if self.current_status == "Forwarded to Approving Authority":
			# notify leave approver about creation
			if frappe.db.get_single_value("HR Settings", "send_leave_notification"):
				self.notify_leave_approver()

			share_doc_with_approver(self, self.leave_approver)
	  

	def on_submit(self):
		if self.status in ["Open", "Cancelled"]:
			frappe.throw(
				_("Only Leave Applications with status 'Approved' and 'Rejected' can be submitted")
			)

		self.validate_back_dated_application()
		self.update_attendance()

		# notify leave applier about approval
		if frappe.db.get_single_value("HR Settings", "send_leave_notification"):
			self.notify_employee()

		self.create_leave_ledger_entry()
		self.reload()

	# def approver_mail(self):
	#     data={}
	#     data["reporting_authority_email"]=self.reporting_authority_email
	#     employee_reporting_aprover(data)

			

	def before_cancel(self):
		self.status = "Cancelled"

	def on_cancel(self):
		self.create_leave_ledger_entry(submit=False)
		# notify leave applier about cancellation
		if frappe.db.get_single_value("HR Settings", "send_leave_notification"):
			self.notify_employee()
		self.cancel_attendance()
	
# def on_trash(self):
# 	self.delete_permission()
	
# def delete_permission(self):
# 	for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
# 		frappe.delete_doc("User Permission",d.name)
	
	def set_shift_request_permission_reporting_authority(doc):
		data={}
		# data["reporting_authority_email"]=self.reporting_authority_email
		if doc.reporting_authority_email:
			print("\n\n\nEmail")
			print(doc.reporting_authority_email)
			for emp in frappe.get_all("Employee", {'reporting_authority_email':doc.reporting_authority_email}, ['reporting_authority_email']):
				print(emp.reporting_authority_email)
				if emp.reporting_authority_email:
					print("\n\n\nIDD")
					print(emp.reporting_authority_email)
					data["reporting_authority_email"]=emp.reporting_authority_email
					add_user_permission(doc.doctype,doc.name,data["reporting_authority_email"],doc)	
				else:
					frappe.msgprint("Reporting Authority Not Found")


	def set_shift_request_permission_approver(doc):
		if doc.current_status=="Forwarded to Approving Authority":
			for emp in frappe.get_all("Employee", {'leave_approver':doc.leave_approver}, ['leave_approver']):
				if emp.leave_approver:
					print(emp.leave_approver)
					add_user_permission(doc.doctype,doc.name,emp.leave_approver,doc)	
					# add_user_permission("Shift Request",doc.name, emp.get('shift_request_approver'), doc)
				else:
					frappe.msgprint("Shift Request Not Found")	

	def validate_applicable_after(self):
		if self.leave_type:
			leave_type = frappe.get_doc("Leave Type", self.leave_type)
			if leave_type.applicable_after > 0:
				date_of_joining = frappe.db.get_value("Employee", self.employee, "date_of_joining")
				leave_days = get_approved_leaves_for_period(
					self.employee, False, date_of_joining, self.from_date
				)
				number_of_days = date_diff(getdate(self.from_date), date_of_joining)
				if nsuku@gmail.comumber_of_days >= 0:
					holidays = 0
					if not frappe.db.get_value("Leave Type", self.leave_type, "include_holiday"):
						holidays = get_holidays(self.employee, date_of_joining, self.from_date)
					number_of_days = number_of_days - leave_days - holidays
					if number_of_days < leave_type.applicable_after:
						frappe.throw(
							_("{0} applicable after {1} working days").format(
								self.leave_type, leave_type.applicable_after
							)
						)

	def validate_dates(self):
		if frappe.db.get_single_value("HR Settings", "restrict_backdated_leave_application"):
			if self.from_date and getdate(self.from_date) < getdate():
				allowed_role = frappe.db.get_single_value(
					"HR Settings", "role_allowed_to_create_backdated_leave_application"
				)
				user = frappe.get_doc("User", frappe.session.user)
				user_roles = [d.role for d in user.roles]
				if not allowed_role:
					frappe.throw(
						_("Backdated Leave Application is restricted. Please set the {} in {}").format(
							frappe.bold("Role Allowed to Create Backdated Leave Application"),
							get_link_to_form("HR Settings", "HR Settings"),
						)
					)

				if allowed_role and allowed_role not in user_roles:
					frappe.throw(
						_("Only users with the {0} role can create backdated leave applications").format(
							allowed_role
						)
					)

		if self.from_date and self.to_date and (getdate(self.to_date) < getdate(self.from_date)):
			frappe.throw(_("To date cannot be before from date"))

		if (
			self.half_day
			and self.half_day_date
			and (
				getdate(self.half_day_date) < getdate(self.from_date)
				or getdate(self.half_day_date) > getdate(self.to_date)
			)
		):

			frappe.throw(_("Half Day Date should be between From Date and To Date"))

		if not is_lwp(self.leave_type):
			self.validate_dates_across_allocation()
			self.validate_back_dated_application()

	def validate_dates_across_allocation(self):
		if frappe.db.get_value("Leave Type", self.leave_type, "allow_negative"):
			return

		alloc_on_from_date, alloc_on_to_date = self.get_allocation_based_on_application_dates()

		if not (alloc_on_from_date or alloc_on_to_date):
			frappe.throw(_("Application period cannot be outside leave allocation period"))
		elif self.is_separate_ledger_entry_required(alloc_on_from_date, alloc_on_to_date):
			frappe.throw(
				_("Application period cannot be across two allocation records"),
				exc=LeaveAcrossAllocationsError,
			)

	def get_allocation_based_on_application_dates(self) -> Tuple[Dict, Dict]:
		"""Returns allocation name, from and to dates for application dates"""

		def _get_leave_allocation_record(date):
			LeaveAllocation = frappe.qb.DocType("Leave Allocation")
			allocation = (
				frappe.qb.from_(LeaveAllocation)
				.select(LeaveAllocation.name, LeaveAllocation.from_date, LeaveAllocation.to_date)
				.where(
					(LeaveAllocation.employee == self.employee)
					& (LeaveAllocation.leave_type == self.leave_type)
					& (LeaveAllocation.docstatus == 1)
					& ((date >= LeaveAllocation.from_date) & (date <= LeaveAllocation.to_date))
				)
			).run(as_dict=True)

			return allocation and allocation[0]

		allocation_based_on_from_date = _get_leave_allocation_record(self.from_date)
		allocation_based_on_to_date = _get_leave_allocation_record(self.to_date)

		return allocation_based_on_from_date, allocation_based_on_to_date

	def validate_back_dated_application(self):
		future_allocation = frappe.db.sql(
			"""select name, from_date from `tabLeave Allocation`
			where employee=%s and leave_type=%s and docstatus=1 and from_date > %s
			and carry_forward=1""",
			(self.employee, self.leave_type, self.to_date),
			as_dict=1,
		)

		if future_allocation:
			frappe.throw(
				_(
					"Leave cannot be applied/cancelled before {0}, as leave balance has already been carry-forwarded in the future leave allocation record {1}"
				).format(formatdate(future_allocation[0].from_date), future_allocation[0].name)
			)

	def update_attendance(self):
		if self.status != "Approved":
			return

		holiday_dates = []
		if not frappe.db.get_value("Leave Type", self.leave_type, "include_holiday"):
			holiday_dates = get_holiday_dates_for_employee(self.employee, self.from_date, self.to_date)

		for dt in daterange(getdate(self.from_date), getdate(self.to_date)):
			date = dt.strftime("%Y-%m-%d")
			attendance_name = frappe.db.exists(
				"Attendance", dict(employee=self.employee, attendance_date=date, docstatus=("!=", 2))
			)

			# don't mark attendance for holidays
			# if leave type does not include holidays within leaves as leaves
			if date in holiday_dates:
				if attendance_name:
					# cancel and delete existing attendance for holidays
					attendance = frappe.get_doc("Attendance", attendance_name)
					attendance.flags.ignore_permissions = True
					if attendance.docstatus == 1:
						attendance.cancel()
					frappe.delete_doc("Attendance", attendance_name, force=1)
				continue

			self.create_or_update_attendance(attendance_name, date)

	def create_or_update_attendance(self, attendance_name, date):
		status = (
			"Half Day"
			if self.half_day_date and getdate(date) == getdate(self.half_day_date)
			else "On Leave"
		)

		if attendance_name:
			# update existing attendance, change absent to on leave
			doc = frappe.get_doc("Attendance", attendance_name)
			if doc.status != status:
				doc.db_set({"status": status, "leave_type": self.leave_type, "leave_application": self.name})
		else:
			# make new attendance and submit it
			doc = frappe.new_doc("Attendance")
			doc.employee = self.employee
			doc.employee_name = self.employee_name
			doc.attendance_date = date
			doc.company = self.company
			doc.leave_type = self.leave_type
			doc.leave_application = self.name
			doc.status = status
			doc.flags.ignore_validate = True
			doc.insert(ignore_permissions=True)
			doc.submit()

	def cancel_attendance(self):
		if self.docstatus == 2:
			attendance = frappe.db.sql(
				"""select name from `tabAttendance` where employee = %s\
				and (attendance_date between %s and %s) and docstatus < 2 and status in ('On Leave', 'Half Day')""",
				(self.employee, self.from_date, self.to_date),
				as_dict=1,
			)
			for name in attendance:
				frappe.db.set_value("Attendance", name, "docstatus", 2)

	def validate_salary_processed_days(self):
		if not frappe.db.get_value("Leave Type", self.leave_type, "is_lwp"):
			return

		last_processed_pay_slip = frappe.db.sql(
			"""
			select start_date, end_date from `tabSalary Slip`
			where docstatus = 1 and employee = %s
			and ((%s between start_date and end_date) or (%s between start_date and end_date))
			order by modified desc limit 1
		""",
			(self.employee, self.to_date, self.from_date),
		)

		if last_processed_pay_slip:
			frappe.throw(
				_(
					"Salary already processed for period between {0} and {1}, Leave application period cannot be between this date range."
				).format(
					formatdate(last_processed_pay_slip[0][0]), formatdate(last_processed_pay_slip[0][1])
				)
			)

	def show_block_day_warning(self):
		block_dates = get_applicable_block_dates(
			self.from_date,
			self.to_date,
			self.employee,
			self.company,
			all_lists=True,
			leave_type=self.leave_type,
		)

		if block_dates:
			frappe.msgprint(_("Warning: Leave application contains following block dates") + ":")
			for d in block_dates:
				frappe.msgprint(formatdate(d.block_date) + ": " + d.reason)

	def validate_block_days(self):
		block_dates = get_applicable_block_dates(
			self.from_date, self.to_date, self.employee, self.company, leave_type=self.leave_type
		)

		if block_dates and self.status == "Approved":
			frappe.throw(_("You are not authorized to approve leaves on Block Dates"), LeaveDayBlockedError)

	def validate_balance_leaves(self):
		if self.from_date and self.to_date:
			self.total_leave_days = get_number_of_leave_days(
				self.employee, self.leave_type, self.from_date, self.to_date, self.half_day, self.half_day_date
			)

			if self.total_leave_days <= 0:
				frappe.throw(
					_(
						"The day(s) on which you are applying for leave are holidays. You need not apply for leave."
					)
				)

			if not is_lwp(self.leave_type):
				leave_balance = get_leave_balance_on(
					self.employee,
					self.leave_type,
					self.from_date,
					self.to_date,
					consider_all_leaves_in_the_allocation_period=True,
					for_consumption=True,
				)
				self.leave_balance = leave_balance.get("leave_balance")
				leave_balance_for_consumption = leave_balance.get("leave_balance_for_consumption")

				if self.status != "Rejected" and (
					leave_balance_for_consumption < self.total_leave_days or not leave_balance_for_consumption
				):
					self.show_insufficient_balance_message(leave_balance_for_consumption)

	def show_insufficient_balance_message(self, leave_balance_for_consumption: float) -> None:
		alloc_on_from_date, alloc_on_to_date = self.get_allocation_based_on_application_dates()

		if frappe.db.get_value("Leave Type", self.leave_type, "allow_negative"):
			if leave_balance_for_consumption != self.leave_balance:
				msg = _("Warning: Insufficient leave balance for Leave Type {0} in this allocation.").format(
					frappe.bold(self.leave_type)
				)
				msg += "<br><br>"
				msg += _(
					"Actual balances aren't available because the leave application spans over different leave allocations. You can still apply for leaves which would be compensated during the next allocation."
				)
			else:
				msg = _("Warning: Insufficient leave balance for Leave Type {0}.").format(
					frappe.bold(self.leave_type)
				)

			frappe.msgprint(msg, title=_("Warning"), indicator="orange")
		else:
			frappe.throw(
				_("Insufficient leave balance for Leave Type {0}").format(frappe.bold(self.leave_type)),
				exc=InsufficientLeaveBalanceError,
				title=_("Insufficient Balance"),
			)

	def validate_leave_overlap(self):
		if not self.name:
			# hack! if name is null, it could cause problems with !=
			self.name = "New Leave Application"

		for d in frappe.db.sql(
			"""
			select
				name, leave_type, posting_date, from_date, to_date, total_leave_days, half_day_date
			from `tabLeave Application`
			where employee = %(employee)s and docstatus < 2 and status in ('Open', 'Approved')
			and to_date >= %(from_date)s and from_date <= %(to_date)s
			and name != %(name)s""",
			{
				"employee": self.employee,
				"from_date": self.from_date,
				"to_date": self.to_date,
				"name": self.name,
			},
			as_dict=1,
		):

			if (
				cint(self.half_day) == 1
				and getdate(self.half_day_date) == getdate(d.half_day_date)
				and (
					flt(self.total_leave_days) == 0.5
					or getdate(self.from_date) == getdate(d.to_date)
					or getdate(self.to_date) == getdate(d.from_date)
				)
			):

				total_leaves_on_half_day = self.get_total_leaves_on_half_day()
				if total_leaves_on_half_day >= 1:
					self.throw_overlap_error(d)
			else:
				self.throw_overlap_error(d)

	def throw_overlap_error(self, d):
		form_link = get_link_to_form("Leave Application", d.name)
		msg = _("Employee {0} has already applied for {1} between {2} and {3} : {4}").format(
			self.employee, d["leave_type"], formatdate(d["from_date"]), formatdate(d["to_date"]), form_link
		)
		frappe.throw(msg, OverlapError)

	def get_total_leaves_on_half_day(self):
		leave_count_on_half_day_date = frappe.db.sql(
			"""select count(name) from `tabLeave Application`
			where employee = %(employee)s
			and docstatus < 2
			and status in ('Open', 'Approved')
			and half_day = 1
			and half_day_date = %(half_day_date)s
			and name != %(name)s""",
			{"employee": self.employee, "half_day_date": self.half_day_date, "name": self.name},
		)[0][0]

		return leave_count_on_half_day_date * 0.5

	def validate_max_days(self):
		max_days = frappe.db.get_value("Leave Type", self.leave_type, "max_continuous_days_allowed")
		if max_days and self.total_leave_days > cint(max_days):
			frappe.throw(_("Leave of type {0} cannot be longer than {1}").format(self.leave_type, max_days))

	def validate_attendance(self):
		attendance = frappe.db.sql(
			"""select name from `tabAttendance` where employee = %s and (attendance_date between %s and %s)
					and status = 'Present' and docstatus = 1""",
			(self.employee, self.from_date, self.to_date),
		)
		if attendance:
			frappe.throw(
				_("Attendance for employee {0} is already marked for this day").format(self.employee),
				AttendanceAlreadyMarkedError,
			)

	def validate_optional_leave(self):
		leave_period = get_leave_period(self.from_date, self.to_date, self.company)
		if not leave_period:
			frappe.throw(_("Cannot find active Leave Period"))
		optional_holiday_list = frappe.db.get_value(
			"Leave Period", leave_period[0]["name"], "optional_holiday_list"
		)
		if not optional_holiday_list:
			frappe.throw(
				_("Optional Holiday List not set for leave period {0}").format(leave_period[0]["name"])
			)
		day = getdate(self.from_date)
		while day <= getdate(self.to_date):
			if not frappe.db.exists(
				{"doctype": "Holiday", "parent": optional_holiday_list, "holiday_date": day}
			):
				frappe.throw(
					_("{0} is not in Optional Holiday List").format(formatdate(day)), NotAnOptionalHoliday
				)
			day = add_days(day, 1)

	def set_half_day_date(self):
		if self.from_date == self.to_date and self.half_day == 1:
			self.half_day_date = self.from_date

		if self.half_day == 0:
			self.half_day_date = None

	def notify_employee(self):
		employee = frappe.get_doc("Employee", self.employee)
		if not employee.user_id:
			return

		parent_doc = frappe.get_doc("Leave Application", self.name)
		args = parent_doc.as_dict()

		template = frappe.db.get_single_value("HR Settings", "leave_status_notification_template")
		if not template:
			frappe.msgprint(_("Please set default template for Leave Status Notification in HR Settings."))
			return
		email_template = frappe.get_doc("Email Template", template)
		message = frappe.render_template(email_template.response, args)

		self.notify(
			{
				# for post in messages
				"message": message,
				"message_to": employee.user_id,
				# for email
				"subject": email_template.subject,
				"notify": "employee",
			}
		)

	def notify_leave_approver(self):
		if self.leave_approver:
			parent_doc = frappe.get_doc("Leave Application", self.name)
			args = parent_doc.as_dict()

			template = frappe.db.get_single_value("HR Settings", "leave_approval_notification_template")
			if not template:
				frappe.msgprint(
					_("Please set default template for Leave Approval Notification in HR Settings.")
				)
				return
			email_template = frappe.get_doc("Email Template", template)
			message = frappe.render_template(email_template.response, args)

			self.notify(
				{
					# for post in messages
					"message": message,
					"message_to": self.leave_approver,
					# for email
					"subject": email_template.subject,
				}
			)

	def notify(self, args):
		args = frappe._dict(args)
		# args -> message, message_to, subject
		if cint(self.follow_via_email):
			contact = args.message_to
			if not isinstance(contact, list):
				if not args.notify == "employee":
					contact = frappe.get_doc("User", contact).email or contact

			sender = dict()
			sender["email"] = frappe.get_doc("User", frappe.session.user).email
			sender["full_name"] = get_fullname(sender["email"])

			try:
				frappe.sendmail(
					recipients=contact,
					sender=sender["email"],
					subject=args.subject,
					message=args.message,
				)
				frappe.msgprint(_("Email sent to {0}").format(contact))
			except frappe.OutgoingEmailError:
				pass

	def create_leave_ledger_entry(self, submit=True):
		if self.status != "Approved" and submit:
			return

		expiry_date = get_allocation_expiry_for_cf_leaves(
			self.employee, self.leave_type, self.to_date, self.from_date
		)
		lwp = frappe.db.get_value("Leave Type", self.leave_type, "is_lwp")

		if expiry_date:
			self.create_ledger_entry_for_intermediate_allocation_expiry(expiry_date, submit, lwp)
		else:
			alloc_on_from_date, alloc_on_to_date = self.get_allocation_based_on_application_dates()
			if self.is_separate_ledger_entry_required(alloc_on_from_date, alloc_on_to_date):
				# required only if negative balance is allowed for leave type
				# else will be stopped in validation itself
				self.create_separate_ledger_entries(alloc_on_from_date, alloc_on_to_date, submit, lwp)
			else:
				raise_exception = False if frappe.flags.in_patch else True
				args = dict(
					leaves=self.total_leave_days * -1,
					from_date=self.from_date,
					to_date=self.to_date,
					is_lwp=lwp,
					holiday_list=get_holiday_list_for_employee(self.employee, raise_exception=raise_exception)
					or "",
				)
				create_leave_ledger_entry(self, args, submit)

	def is_separate_ledger_entry_required(
		self, alloc_on_from_date: Optional[Dict] = None, alloc_on_to_date: Optional[Dict] = None
	) -> bool:
		"""Checks if application dates fall in separate allocations"""
		if (
			(alloc_on_from_date and not alloc_on_to_date)
			or (not alloc_on_from_date and alloc_on_to_date)
			or (
				alloc_on_from_date and alloc_on_to_date and alloc_on_from_date.name != alloc_on_to_date.name
			)
		):
			return True
		return False

	def create_separate_ledger_entries(self, alloc_on_from_date, alloc_on_to_date, submit, lwp):
		"""Creates separate ledger entries for application period falling into separate allocations"""
		# for creating separate ledger entries existing allocation periods should be consecutive
		if (
			submit
			and alloc_on_from_date
			and alloc_on_to_date
			and add_days(alloc_on_from_date.to_date, 1) != alloc_on_to_date.from_date
		):
			frappe.throw(
				_(
					"Leave Application period cannot be across two non-consecutive leave allocations {0} and {1}."
				).format(
					get_link_to_form("Leave Allocation", alloc_on_from_date.name),
					get_link_to_form("Leave Allocation", alloc_on_to_date),
				)
			)

		raise_exception = False if frappe.flags.in_patch else True

		if alloc_on_from_date:
			first_alloc_end = alloc_on_from_date.to_date
			second_alloc_start = add_days(alloc_on_from_date.to_date, 1)
		else:
			first_alloc_end = add_days(alloc_on_to_date.from_date, -1)
			second_alloc_start = alloc_on_to_date.from_date

		leaves_in_first_alloc = get_number_of_leave_days(
			self.employee,
			self.leave_type,
			self.from_date,
			first_alloc_end,
			self.half_day,
			self.half_day_date,
		)
		leaves_in_second_alloc = get_number_of_leave_days(
			self.employee,
			self.leave_type,
			second_alloc_start,
			self.to_date,
			self.half_day,
			self.half_day_date,
		)

		args = dict(
			is_lwp=lwp,
			holiday_list=get_holiday_list_for_employee(self.employee, raise_exception=raise_exception)
			or "",
		)

		if leaves_in_first_alloc:
			args.update(
				dict(from_date=self.from_date, to_date=first_alloc_end, leaves=leaves_in_first_alloc * -1)
			)
			create_leave_ledger_entry(self, args, submit)

		if leaves_in_second_alloc:
			args.update(
				dict(from_date=second_alloc_start, to_date=self.to_date, leaves=leaves_in_second_alloc * -1)
			)
			create_leave_ledger_entry(self, args, submit)

	def create_ledger_entry_for_intermediate_allocation_expiry(self, expiry_date, submit, lwp):
		"""Splits leave application into two ledger entries to consider expiry of allocation"""
		raise_exception = False if frappe.flags.in_patch else True

		leaves = get_number_of_leave_days(
			self.employee, self.leave_type, self.from_date, expiry_date, self.half_day, self.half_day_date
		)

		if leaves:
			args = dict(
				from_date=self.from_date,
				to_date=expiry_date,
				leaves=leaves * -1,
				is_lwp=lwp,
				holiday_list=get_holiday_list_for_employee(self.employee, raise_exception=raise_exception)
				or "",
			)
			create_leave_ledger_entry(self, args, submit)

		if getdate(expiry_date) != getdate(self.to_date):
			start_date = add_days(expiry_date, 1)
			leaves = get_number_of_leave_days(
				self.employee, self.leave_type, start_date, self.to_date, self.half_day, self.half_day_date
			)

			if leaves:
				args.update(dict(from_date=start_date, to_date=self.to_date, leaves=leaves * -1))
				create_leave_ledger_entry(self, args, submit)

	# def create_leave_application():
	# 	print("\n\n\n")
	# 	print("Hello")

	# 	session_user_employee_code = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")

	# 	if session_user_employee_code == employee:
	# 		pass
	# 	else:
	# 		raise frappe.ValidationError("You are not allowed to create leave applications for other employees.")

def get_allocation_expiry_for_cf_leaves(
	employee: str, leave_type: str, to_date: datetime.date, from_date: datetime.date
) -> str:
	"""Returns expiry of carry forward allocation in leave ledger entry"""
	expiry = frappe.get_all(
		"Leave Ledger Entry",
		filters={
			"employee": employee,
			"leave_type": leave_type,
			"is_carry_forward": 1,
			"transaction_type": "Leave Allocation",
			"to_date": ["between", (from_date, to_date)],
			"docstatus": 1,
		},
		fields=["to_date"],
	)
	return expiry[0]["to_date"] if expiry else ""
	
def is_lwp(leave_type):
	lwp = frappe.db.sql("select is_lwp from `tabLeave Type` where name = %s", leave_type)
	return lwp and cint(lwp[0][0]) or 0
