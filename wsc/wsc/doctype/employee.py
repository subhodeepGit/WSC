# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe

from frappe import _, enqueue, scrub, throw
from frappe.model.naming import set_name_by_naming_series
from frappe.permissions import (
    add_user_permission,
    get_doc_permissions,
    has_permission,
    remove_user_permission,
    set_user_permission_if_allowed,
)
from frappe.utils import add_years, cstr, getdate, today, validate_email_address
from frappe.utils.nestedset import NestedSet

from erpnext.utilities.transaction_base import delete_events
import re
# from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions


class EmployeeUserDisabledError(frappe.ValidationError):
    pass
class InactiveEmployeeStatusError(frappe.ValidationError):
    pass

class Employee(NestedSet):
    nsm_parent_field = 'reports_to'

    def autoname(self):
        naming_method = frappe.db.get_value("HR Settings", None, "emp_created_by")
        if not naming_method:
            throw(_("Please setup Employee Naming System in Human Resource > HR Settings"))
        else:
            if naming_method == 'Naming Series':
                set_name_by_naming_series(self)
            elif naming_method == 'Employee Number':
                self.name = self.employee_number
            elif naming_method == 'Full Name':
                self.set_employee_name()
                self.name = self.employee_name

        self.employee = self.name

    def validate(self):
        
        from erpnext.controllers.status_updater import validate_status
        validate_status(self.status, ["Active", "Inactive", "Suspended", "Left"])
        self.employee = self.name
        self.set_employee_name()
        self.validate_date()
        self.validate_email()
        self.validate_status()
        self.validate_reports_to()
        self.validate_preferred_email()
        self.create_profile()
        # self.create_user_permission_for_employee()
        if self.job_applicant:
            self.validate_onboarding_process()

        if self.user_id:
            self.validate_user_details()
        else:
            existing_user_id = frappe.db.get_value("Employee", self.name, "user_id")
            if existing_user_id:
                remove_user_permission(
                    "Employee", self.name, existing_user_id)
        self.validate_joining_date()
        self.validate_offer_date()
        self.validate_passport_date()
        self.validate_notice_days()
        self.validate_mobile_number() 
        if not self.present_contract_start_date :
            self.present_contract_start_date = self.date_of_joining
        # if not self.is_new():
        #     dynamic_workflow_goal_setting(self)    

        

    def create_profile(self):
        check_profile = frappe.get_all("My Profile", {'name':self.name},['name'])
        if len(check_profile) == 0:
            my_profile = frappe.new_doc("My Profile")
            my_profile.employee = self.name
            my_profile.employee_name=self.employee_name
            my_profile.department = self.department
            my_profile.designation=self.designation
            my_profile.branch = self.branch
            my_profile.employment_type = self.employment_type
            my_profile.employee_number = self.employee_number
            my_profile.user_id = self.user_id
            my_profile.gender = self.gender
            my_profile.date_of_birth=self.date_of_birth
            my_profile.blood_group=self.blood_group
            my_profile.mobile = self.cell_number
            my_profile.emergency_contact_name = self.person_to_be_contacted
            my_profile.emergency_contact = self.emergency_phone_number
            my_profile.personal_email = self.personal_email
            my_profile.company_email = self.company_email
            my_profile.current_address=self.current_address
            my_profile.permananet_address=self.permanent_address
            my_profile.save()
        elif len(check_profile) > 0:
            old_profile= frappe.get_doc("My Profile", self.name)
            old_profile.employee_name=self.employee_name
            old_profile.department = self.department
            old_profile.designation=self.designation
            old_profile.branch = self.branch
            old_profile.employment_type = self.employment_type
            old_profile.employee_number = self.employee_number
            old_profile.user_id = self.user_id
            old_profile.gender = self.gender
            old_profile.date_of_birth=self.date_of_birth
            old_profile.blood_group=self.blood_group
            old_profile.mobile = self.cell_number
            old_profile.emergency_contact_name = self.person_to_be_contacted
            old_profile.emergency_contact = self.emergency_phone_number
            old_profile.personal_email = self.personal_email
            old_profile.company_email = self.company_email
            old_profile.current_address=self.current_address
            old_profile.permananet_address=self.permanent_address
            old_profile.save()
            
    def validate_notice_days(self):
        if self.notice_number_of_days:
            if self.notice_number_of_days<0 :
                frappe.throw("Notice Days should not be -ve")
    def validate_mobile_number(self):
        if self.cell_number:
            pattern = r"^\d{10}$"

            if not re.match(pattern, self.cell_number):
                frappe.throw("Invalid mobile number format")
    
    

    def on_change(self):
        self.permissions()
    def after_insert(self):
        self.permissions()
        
    def permissions(doc):
        for result in frappe.get_all("User",{"name":doc.user_id},['name']):
            for get_role in frappe.get_all("Has Role",{"parent":result.name},['role']):
                print("\n\n\n\nROLE USER",get_role.role) 
            print("\n\nFirst",doc.user_id)
            if doc.user_id ==result.name and get_role.role not in ["HR Admin","Director"]:
               
                print("\n\nSecond",result.name)
                print("\n\nThrird",get_role.role)

            # user_role and "Director" not in user_role:
                add_user_permission(doc.doctype,doc.name,doc.user_id,doc)
            else:
                frappe.msgprint("Welcome")
            
            if doc.leave_approver:
                add_user_permission(doc.doctype,doc.name,doc.leave_approver,doc)
            if doc.reporting_authority_email:
                add_user_permission(doc.doctype,doc.name,doc.reporting_authority_email,doc)

    def after_rename(self, old, new, merge):
        self.db_set("employee", new)

    def set_employee_name(self):
        self.employee_name = ' '.join(filter(lambda x: x, [self.first_name, self.middle_name, self.last_name]))

    def validate_user_details(self):
        data = frappe.db.get_value('User',
            self.user_id, ['enabled', 'user_image'], as_dict=1)
        if data.get("user_image") and self.image == '':
            self.image = data.get("user_image")
        self.validate_for_enabled_user_id(data.get("enabled", 0))
        self.validate_duplicate_user_id()

    def update_nsm_model(self):
        frappe.utils.nestedset.update_nsm(self)

    def on_update(self):
        self.update_nsm_model()
        if self.user_id:
            self.update_user()
            self.update_user_permissions()
        self.reset_employee_emails_cache()
        self.update_approver_role()

    def update_user_permissions(self):
        if not self.create_user_permission: return
        if not has_permission('User Permission', ptype='write', raise_exception=False): return

        employee_user_permission_exists = frappe.db.exists('User Permission', {
            'allow': 'Employee',
            'for_value': self.name,
            'user': self.user_id
        })

        if employee_user_permission_exists:
            set_permissions(self)
            return

        set_user_permission_if_allowed("Company", self.company, self.user_id)

    def update_user(self):
        # add employee role if missing
        user = frappe.get_doc("User", self.user_id)
        user.flags.ignore_permissions = True

        if "Employee" not in user.get("roles"):
            user.append_roles("Employee")

        # copy details like Fullname, DOB and Image to User
        if self.employee_name and not (user.first_name and user.last_name):
            employee_name = self.employee_name.split(" ")
            if len(employee_name) >= 3:
                user.last_name = " ".join(employee_name[2:])
                user.middle_name = employee_name[1]
            elif len(employee_name) == 2:
                user.last_name = employee_name[1]

            user.first_name = employee_name[0]

        if self.date_of_birth:
            user.birth_date = self.date_of_birth

        if self.gender:
            user.gender = self.gender

        if self.image:
            if not user.user_image:
                user.user_image = self.image
                try:
                    frappe.get_doc({
                        "doctype": "File",
                        "file_url": self.image,
                        "attached_to_doctype": "User",
                        "attached_to_name": self.user_id
                    }).insert()
                except frappe.DuplicateEntryError:
                    # already exists
                    pass

        user.save()

    def update_approver_role(self):
        if self.leave_approver:
            user = frappe.get_doc("User", self.leave_approver)
            user.flags.ignore_permissions = True
            user.add_roles("Leave Approver")

        if self.expense_approver:
            user = frappe.get_doc("User", self.expense_approver)
            user.flags.ignore_permissions = True
            user.add_roles("Expense Approver")

    def validate_date(self):
        if self.date_of_birth and getdate(self.date_of_birth) > getdate(today()):
            throw(_("Date of Birth cannot be greater than today."))

        if self.date_of_birth and self.date_of_joining and getdate(self.date_of_birth) >= getdate(self.date_of_joining):
            throw(_("Date of Joining must be greater than Date of Birth"))

        elif self.date_of_retirement and self.date_of_joining and (getdate(self.date_of_retirement) <= getdate(self.date_of_joining)):
            throw(_("Date Of Retirement must be greater than Date of Joining"))

        elif self.relieving_date and self.date_of_joining and (getdate(self.relieving_date) < getdate(self.date_of_joining)):
            throw(_("Relieving Date must be greater than or equal to Date of Joining"))

        elif self.contract_end_date and self.date_of_joining and (getdate(self.contract_end_date) <= getdate(self.date_of_joining)):
            throw(_("Contract End Date must be greater than Date of Joining"))

    def validate_email(self):
        if self.company_email:
            validate_email_address(self.company_email, True)
        if self.personal_email:
            validate_email_address(self.personal_email, True)

    def set_preferred_email(self):
        preferred_email_field = frappe.scrub(self.prefered_contact_email)
        if preferred_email_field:
            preferred_email = self.get(preferred_email_field)
            self.prefered_email = preferred_email

    def validate_status(self):
        if self.status == 'Left':
            reports_to = frappe.db.get_all('Employee',
                filters={'reports_to': self.name, 'status': "Active"},
                fields=['name','employee_name']
            )
            if reports_to:
                link_to_employees = [frappe.utils.get_link_to_form('Employee', employee.name, label=employee.employee_name) for employee in reports_to]
                message = _("The following employees are currently still reporting to {0}:").format(frappe.bold(self.employee_name))
                message += "<br><br><ul><li>" + "</li><li>".join(link_to_employees)
                message += "</li></ul><br>"
                message += _("Please make sure the employees above report to another Active employee.")
                throw(message, InactiveEmployeeStatusError, _("Cannot Relieve Employee"))
            if not self.relieving_date:
                throw(_("Please enter relieving date."))

    def validate_for_enabled_user_id(self, enabled):
        if not self.status == 'Active':
            return

        if enabled is None:
            frappe.throw(_("User {0} does not exist").format(self.user_id))
        if enabled == 0:
            frappe.throw(_("User {0} is disabled").format(self.user_id), EmployeeUserDisabledError)

    def validate_duplicate_user_id(self):
        employee = frappe.db.sql_list("""select name from `tabEmployee` where
            user_id=%s and status='Active' and name!=%s""", (self.user_id, self.name))
        if employee:
            throw(_("User {0} is already assigned to Employee {1}").format(
                self.user_id, employee[0]), frappe.DuplicateEntryError)

    def validate_reports_to(self):
        if self.reports_to == self.name:
            throw(_("Employee cannot report to himself."))

    def on_trash(self):
        self.update_nsm_model()
        delete_events(self.doctype, self.name)
        if frappe.db.exists("Employee Transfer", {'new_employee_id': self.name, 'docstatus': 1}):
            emp_transfer = frappe.get_doc("Employee Transfer", {'new_employee_id': self.name, 'docstatus': 1})
            emp_transfer.db_set("new_employee_id", '')

    def validate_preferred_email(self):
        if self.prefered_contact_email and not self.get(scrub(self.prefered_contact_email)):
            frappe.msgprint(_("Please enter {0}").format(self.prefered_contact_email))

    def validate_onboarding_process(self):
        employee_onboarding = frappe.get_all("Employee Onboarding",
            filters={"job_applicant": self.job_applicant, "docstatus": 1, "boarding_status": ("!=", "Completed")})
        if employee_onboarding:
            doc = frappe.get_doc("Employee Onboarding", employee_onboarding[0].name)
            doc.validate_employee_creation()
            doc.db_set("employee", self.name)

    def reset_employee_emails_cache(self):
        prev_doc = self.get_doc_before_save() or {}
        cell_number = cstr(self.get('cell_number'))
        prev_number = cstr(prev_doc.get('cell_number'))
        if (cell_number != prev_number or
            self.get('user_id') != prev_doc.get('user_id')):
            frappe.cache().hdel('employees_with_number', cell_number)
            frappe.cache().hdel('employees_with_number', prev_number)
    
    def validate_joining_date(self):
        if self.date_of_joining and self.final_confirmation_date:
            if self.final_confirmation_date>self.date_of_joining:
                frappe.throw("Confirmation Date Should not be after the date of Joining")
            else :
                pass
        else :
            pass
    def validate_offer_date(self):
        if self.scheduled_confirmation_date and self.date_of_joining:
            if self.scheduled_confirmation_date > self.date_of_joining:
                frappe.throw("Offer date should not be after the Date of Joining")
            else :
                pass
        if self.scheduled_confirmation_date and self.final_confirmation_date :
            if self.scheduled_confirmation_date < self.final_confirmation_date :
                frappe.throw("Confirmation date should not be after the Offer Date")
            
            else :
                pass
    def validate_passport_date(self):
        if self.valid_upto and self.date_of_issue:
            if self.valid_upto<self.date_of_issue :
                frappe.throw("Passport Valid date should not be Before the Date of Issue")
            else :
                pass
    
