import frappe
import datetime
import calendar

@frappe.whitelist()
def get_data():
    print("\n\n\n")
    
    user_data = frappe.get_all("User",{'email':frappe.session.user} , ['email' , 'role_profile_name' ])

    if user_data[0]['role_profile_name'] == 'Director' or user_data[0]['role_profile_name'] == 'Administrater':
        
        last_six_months = []

        # Get the current date
        current_date = datetime.datetime.now()

        status = ['Present' , 'Absent' , 'On Leave' , 'Half Day' , 'Work From Home']

        filters_present = {
            "status": status[0],
            "docstatus": 1,
            "attendance_date": [">=", frappe.utils.add_months(frappe.utils.nowdate(), -6)],
            "attendance_date": ["<=", frappe.utils.nowdate()]
        }

        filters_absent = {
            "status": status[1],
            "docstatus": 1,
            "attendance_date": [">=", frappe.utils.add_months(frappe.utils.nowdate(), -6)],
            "attendance_date": ["<=", frappe.utils.nowdate()]
        }

        filters_on_leave = {
            "status": status[2],
            "docstatus": 1,
            "attendance_date": [">=", frappe.utils.add_months(frappe.utils.nowdate(), -6)],
            "attendance_date": ["<=", frappe.utils.nowdate()]
        }

        filters_half_day = {
            "status": status[3],
            "docstatus": 1,
            "attendance_date": [">=", frappe.utils.add_months(frappe.utils.nowdate(), -6)],
            "attendance_date": ["<=", frappe.utils.nowdate()]
        }

        filters_wfh = {
            "status": status[4],
            "docstatus": 1,
            "attendance_date": [">=", frappe.utils.add_months(frappe.utils.nowdate(), -6)],
            "attendance_date": ["<=", frappe.utils.nowdate()]
        }
        
        present_fields = ["status","attendance_date", "MONTH(attendance_date) as month", "YEAR(attendance_date) as year", "COUNT(status) as present"]

        absent_fields = ["status", "attendance_date", "MONTH(attendance_date) as month", "YEAR(attendance_date) as year", "COUNT(status) as absent"]

        on_leave_fields = ["status", "attendance_date","MONTH(attendance_date) as month", "YEAR(attendance_date) as year", "COUNT(status) as on_leave"]

        half_day_fields = ["status","attendance_date", "MONTH(attendance_date) as month", "YEAR(attendance_date) as year", "COUNT(status) as half_day"]

        wfh_fields = ["status", "attendance_date","MONTH(attendance_date) as month", "YEAR(attendance_date) as year",  "COUNT(status) as work_from_home"]
        
        attendance_present = frappe.get_list("Attendance", filters_present , present_fields , group_by="MONTH(attendance_date), YEAR(attendance_date)")

        attendance_absent = frappe.get_list("Attendance", filters_absent , absent_fields , group_by="MONTH(attendance_date), YEAR(attendance_date)")

        attendance_on_leave = frappe.get_list("Attendance", filters_on_leave , on_leave_fields , group_by="MONTH(attendance_date), YEAR(attendance_date)")

        attendance_half_day = frappe.get_list("Attendance", filters_half_day , half_day_fields , group_by="MONTH(attendance_date), YEAR(attendance_date)")

        attendance_wfh = frappe.get_list("Attendance", filters_wfh , wfh_fields , group_by="MONTH(attendance_date), YEAR(attendance_date)")

        leave_records = frappe.get_list('Leave Application' , {'current_status':'Approved'} , ['name' , 'employee_name' , 'leave_type' , 'from_date' , 'to_date'] , limit_start=0 , limit_page_length=10)

        job_applicant_records = frappe.get_list("Job Applicant" , {
            'current_status': ['in', ['Applied', 'Qualified']] 
            }, 
            ['name' , 'applicant_name', 'email_id', 'designation', 'current_status', 'application_year']
        )

        employee_count = frappe.get_list("Employee" , {'status':'Active'} , 
                                    ["COUNT(name) as employee_count" , 'status']     
                                )

        inactive_emp_count = frappe.get_list("Employee" , {'status':'Inactive'} , ["COUNT(name) as count" , 'status'])

        suspended_emp_count = frappe.get_list("Employee" , {'status':'Suspended'} , ["COUNT(name) as count" ,'status'])

        left_emp_count = frappe.get_list("Employee" , {'status':'Left'} , ["COUNT(name) as count" , 'status'])

        total_emp_count = frappe.get_list("Employee" , {'status': ['!=', 'Active']} , ["COUNT(name) as total_count"])

        holiday_list = frappe.db.sql("""
            SELECT 
                list.name ,
                holiday.holiday_date ,
                holiday.weekly_off ,
                holiday.description 
            FROM 
                `tabHoliday List` list
            INNER JOIN
                `tabHoliday`holiday
            ON holiday.parent = list.name
            WHERE 
                holiday.holiday_date >= CURRENT_DATE()
            ORDER BY holiday.holiday_date 
            LIMIT 10    
        """,as_dict=1)
    
        print(attendance_on_leave)
        print(filters_on_leave)

        return [attendance_present , attendance_absent , attendance_on_leave , attendance_half_day , attendance_wfh , leave_records , job_applicant_records , employee_count , inactive_emp_count , suspended_emp_count , left_emp_count , total_emp_count , holiday_list]
    
    else: 
        frappe.throw("Page Only Visible to Director")
            
    # return attendance_data[0]
def days_in_month(year, month):
    return calendar.monthrange(year, month)[1]

def is_within_last_six_months(date_to_check):
    # Get the current date
    current_date = datetime.date.today()
    
    # Calculate the date six months ago
    six_months_ago = current_date - datetime.timedelta(days=6*30)  # Approximating 30 days per month
    
    # Check if the date falls within the last six months
    return six_months_ago <= date_to_check <= current_date

# Example usage

        