def get_timeline_data(doctype, name):
    '''Return timeline for attendance'''
    return dict(frappe.db.sql('''select unix_timestamp(attendance_date), count(*)
        from `tabAttendance` where employee=%s
            and attendance_date > date_sub(curdate(), interval 1 year)
            and status in ('Present', 'Half Day')
            group by attendance_date''', name))

@frappe.whitelist()
def get_retirement_date(date_of_birth=None):
    ret = {}
    if date_of_birth:
        try:
            retirement_age = int(frappe.db.get_single_value("HR Settings", "retirement_age") or 60)
            dt = add_years(getdate(date_of_birth),retirement_age)
            ret = {'date_of_retirement': dt.strftime('%Y-%m-%d')}
        except ValueError:
            # invalid date
            ret = {}

    return ret

def validate_employee_role(doc, method):
    # called via User hook
    if "Employee" in [d.role for d in doc.get("roles")]:
        if not frappe.db.get_value("Employee", {"user_id": doc.name}):
            frappe.msgprint(_("Please set User ID field in an Employee record to set Employee Role"))
            doc.get("roles").remove(doc.get("roles", {"role": "Employee"})[0])

def update_user_permissions(doc, method):
    # called via User hook
    if "Employee" in [d.role for d in doc.get("roles")]:
        if not has_permission('User Permission', ptype='write', raise_exception=False): return
        employee = frappe.get_doc("Employee", {"user_id": doc.name})
        employee.update_user_permissions()

def get_employee_email(employee_doc):
    return employee_doc.get("user_id") or employee_doc.get("personal_email") or employee_doc.get("company_email")

def get_holiday_list_for_employee(employee, raise_exception=True):
    if employee:
        holiday_list, company = frappe.db.get_value("Employee", employee, ["holiday_list", "company"])
    else:
        holiday_list=''
        company=frappe.db.get_value("Global Defaults", None, "default_company")

    if not holiday_list:
        holiday_list = frappe.get_cached_value('Company',  company,  "default_holiday_list")

    if not holiday_list and raise_exception:
        frappe.throw(_('Please set a default Holiday List for Employee {0} or Company {1}').format(employee, company))

    return holiday_list

def is_holiday(employee, date=None, raise_exception=True, only_non_weekly=False, with_description=False):
    '''
    Returns True if given Employee has an holiday on the given date
        :param employee: Employee `name`
        :param date: Date to check. Will check for today if None
        :param raise_exception: Raise an exception if no holiday list found, default is True
        :param only_non_weekly: Check only non-weekly holidays, default is False
    '''

    holiday_list = get_holiday_list_for_employee(employee, raise_exception)
    if not date:
        date = today()

    if not holiday_list:
        return False

    filters = {
        'parent': holiday_list,
        'holiday_date': date
    }
    if only_non_weekly:
        filters['weekly_off'] = False

    holidays = frappe.get_all(
        'Holiday',
        fields=['description'],
        filters=filters,
        pluck='description'
    )

    if with_description:
        return len(holidays) > 0, holidays

    return len(holidays) > 0

@frappe.whitelist()
def deactivate_sales_person(status = None, employee = None):
    if status == "Left":
        sales_person = frappe.db.get_value("Sales Person", {"Employee": employee})
        if sales_person:
            frappe.db.set_value("Sales Person", sales_person, "enabled", 0)

@frappe.whitelist()
def create_user(employee, user = None, email=None):
    emp = frappe.get_doc("Employee", employee)

    employee_name = emp.employee_name.split(" ")
    middle_name = last_name = ""

    if len(employee_name) >= 3:
        last_name = " ".join(employee_name[2:])
        middle_name = employee_name[1]
    elif len(employee_name) == 2:
        last_name = employee_name[1]

    first_name = employee_name[0]

    if email:
        emp.prefered_email = email

    user = frappe.new_doc("User")
    user.update({
        "name": emp.employee_name,
        "email": emp.prefered_email,
        "enabled": 1,
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "gender": emp.gender,
        "birth_date": emp.date_of_birth,
        "phone": emp.cell_number,
        "bio": emp.bio
    })
    user.insert()
    return user.name

def get_all_employee_emails(company):
    '''Returns list of employee emails either based on user_id or company_email'''
    employee_list = frappe.get_all('Employee',
        fields=['name','employee_name'],
        filters={
            'status': 'Active',
            'company': company
        }
    )
    employee_emails = []
    for employee in employee_list:
        if not employee:
            continue
        user, company_email, personal_email = frappe.db.get_value('Employee',
            employee, ['user_id', 'company_email', 'personal_email'])
        email = user or company_email or personal_email
        if email:
            employee_emails.append(email)
    return employee_emails

def get_employee_emails(employee_list):
    '''Returns list of employee emails either based on user_id or company_email'''
    employee_emails = []
    for employee in employee_list:
        if not employee:
            continue
        user, company_email, personal_email = frappe.db.get_value('Employee', employee,
                                            ['user_id', 'company_email', 'personal_email'])
        email = user or company_email or personal_email
        if email:
            employee_emails.append(email)
    return employee_emails

@frappe.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False, is_tree=False):

    filters = [['status', '=', 'Active']]
    if company and company != 'All Companies':
        filters.append(['company', '=', company])

    fields = ['name as value', 'employee_name as title']

    if is_root:
        parent = ''
    if parent and company and parent!=company:
        filters.append(['reports_to', '=', parent])
    else:
        filters.append(['reports_to', '=', ''])

    employees = frappe.get_list(doctype, fields=fields,
        filters=filters, order_by='name')

    for employee in employees:
        is_expandable = frappe.get_all(doctype, filters=[
            ['reports_to', '=', employee.get('value')]
        ])
        employee.expandable = 1 if is_expandable else 0

    return employees

def on_doctype_update():
    frappe.db.add_index("Employee", ["lft", "rgt"])

def has_user_permission_for_employee(user_name, employee_name):
    return frappe.db.exists({
        'doctype': 'User Permission',
        'user': user_name,
        'allow': 'Employee',
        'for_value': employee_name
    })

def has_upload_permission(doc, ptype='read', user=None):
    if not user:
        user = frappe.session.user
    if get_doc_permissions(doc, user=user, ptype=ptype).get(ptype):
        return True
    return doc.user_id == user
import frappe

def validate(doc,method):
    set_permissions(doc)

def set_permissions(doc):
    if not check_duplicate_permission(doc):
        user_permission=frappe.new_doc("User Permission")
        user_permission.applicable_for="Mentor Allocation"
        user_permission.user=doc.user_id
        user_permission.allow="Employee"
        user_permission.for_value=doc.name
        user_permission.apply_to_all_doctypes=0
        user_permission.reference_doctype=doc.doctype
        user_permission.reference_docname=doc.name
        user_permission.save()

def check_duplicate_permission(doc):
    return  frappe.db.get_all("User Permission", filters={
            'allow': "Employee",
            'for_value': doc.name,
            'user': doc.user_id,
            'applicable_for': "Mentor Allocation",
            'name': ['!=', doc.name]
        }, limit=1)

def dynamic_workflow_goal_setting(self):
    doc_before_save = self.get_doc_before_save()
    for t in doc_before_save.get("goal_settings_workflow"):
        pass
    for t in self.get("goal_settings_workflow"):
        data=frappe.get_all("Employee",{"name":t.employee},["user_id"])
        if data:
            user = frappe.get_doc("User",data[0]["user_id"])
            user.add_roles(t.level_of_approval)
