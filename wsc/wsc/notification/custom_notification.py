from re import L
import frappe
from frappe.utils.data import format_date
from frappe.utils import get_url_to_form
from frappe.utils import cint, cstr, parse_addr


def student_applicant_submit(doc):
    sub="""<p><b>Application Form is Sucessfully Submitted</b></p><br>"""
    msg="""<b>---------------------Applicant Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}{1}<br>""".format(doc.get('first_name'), doc.get('last_name'))
    msg+="""<b>Application Number:</b>  {0}<br>""".format(doc.get('name'))
    msg+="""<b>Department:</b>  {0}<br>""".format(doc.get('department'))
    msg+="""<b>Program Grade:</b>  {0}<br>""".format(doc.get('program_grade'))
    msg+="""<p>Priority Programs: </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Programs</th>"""
    for d in doc.get("program_priority"):
        msg += """<tr><td>{0}</td></tr>""".format(str(d.get('programs'))) 
    msg += "</table>"
    send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg)


def employee_reporting_aproverr(doc):
    sub="""Leave Approval Notification"""
    
    msg="""<b>---------------------Leave Application Details---------------------</b><br>"""
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc['employee_name'])
    msg+="""<b>Leave Type:</b>  {0}<br>""".format(doc['leave_type'])
    msg+="""<b>From Date:</b>  {0}<br>""".format(doc['from_date'])
    msg+="""<b>To Date:</b>  {0}<br>""".format(doc['to_date'])
    
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    leave_app_url = get_url_to_form('Leave Application', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(leave_app_url)

    send_mail([doc['reporting_authority_email']],sub,msg)
    frappe.msgprint("Email sent to reporting authority",[doc['reporting_authority_email']])

def employee_shift_reporting_aprover(doc):
    sub="""Shift Request Approval Notification"""
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Employee Separation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
    msg="""<b>---------------------Shift Request Details---------------------</b><br>"""
    msg+="""<b>Employee ID:</b>  {0}<br>""".format(doc.get('employee'))
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc.get('employee_name'))
    msg+="""<b>Shift Type:</b>  {0}<br>""".format(doc.get('shift_type'))
    msg+="""<b>From Date:</b>  {0}<br>""".format(doc.get('from_date'))
    msg+="""<b>To Date:</b>  {0}<br>""".format(doc.get('to_date'))
    shift_app_url = get_url_to_form('Shift Request', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(shift_app_url)
    send_mail(frappe.db.get_value("Shift Request",doc.get('name'),"reporting_authority"),sub,msg)
    frappe.msgprint("Email sent to Shift Reporting Authority")  

def employee_shift_approver(doc):
    sub="Shift Request Approval Notification"
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Shift Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""
    msg="""<b>---------------------Shift Request Details---------------------</b><br>"""
    msg+="""<b>Employee ID:</b>  {0}<br>""".format(doc.get('employee'))
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc.get('employee_name'))
    msg+="""<b>Shift Type:</b>  {0}<br>""".format(doc.get('shift_type'))
    msg+="""<b>From Date:</b>  {0}<br>""".format(doc.get('from_date'))
    msg+="""<b>To Date:</b>  {0}<br>""".format(doc.get('to_date'))
    shift_app_url = get_url_to_form('Shift Request', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(shift_app_url)
    send_mail(frappe.db.get_value("Shift Request",doc.get('name'),"approver"),sub,msg)
    frappe.msgprint("Email sent to Shift Request Approving Authority")

def employee_grievance_member(doc):
    sub = "Reg:Employee Grievance Details</b></p><br>"

    msg = "<b>---------------------Employee Grievance Details---------------------</b><br>"

    msg += "<b>Employee Grievance ID:</b> {0}<br>".format(doc.get('name'))
    msg += "<b>Raised By:</b> {0}<br>".format(doc.get('raise_by'))
    msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
    msg += "<b>Date:</b> {0}<br>".format(doc.get('date'))

    grievance_app_url = get_url_to_form('Employee Grievance', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(grievance_app_url)

    recipients = frappe.get_all("User", filters={'role': 'Grievance Cell Member'}, fields=['email'])
    recipient_emails = [recipient.get('email') for recipient in recipients]

    send_mail(recipient_emails, sub, msg)
    frappe.msgprint("Email sent to Grievance Cell Members")

def employee_grievance_employee_mail(doc):
    sub = "Reg:Employee Grievance Status"

    msg = "<b>---------------------Employee Grievance Status Details---------------------</b><br>"

    msg += "<b>Employee Grievance ID:</b> {0}<br>".format(doc.get('name'))
    msg += "<b>Date:</b> {0}<br>".format(doc.get('date'))
    msg += "<b>Status:</b> {0}<br>".format(doc.get('status'))

    grievance_app_url = get_url_to_form('Employee Grievance', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(grievance_app_url)

    send_mail(frappe.db.get_value("Employee Grievance",doc.get('name'),"employee_email"),sub,msg)
    frappe.msgprint("Status details is sent to the Employee")

def employee_separation_reporting_authority_mail(doc):
    sub = "Reg:Employee Separation Details"
    
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Employee Separation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
    msg += "<b>---------------------Employee Grievance Status Details---------------------</b><br>"
    msg += "<b>Employee Separation ID:</b> {0}<br>".format(doc.get('name'))
    msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
    msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
    msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
    msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
    msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

    separation_app_url = get_url_to_form('Employee Separation', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(separation_app_url)

    send_mail(frappe.db.get_value("Employee Separation",doc.get('name'),"reporting_authority"),sub,msg)
    frappe.msgprint("Employee Separation Details is sent to the Reporting Authority")

def employee_separation_department_head_mail(doc):
    sub = "Reg:Employee Separation Details"
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Employee Separation Details below and navigate to the form by clicking on "Open Now".</p></br>"""

    msg += "<b>---------------------Employee Separation Details---------------------</b><br>"

    msg += "<b>Employee Separation ID:</b> {0}<br>".format(doc.get('name'))
    msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
    msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
    msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
    msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
    msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

    separation_app_url = get_url_to_form('Employee Separation', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(separation_app_url)

    send_mail(frappe.db.get_value("Employee Separation",doc.get('name'),"department_head"),sub,msg)
    frappe.msgprint("Employee Separation Details is sent to the Department Head")    

def employee_separation_director_mail(doc):
    sub = "Reg:Employee Separation Details"
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Employee Separation Details below and navigate to the form by clicking on "Open Now".</p></br>"""

    msg += "<b>---------------------Employee Separation Details---------------------</b><br>"

    msg += "<b>Employee Separation ID:</b> {0}<br>".format(doc.get('name'))
    msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
    msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
    msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
    msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
    msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

    separation_app_url = get_url_to_form('Employee Separation', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(separation_app_url)

    recipients = frappe.get_all("User", filters={'role': 'Director'}, fields=['email'])
    recipient_emails = [recipient.get('email') for recipient in recipients]

    send_mail(recipient_emails, sub, msg)
    frappe.msgprint("Employee Separation Details is sent to the Director")

def employee_separation_hr_mail(doc):
    sub = "Reg:Employee Separation Status Detail"
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Employee Separation Details Status below and navigate to the form by clicking on "Open Now".</p></br>"""
    msg += "<b>---------------------Employee Separation Status---------------------</b><br>"

    msg += "<b>Employee Separation ID:</b> {0}<br>".format(doc.get('name'))
    msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
    msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
    msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
    msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
    msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))
    msg += "<b>Status:</b> {0}<br>".format(doc.get('workflow_state'))

    separation_app_url = get_url_to_form('Employee Separation', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(separation_app_url)

    recipients = frappe.get_all("User", filters={'role':'HR Admin'}, fields=['email'])
    recipient_emails = [recipient.get('email') for recipient in recipients]

    send_mail(recipient_emails, sub, msg)
    frappe.msgprint("Employee Separation Details status is sent to the HR")

    ######################################################################################################Attendance Request#############

def send_mail_to_hr_updation(doc):
    sub="""Attendance Request Approval Notification"""
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Attendance Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""
    msg +="""<b>---------------------Attendance Request Details---------------------</b><br>"""
    msg+="""<b>Employee ID:</b>  {0}<br>""".format(doc.get('employee'))
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc.get('employee_name'))
    msg+="""<b>From Date:</b>  {0}<br>""".format(doc['from_date'])
    msg+="""<b>To Date:</b>  {0}<br>""".format(doc['to_date'])
    shift_app_url = get_url_to_form('Attendance Request', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(shift_app_url)

    recipients = frappe.get_all("User", filters={'role':'HR Admin'}, fields=['email'])
    recipient_emails = [recipient.get('email') for recipient in recipients]

    send_mail(recipient_emails,sub,msg)
    frappe.msgprint("Email sent to HR")  

def send_mail_to_reporting(doc):
    sub="""Attendance Request Approval Notification"""
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Attendance Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""
    msg +="""<b>---------------------Attendance Request Details---------------------</b><br>"""
    msg+="""<b>Employee ID:</b>  {0}<br>""".format(doc.get('employee'))
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc.get('employee_name'))
    msg+="""<b>From Date:</b>  {0}<br>""".format(doc['from_date'])
    msg+="""<b>To Date:</b>  {0}<br>""".format(doc['to_date'])
    shift_app_url = get_url_to_form('Attendance Request', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(shift_app_url)
    send_mail(frappe.db.get_value("Attendance Request",doc.get('name'),"reporting_authority_id"),sub,msg)
    frappe.msgprint("Email sent to Reporting Authority") 

def attendance_update_mail(doc):
    sub="""Attendance Request Status Notification"""
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Attendance Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""
    msg +="""<b>---------------------Attendance Request Details---------------------</b><br>"""
    msg+="""<b>Employee ID:</b>  {0}<br>""".format(doc.get('employee'))
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc.get('employee_name'))
    msg+="""<b>From Date:</b>  {0}<br>""".format(doc.get('from_date'))
    msg+="""<b>To Date:</b>  {0}<br>""".format(doc.get('to_date'))
    msg+="""<b>Status:</b> {0}<br>""".format(doc.get('worklow_state'))
    shift_app_url = get_url_to_form('Attendance Request', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(shift_app_url)

    recipients = frappe.get_all("User", filters={'role':'HR Admin'}, fields=['email'])
    recipient_emails = [recipient.get('email') for recipient in recipients]

    send_mail(recipient_emails,sub,msg)
    frappe.msgprint("Status Notification sent to HR and Employee")

def attendance_update_mail_employee(doc):
    sub="""Attendance Request Status Notification"""
    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p>Kindly refer to the Attendance Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""
    msg +="""<b>---------------------Attendance Request Details---------------------</b><br>"""
    msg+="""<b>Employee ID:</b>  {0}<br>""".format(doc.get('employee'))
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc.get('employee_name'))
    msg+="""<b>From Date:</b>  {0}<br>""".format(doc.get('from_date'))
    msg+="""<b>To Date:</b>  {0}<br>""".format(doc.get('to_date'))
    msg+="""<b>Status:</b> {0}<br>""".format(doc.get('worklow_state'))
    shift_app_url = get_url_to_form('Attendance Request', doc.get('name'))
    msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(shift_app_url)

    send_mail(frappe.db.get_value("Attendance Request",doc.get('name'),"employee_email"),sub,msg)
    frappe.msgprint("Status Notification sent to HR and Employee")
###############################################################################################################################################################
def student_applicant_approved(doc):
    sub="""<p><b>Congratulation !! Your Application Form has been Approved</b></p><br>"""
    msg+="""Further Process, we will connect with you soon.</b><br>"""
    msg+="""<b>---------------------Applicant Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}{1}<br>""".format(doc.get('first_name'), doc.get('last_name'))
    msg+="""<b>Application Number:</b>  {0}<br>""".format(doc.get('name'))
    send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg)

def student_applicant_onhold(doc):
    sub="""<p><b>Application Form is in Waiting Status</b></p><br>"""
    msg+="""<b>---------------------Applicant Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}{1}<br>""".format(doc.get('first_name'), doc.get('last_name'))
    msg+="""<b>Application Number:</b>  {0}<br>""".format(doc.get('name'))
    send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg)

def student_applicant_rejected(doc):
    sub="""<p><b>Application Form has been rejected.</b></p><br>"""
    msg+="""<b>---------------------Applicant Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}{1}<br>""".format(doc.get('first_name'), doc.get('last_name'))
    msg+="""<b>Application Number:</b>  {0}<br>""".format(doc.get('name'))
    send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg)
  

def program_enrollment_admitted(doc):
    msg="""<p>You are admitted in the Programs <b>{0}</b></p><br>""".format(doc.get('programs'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Student Batch:</b>  {0}<br>""".format(doc.get('student_batch_name') or '-')
    msg+="""<b>Permanent Registration Number:</b>  {0}<br>""".format(doc.get('permanant_registration_number') or '-' )
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('programs'))
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('program'))
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Academic Term:</b> {0}<br>""".format(doc.get('academic_term') or '-')
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application status',msg)

def program_enrollment_provisional_admission(doc):
    msg="""<p>You are Provisionaly Admitted in the Programs <b>{0}</b></p><br>""".format(doc.get('programs'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Student Batch:</b>  {0}<br>""".format(doc.get('student_batch_name') or '-')
    msg+="""<b>Permanent Registration Number:</b>  {0}<br>""".format(doc.get('permanant_registration_number') or '-' )
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('programs'))
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('program'))
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Academic Term:</b> {0}<br>""".format(doc.get('academic_term') or '-')

    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application status',msg)


def branch_change_declaration_submit(doc):
    msg="""<p>Branch Change for <b>{0}</b> has been declared </p><br>""".format(doc.get('for_program'))
    msg+="""<b>---------------Branch Change Declaration Details---------------</b><br>"""
    msg+="""<b>Branch Change Declaration ID:</b>  {0}<br>""".format(doc.get('name'))
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Application Start Date:</b>  {0}<br>""".format(format_date(doc.get('application_start_date'), 'dd/mm/yyyy'))
    msg+="""<b>Application End Date:</b>  {0}<br><br><br>""".format(format_date(doc.get('application_end_date'), 'dd/mm/yyyy'))
    msg+="""<b>Branch Change Criteria:</b><br>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Programs</th><th>Semester</th><th>Eligibility score</th><th>Available Seats</th>"""

    for d in doc.get("branch_sliding__criteria"):
        msg += "<tr><td>" + """{0}""".format(str(d.get('program'))) + "</td><td>" + str(d.get('semester')) + "</td><td>" + str(d.get('eligibility_score')) + "</td><td>" + str(d.get('available_seats'))  + "</td></tr>"
    
    msg += "</table>"

    for enroll in frappe.get_all("Program Enrollment",{"programs":doc.get('for_program'),"academic_year":doc.get('academic_year')},['student']):
        send_mail(frappe.db.get_value("Student",enroll.get('student'),"student_email_id"),'Branch Change Declaration',msg)

def branch_change_application_applied(doc):
    msg="""<p>Your application <b>{0}</b> for Branch Change is successfully submitted. </p><br>""".format(doc.get('name'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('sliding_in_program') or '-')
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('sliding_in_semester') or '-')
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application Status',msg)



def send_clearance_notification_to_department(doc):
    msg="""<p>Dear Department,please refer to department clearance status table.</p><br>"""
    msg+="""<b>Student Details</b><br>"""
    msg+="""<b>Student Id:</b>  {0}<br>""".format(doc.get('student_id'))
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name') or '-')
    recepients_list=[]
    for row in doc.departments_clearance_status:
        recepients_list.append(row.department_email_id)
    send_mail(recepients_list,'Student Clearance Status',msg)
    frappe.msgprint("Email sent to all mentioned departments")

def send_pendingDues_notification_to_student(doc):
    msg="""<p>Dear Student,You have Pending dues, please refer to department clearance status table.</p><br>"""
    student_email=doc.student_email_address
    send_mail(student_email,'Student Clearance Status',msg)
    frappe.msgprint("Email sent to %s"%(doc.student_name))

def branch_change_application_approved(doc):
    msg="""<p>Your application <b>{0}</b> for Branch Change is Approved. </p><br>""".format(doc.get('name'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('sliding_in_program') or '-')
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('sliding_in_semester') or '-')
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application Status',msg)

def branch_change_application_rejected(doc):
    msg="""<p>Your application <b>{0}</b> for Branch Change is Rejected. </p><br>""".format(doc.get('name'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('sliding_in_program') or '-')
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('sliding_in_semester') or '-')
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))
    
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application Status',msg)

def mentor_allocation_submit(doc):
    # For Mentor
    msg="""<p>You have been assigned the mentees for this Academic Year <b>{0}</b></p><br>""".format(doc.get('academic_year'))
    msg+="""<b>-----------Mentor-Mentee Group Details-----------</b><br>"""
    msg+="""<b>Mentor Name:</b>  {0}<br>""".format(doc.get('mentor_name') or '-')
    msg+="""<b>Alloaction From:</b>  {0}<br>""".format(doc.get('allocation_from') or '-')
    msg+="""<b>Alloaction To:</b>  {0}<br>""".format(doc.get('allocation_to') or '-')
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('program') or '-')
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('semester') or '-')
    msg+="""<b>Student Table:</b>  <a href="{0}">Click here to see the students</a><br>""".format(get_url_to_form('Mentor Allocation',doc.get('name')))

    send_mail(frappe.db.get_value("Employee",doc.get('mentor'),"user_id"),'Mentor Allocation', msg)

    # For Student
    for st in doc.get("mentee_list"):
        msg="""<p>You have been assigned the Mentor for this Academic Year <b>{0}</b></p><br>""".format(doc.get('academic_year'))
        msg+="""<b>-----------Mentor-Mentee Group Details-----------</b><br>"""
        msg+="""<b>Mentor Name:</b>  {0}<br>""".format(doc.get('mentor_name') or '-')
        msg+="""<b>Alloaction From:</b>  {0}<br>""".format(doc.get('allocation_from') or '-')
        msg+="""<b>Alloaction To:</b>  {0}<br>""".format(doc.get('allocation_to') or '-')
        msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('program') or '-')
        msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('semester') or '-')
        msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))

        send_mail(frappe.db.get_value("Student",st.get('student'),"student_email_id"),'Mentor Allocation',msg)


def exam_declaration_submit(doc):
    sub = "Exam has been declared for your program {0}".format(doc.exam_program)
    msg="""<p>--------Exam Details----------</p>"""
    msg+="""<p>Exam Declaration Id : {0}</p>""".format(doc.name)
    msg+="""<p>Exam Program : {0}</p>""".format(doc.exam_program)
    msg+="""<p>Application start date : {0}</p>""".format(doc.application_form_start_date)
    msg+="""<p>Application End Date : {0}</p>""".format(doc.application_form_end_date)
    msg+="""<p>Blocklist Date:{0}</p>""".format(doc.block_list_display_date)
    msg+="""<p>Admit Card Issue Date : {0}</p>""".format(doc.admit_card_issue_date)
    msg+="""<p>Exam Semester : </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Semester</th>"""
    for d in doc.get("semesters"):
        msg += """<tr><td>{0}</td></tr>""".format(str(d.get('semester'))) 
    msg += "</table>"
    if doc.exam_fees_applicable == "YES":
        msg+="""<p>Exam Fees : </p>"""
        msg += """</u></b></p><table class='table table-bordered'><tr>
            <th>Student Category</th><th>Fee Structure</th><th>Amount</th><th>Due Date</th>"""
        for d in doc.get("fee_structure"):
            msg += "<tr><td>" + """{0}""".format(str(d.get('student_category'))) + "</td><td>" + str(d.get('fee_structure') or '') + "</td><td>" + str(d.get('amount')) + "</td><td>" + str(d.get('due_date'))  + "</td></tr>"
        msg += "</table>"
    
    for s in frappe.db.get_all('Current Educational Details',{'programs': doc.exam_program,"semesters":["IN",[d.semester for d in doc.get("semesters")]],'academic_year': doc.academic_year, 'academic_term':doc.academic_term}, 'parent'):
        send_mail(frappe.db.get_value("Student",s.get('parent'),"student_email_id"),sub,msg)

def post_exam_declaration_save(doc):
    msg="""<p>--------Post Exam Details----------</p>"""
    msg+="""<p>Post Exam Declaration Id : {0}</p>""".format(doc.name)
    msg+="""<p>Exam Declaration Id : {0}</p>""".format(doc.exam_declaration)
    exam_declrn = frappe.db.get_all('Exam Declaration', {'name':doc.exam_declaration})
    ed_doc = frappe.get_doc('Exam Declaration',exam_declrn[0]['name'])
    exam_program = ''
    msg+="""<p>Exam Program : {0}</p>""".format(ed_doc.exam_program)
    msg+="""<p>Application start date : {0}</p>""".format(doc.start_date or "")
    msg+="""<p>Application End Date : {0}</p>""".format(doc.end_date or "")
    msg+="""<p>Exam Semester : </p>  """
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Semester</th>"""
    for d in ed_doc.get("semesters"):
        msg += """<tr><td>{0}</td></tr>""".format(str(d.get('semester'))) 
    msg += "</table>"
    if doc.fees_applicable == "YES":
        msg+="""<p>Exam Fees : </p>"""
        msg += """</u></b></p><table class='table table-bordered'><tr>
            <th>Student Category</th><th>Fee Structure</th><th>Amount</th><th>Due Date</th>"""
        for d in doc.get("fee_structure"):
            msg += "<tr><td>" + """{0}""".format(str(d.get('student_category'))) + "</td><td>" + str(d.get('fee_structure') or '') + "</td><td>" + str(d.get('amount')) + "</td><td>" + str(d.get('due_date'))  + "</td></tr>"
        msg += "</table>"
    sub = "Post Exam has been declared for your program {0}".format(ed_doc.exam_program)
    student_list = frappe.db.get_all('Program Enrollment',{'programs': ed_doc.exam_program}, 'student')
    for s in student_list:
        send_mail(frappe.db.get_value("Student",s.get('student'),"student_email_id"),sub,msg)

def student_exam_block_submit(doc):
    sub = "Exam has been declared for your program {0}".format(doc.program)
    msg="""<p>--------Exam Details----------</p>"""
    msg+="""<p>>Exam Declaration : {0}</p>""".format(doc.exam_declaration)
    msg+="""<p>Program of Exam : {0}</p>""".format(doc.program)
    exam_declrn = frappe.db.get_all('Exam Declaration', {'name':doc.exam_declaration})
    for e in exam_declrn:
        msg+="""<p>Academic Year : {0}</p>""".format(e.academic_year)
        msg+="""<p>Academic Term : {0}</p>""".format(e.academic_term)
    for s in doc.student_block_item:
        send_mail(frappe.db.get_value("Student",s.get('student'),"student_email_id"),sub,msg)

@frappe.whitelist()
def placement_drive_application_submit(doc):
    import json
    doc = json.loads(doc)
    student_email_id = frappe.db.get_value("Student",{'name':doc.get('student')}, "student_email_id")
    sub = "Application Status"
    if doc.get('status') == "Shortlisted":
        sub = "Your application {0} is shortlisted for placement drive {1}".format(doc.get('name'), doc.get('placement_drive'))
    if doc.get('status') == "Hired":
        sub = "Your application {0} is hired for placement drive {1}".format(doc.get('name'), doc.get('placement_drive'))
    if doc.get('status') == "Rejected":
        sub = "Your application {0} is rejected for placement drive {1}".format(doc.get('name'), doc.get('placement_drive'))
    msg="""<p>--------Student Details----------</p>"""
    msg+="""<p>Student Name : {0}</p>""".format(doc.get('student_name'))
    msg+="""<p>Student Email: {0}</p>""".format(student_email_id)
    msg+="""<p>Placement Drive Name: {0}</p>""".format(doc.get('placement_drive'))
    msg+="""<p>Status: {0}</p>""".format(doc.get('status'))
    send_mail(student_email_id, sub, msg)

def placement_drive_submit(doc):
    sub = "Placement Drive is declared for {0}".format(doc.placement_company)
    msg="""<p>--------Placement Drive Details----------</p>"""
    msg+="""<p>Company Name : {0}</p>""".format(doc.placement_company)
    msg+="""<p>Application Start Date : {0}</p>""".format(doc.application_start_date)
    msg+="""<p>Application End Date :{0}</p>""".format(doc.application_end_date)
    msg+="""<p>Position: </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
            <th>Designation</th><th>No. of Positions</th>"""
    for d in doc.get("designations_position"):
        msg += "<tr><td>" + """{0}""".format(str(d.get('designation'))) + "</td><td>" + str(d.get('no_of_position') or '') + "</td></tr>"
    msg += "</table>"
    msg+="""<p>Applicable Programs: </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
            <th>Programs</th><th>Semester</th>"""
    for d in doc.get("for_programs"):
        msg += "<tr><td>" + """{0}""".format(str(d.get('programs'))) + "</td><td>" + str(d.get('semester') or '') + "</td></tr>"
    msg += "</table>"
    msg+="""<p>Eligibility Criteria: {0}</p>""".format(doc.eligibility_criteria)
    msg+="""<p>Placement Process: {0}</p>""".format(doc.process_of_placement)
    for s in doc.for_programs:
        student_list = frappe.get_all("Current Educational Details",{'programs':s.programs, 'semesters':s.semester}, 'parent')
        for stud in student_list:
            send_mail(frappe.db.get_value("Student",stud.parent,"student_email_id"),sub,msg)

def exam_declaration_for_instructor_submit(doc):
    sub = "Exam Declaration for {0}".format(doc.exam_program)
    msg="""<p>--------Exam Details----------</p>"""
    msg="""<p>The exam has been declared for {0}</p>""".format(doc.exam_program)
    msg+="""<p>Exam Declaration Id : {0}</p>""".format(doc.name)
    msg+="""<p>Exam Program : {0}</p>""".format(doc.exam_program)

    msg+="""<p>Exam start date : {0}</p>""".format(doc.exam_start_date)
    msg+="""<p>Exam End Date : {0}</p>""".format(doc.exam_end_date)
    msg+="""<p>Exam Semester:</p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Semester</th>"""
    for d in doc.get("semesters"):
        msg += """<tr><td>{0}</td></tr>""".format(str(d.get('semester'))) 
    msg += "</table>"
    msg+="""<p>Offered Courses Offered : </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Courses</th><th>Course Name</th><th>Course Code</th><th>Semester</th><th>Examination Date</th><th>From Time</th><th>To Time</th><th>Total Duration(In Hours)</th>"""
    for d in doc.get("courses_offered"):
        msg += "<tr><td>" + """{0}""".format(str(d.get('courses'))) + "</td><td>" + str(d.get('course_name') or '') + "</td><td>" + str(d.get('course_code')) + "</td><td>" + str(d.get('semester')) + "</td><td>" + str(d.get('examination_date')) + "</td><td>" + str(d.get('from_time')) + "</td><td>" + str(d.get('to_time')) + "</td><td>" + str(d.get('total_duration_in_hours')) +  "</td></tr>"
    msg += "</table>"
    semester_list =[s.semester for s in doc.semesters]
    course_list = [c.courses for c in doc.courses_offered]
    instructor_list = frappe.db.get_all('Instructor Log',{'programs': doc.exam_program, 'program': ('in', semester_list), 'academic_year': doc.academic_year, 'academic_term':doc.academic_term}, 'parent')
    for i in instructor_list:
        instructor_name = frappe.db.get_value('Instructor',{'name':i.get('parent')},'instructor_name')
        send_mail(frappe.db.get_value("User",{'full_name':instructor_name, 'enabled':1},"email"),sub,msg)

def exam_evaluation_plan_for_paper_setter_submit(doc):
    
    # msg1="""<p>--------Exam Details----------</p>"""
    # msg1+="""<p>Exam Declaration : {0}</p>""".format(doc.exam_declaration)
    # msg1+="""<p>Program : {0}</p>""".format(doc.programs)
    # msg1+="""<p>Semster :  {0}</p>""".format(doc.program)
    # for e in doc.examiners_list:
    #     msg = ""
    #     msg+="""<p>Course : {0}</p><p>Course Name:{1}</p><p>Course Code:{2}</p>""".format(e.course,e.course_name,e.course_code)
    #     msg+="""<p>Assessment Criteria:{0}</p>""".format(doc.assessment_criteria)
    #     msg+="""<p>Academic Year :{0}</p>""".format(doc.academic_year)
    #     msg+="""<p>Academic Term:{0}</p>""".format(doc.academic_term)
    #     msg+="""<p>Paper Setting Start Date:{0}</p>""".format(doc.paper_setting_start_date)
    #     msg+="""<p>Paper Setting End Date:{0}</p>""".format(doc.paper_setting_end_date)


  
    for e in doc.examiners_list:
        sub = "You are invited to set the paper for exam declaration {0}".format(doc.exam_declaration)
        msg="""
        <table style="line-height: 1em;width: 100%;" border="1" cellpadding="2" cellspacing="2">
        <thead>
            <tr><th colspan="11"><b>Examination Details</b></th></tr>
            <tr>
                <th class="text-center" style="width:9%; font-size:14px;">Exam Declaration</th>
                <th class="text-center" style="width:9%; font-size:14px;">Program</th>
                <th class="text-center" style="width:10%; font-size:14px;">Semester</th>
                <th class="text-center" style="width:9%; font-size:14px;">Course</th>
                <th class="text-center" style="width:9%; font-size:14px;">Course Name</th>
                <th class="text-center" style="width:9%; font-size:14px;">Course Code</th>
                <th class="text-center" style="width:9%; font-size:14px;">Assessment Criteria</th>
                <th class="text-center" style="width:9%; font-size:14px;">Academic Year</th>
                <th class="text-center" style="width:9%; font-size:14px;">Academic Term</th>
                <th class="text-center" style="width:9%; font-size:14px;">Paper Setting Start Date</th>
                <th class="text-center" style="width:9%; font-size:14px;">Paper Setting End Date</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">{0}</td>""".format(doc.exam_declaration)
        msg+="""<td class="text-center">{0}</td>""".format(doc.programs)
        msg+="""<td class="text-center">{0}</td>""".format(doc.program)
        msg+="""<td class="text-center">{0}</td>""".format(e.course)
        msg+="""<td class="text-center">{0}</td>""".format(e.course_name)
        msg+="""<td class="text-center">{0}</td>""".format(e.course_code)
        msg+="""<td class="text-center">{0}</td>""".format(doc.assessment_criteria)
        msg+="""<td class="text-center">{0}</td>""".format(doc.academic_year)
        msg+="""<td class="text-center">{0}</td>""".format(doc.academic_term)
        msg+="""<td class="text-center">{0}</td>""".format(doc.paper_setting_start_date)
        msg+="""<td class="text-center">{0}</td>""".format(doc.paper_setting_end_date)
        msg+="""</tr>
        </tbody>
        </table>"""
        employee = frappe.db.get_value('Instructor',{'name':e.paper_setter},'employee')
        email = frappe.db.get_value('Employee',{'name':employee},'user_id')
        if frappe.db.get_value("User",{'email':email, 'enabled':1},"email"):
            # send_mail(email,sub,msg1+msg)
            send_mail(email,sub,msg)


def exam_evaluation_plan_for_moderator_submit(doc):
    
    # msg1="""<p>--------Exam Details----------</p>"""
    # msg1+="""<p>Exam Declaration : {0}</p>""".format(doc.exam_declaration)
    # msg1+="""<p>Program : {0}</p>""".format(doc.programs)
    # msg1+="""<p>Semster :  {0}</p>""".format(doc.program)
    # for e in doc.moderator_list:
    #     msg = ""
    #     msg+="""<p>Course : {0}</p><p>Course Name:{1}</p><p>Course Code:{2}</p>""".format(e.course,e.course_name,e.course_code)
    #     msg+="""<p>Assessment Criteria:{0}</p>""".format(doc.assessment_criteria)
    #     msg+="""<p>Academic Year :{0}</p>""".format(doc.academic_year)
    #     msg+="""<p>Academic Term:{0}</p>""".format(doc.academic_term)
    #     msg+="""<p>Paper Setting Start Date:{0}</p>""".format(doc.paper_setting_start_date)
    #     msg+="""<p>Paper Setting End Date:{0}</p>""".format(doc.paper_setting_end_date)
    #     employee = frappe.db.get_value('Instructor',{'name':e.moderator},'employee')
    #     email = frappe.db.get_value('Employee',{'name':employee},'user_id')
    #     if frappe.db.get_value("User",{'email':email, 'enabled':1},"email"):
    #         send_mail(email,sub,msg1+msg)


    for e in doc.moderator_list:
        sub = "You are invited as moderator for exam declaration {0}".format(doc.exam_declaration)
        msg="""
        <table style="line-height: 1em;width: 100%;" border="1" cellpadding="2" cellspacing="2">
        <thead>
            <tr><th colspan="11"><b>Examination Details</b></th></tr>
            <tr>
                <th class="text-center" style="width:9%; font-size:14px;">Exam Declaration</th>
                <th class="text-center" style="width:9%; font-size:14px;">Program</th>
                <th class="text-center" style="width:10%; font-size:14px;">Semester</th>
                <th class="text-center" style="width:9%; font-size:14px;">Course</th>
                <th class="text-center" style="width:9%; font-size:14px;">Course Name</th>
                <th class="text-center" style="width:9%; font-size:14px;">Course Code</th>
                <th class="text-center" style="width:9%; font-size:14px;">Assessment Criteria</th>
                <th class="text-center" style="width:9%; font-size:14px;">Academic Year</th>
                <th class="text-center" style="width:9%; font-size:14px;">Academic Term</th>
                <th class="text-center" style="width:9%; font-size:14px;">Paper Setting Start Date</th>
                <th class="text-center" style="width:9%; font-size:14px;">Paper Setting End Date</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">{0}</td>""".format(doc.exam_declaration)
        msg+="""<td class="text-center">{0}</td>""".format(doc.programs)
        msg+="""<td class="text-center">{0}</td>""".format(doc.program)
        msg+="""<td class="text-center">{0}</td>""".format(e.course)
        msg+="""<td class="text-center">{0}</td>""".format(e.course_name)
        msg+="""<td class="text-center">{0}</td>""".format(e.course_code)
        msg+="""<td class="text-center">{0}</td>""".format(doc.assessment_criteria)
        msg+="""<td class="text-center">{0}</td>""".format(doc.academic_year)
        msg+="""<td class="text-center">{0}</td>""".format(doc.academic_term)
        msg+="""<td class="text-center">{0}</td>""".format(doc.paper_setting_start_date)
        msg+="""<td class="text-center">{0}</td>""".format(doc.paper_setting_end_date)
        msg+="""</tr>
        </tbody>
        </table>"""
        employee = frappe.db.get_value('Instructor',{'name':e.moderator},'employee')
        email = frappe.db.get_value('Employee',{'name':employee},'user_id')
        if frappe.db.get_value("User",{'email':email, 'enabled':1},"email"):
            # send_mail(email,sub,msg1+msg)
            send_mail(email,sub,msg)

def payment_entry_submit(doc):
    msg="""<p><b>Payment is Sucessfull</b></p><br>"""
    msg+="""<b>---------------------Payment Details---------------------</b><br>"""
    msg+="""<p>---------------------Type of Payment---------------------</p><br>"""
    msg+="""<b>Payment Entry No.:</b>  {0}<br>""".format(doc.get('name'))
    msg+="""<b>Date:</b>  {0}<br>""".format(format_date(doc.get('posting_date'), 'dd/mm/yyyy'))
    msg+="""<p>---------------------Payment From / TO---------------------</p><br>"""
    msg+="""<b>Name:</b>  {0}<br>""".format(doc.get('party_name') or '-')
    msg+="""<b>Roll Number:</b>  {0}<br>""".format(doc.get('roll_no') or '-' )
    msg+="""<b>Amount Paid:</b>  {0}<br>""".format(doc.get('paid_amount') or '-' )
    recipients = frappe.db.get_value("Student",doc.get('party'),"student_email_id")
    attachments = [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, print_format='Payment Entry Money Recipt')]
    send_mail(recipients,'Payment Successful',msg,attachments)

def employee_reporting_aprover(doc):
    sub="""<p><b>Profile Updation Notification</b></p><br>"""
    msg="""<b>---------------------Employee Details---------------------</b><br>"""
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc['employee_name'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    emp_profile_updation = get_url_to_form('Employee Profile Updation', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(emp_profile_updation)

    send_mail([doc['reporting_authority_email']],sub,msg)

    frappe.msgprint("Email sent to reporting authority")
def employee_hr(doc):
    sub="""<p><b>Profile Updation Notification</b></p><br>"""
    msg="""<b>---------------------Employee Details---------------------</b><br>"""
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc['employee_name'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    emp_profile_updation = get_url_to_form('Employee Profile Updation', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(emp_profile_updation)
    send_mail([doc['hr_email']],sub,msg)
    frappe.msgprint("Email sent to HR",[doc['hr_email']])
def send_mail_to_director(doc):
    sub="""<p><b>Leave Policy Request</b></p><br>"""
    msg="""<b>---------------------Leave Policy Details---------------------</b><br>"""
    msg+="""<b>Leave polciy:</b>  {0}<br>""".format(doc['leave_policy'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    leave_policy_url = get_url_to_form('Leave Policy', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(leave_policy_url)
    send_mail([doc['director_mail']],sub,msg)
    frappe.msgprint("Email sent to Director",[doc['director_mail']])
def send_mail_to_hr(doc):
    sub="""<p><b>Leave Policy Request</b></p><br>"""
    msg="""<b>---------------------Leave Policy Details---------------------</b><br>"""
    msg+="""<b>Leave polciy:</b>  {0}<br>""".format(doc['leave_policy'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    leave_policy_url = get_url_to_form('Leave policy', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(leave_policy_url)
    send_mail([doc['hr_mail']],sub,msg)
    frappe.msgprint("Email sent to HR",[doc['hr_mail']])

def shift_req_hr(doc):
    sub="""<p><b>Shift Request Approval Notification</b></p><br>"""

    msg="""<b>---------------------Shift Request Details---------------------</b><br>"""
    msg+="""<b>Employee ID:</b>  {0}<br>""".format(doc.get('employee'))
    msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc.get('employee_name'))
    msg+="""<b>Shift Type:</b>  {0}<br>""".format(doc.get('shift_type'))
    msg+="""<b>From Date:</b>  {0}<br>""".format(doc.get('from_date'))
    msg+="""<b>To Date:</b>  {0}<br>""".format(doc.get('to_date'))
    msg+="""<b>Status:</b>  {0}<br>""".format(doc.get('status'))
    
    send_mail(frappe.db.get_value("Shift Request",doc.get('name'),"hr_mail"),sub,msg)
    frappe.msgprint("Status mail sent to HR")

#Notification for Employee Suggestion 
def notify_hr(doc):
    sub="""<p><b>Employee Suggestion</b></p><br>"""
    msg="""<b>---------------------Employee Suggestion Details---------------------</b><br>"""
    msg+="""<b>Employee Suggestion:</b>  {0}<br>""".format(doc['employee_suggestion'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    employee_suggestion_url = get_url_to_form('Employee Suggestion', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(employee_suggestion_url)
    send_mail([doc['hr_email']],sub,msg)
    frappe.msgprint("Email sent to HR",[doc['hr_mail']])
def notify_director(doc):
    sub="""<p><b>Employee Suggestion</b></p><br>"""
    msg="""<b>---------------------Employee Suggestion Details---------------------</b><br>"""
    msg+="""<b>Employee Suggestion:</b>  {0}<br>""".format(doc['employee_suggestion'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    employee_suggestion_url = get_url_to_form('Employee Suggestion', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(employee_suggestion_url)
    send_mail([doc['director_email']],sub,msg)
    frappe.msgprint("Email sent to Director",[doc['director_email']])
def notify_employee(doc):
    sub="""<p><b>Employee Suggestion</b></p><br>"""
    msg="""<b>---------------------Employee Suggestion Details---------------------</b><br>"""
    msg+="""<b>Employee Suggestion:</b>  {0}<br>""".format(doc['employee_suggestion'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    employee_suggestion_url = get_url_to_form('Employee Suggestion', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(employee_suggestion_url)
    send_mail([doc['employee_email']],sub,msg)
    frappe.msgprint("Email sent to Employee",[doc['employee_email']])

# def online_payment_submit(doc):
#     msg="""<p><b>Payment Status</b></p><br>"""
#     msg+="""<b>---------------------Payment Details---------------------</b><br>"""
#     msg+="""<p>---------------------Type of Payment---------------------</p><br>"""
#     msg+="""<b>Payment Entry No.:</b>  {0}<br>""".format(doc.get('name'))
#     msg+="""<b>Date:</b>  {0}<br>""".format(doc.get('date_time_of_transaction'))
#     msg+="""<p>---------------------Payment From / TO---------------------</p><br>"""
#     msg+="""<b>Name:</b>  {0}<br>""".format(doc.get('party_name') or '-')
#     msg+="""<b>Roll Number:</b>  {0}<br>""".format(doc.get('roll_no') or '-' )
#     msg+="""<b>Amount Paid:</b>  {0}<br>""".format(doc.get('paying_amount') or '-' )
#     msg+="""<b>Transaction Id:</b>  {0}<br>""".format(doc.get('transaction_id') or '-' )
#     msg+="""<b>Transaction Status:</b>  {0}<br>""".format(doc.get('transaction_status') or '-' )

#     recipients = frappe.db.get_value("Student",doc.get('party'),"student_email_id")
#     attachments = None
#     send_mail(recipients,'Payment Status',msg,attachments)


def online_payment_submit(doc):
   
    msg="""<b>---------------------Payment Details---------------------</b><br>"""
    msg+="""<b>Payment Entry No.:</b>  {0}<br>""".format(doc.get('name'))
    msg+="""<b>Date:</b>  {0}<br>""".format(doc.get('date_time_of_transaction'))
    msg+="""<p>---------------------Payment From / TO---------------------</p><br>"""
    msg+="""<b>Name:</b>  {0}<br>""".format(doc.get('party_name') or '-')
    msg+="""<b>Roll Number:</b>  {0}<br>""".format(doc.get('roll_no') or '-' )
    msg+="""<b>Total Outstanding Amount :</b>  {0}<br>""".format(doc.get('total_outstanding_amout') or '-' )
    msg+="""<b>Amount Paid:</b>  {0}<br>""".format(doc.get('paying_amount') or '-' )
    msg+="""<b>Transaction Id:</b>  {0}<br>""".format(doc.get('transaction_id') or '-' )
    msg+="""<b>Transaction Status:</b>  {0}<br>""".format(doc.get('transaction_status') or '-' )
    recipients = frappe.db.get_value("Student",doc.get('party'),"student_email_id")
    attachments = None
    send_mail(recipients,'Payment Details',msg,attachments)

##### Notification for Procurement and Inventory Management #####
#####   START   #####
def item_expiry(doc):
    msg="""<b>---------------------Item Warranty Expiry Remainder---------------------</b><br>"""
    msg+="""<b>Warranty for {0} will be expiring in 30 days""".format(doc.get('item_name'))
    recipients_list = list(frappe.db.sql("select department_email_id from `tabDepartment Email ID`"))
    recipients = recipients_list[0]
    attachments = None
    send_mail(recipients,'Item',msg,attachments)

def changed_impaneled_price(doc):
    msg="""<b>---------------------Impanelement Price Changed for Item {0}---------------------</b><br>""".format(doc.get('item_name'))
    recipients = doc.supllier_email
    attachments = None
    send_mail(recipients,'Item Price',msg,attachments)

def all_items_received(doc):
    msg="""---------------------All Item for PO <b>{0}</b> have been received""".format(doc.get('name'))
    recipients = doc.supplier_email
    attachments = None
    send_mail(recipients,'Purchase Order',msg,attachments)

def purchase_requisition_raised(doc):
    msg="""<b>---------------------Purchase Requisition raised by {0} department---------------------</b><br>""".format(doc.get('department'))
    msg+="""Please login to the Application to see details regarding the requisition raised"""
    recipients_list = list(frappe.db.sql("select department_email_id from `tabDepartment Email ID`"))
    recipients = recipients_list[0]
    attachments = None
    send_mail(recipients,'Material Request',msg,attachments)

def received_in_inventory(doc):
    msg="""<b>---------------------Purchase Requisition: {0} received in Store---------------------</b><br>""".format(doc.get('name'))
    msg+="""Please completed the Issue of requested material to {0} department""".format(doc.get('department'))
    recipients_list = list(frappe.db.sql("select department_email_id from `tabDepartment Email ID`"))
    recipients = recipients_list[0]
    attachments = None
    send_mail(recipients,'Material Request',msg,attachments)

def received_by_department(doc):
    msg="""<b>---------------------Purchase Requisition: {0} received---------------------</b><br>"""
    msg+="""Items received on dated: {0}""".format(doc.get('transaction_date'))
    msg+="""For Purchase requisition number: {0}""".format(doc.get('name'))
    recipients = doc.department_email
    attachments = None
    send_mail(recipients,'Material Request',msg,attachments)

def workflow_wating_approval(doc, receipient):
    msg="""<b>---------------------Workflow awaiting response---------------------</b><br>"""
    msg+="""You have received a workflow waiting for your review and approval"""
    recipients = receipient
    attachments = None
    send_mail(recipients,'Material Request',msg,attachments)

#####   END   #####

# def has_default_email_acc():
# 	for d in frappe.get_all("Email Account", {"default_outgoing":1}):
# 	   return "true"
# 	return ""
def has_default_email_acc():
    for d in frappe.get_all('Email Account',{"default_outgoing":1}):
        return "true"
    return ""

def send_mail(recipients=None,subject=None,message=None,attachments=None):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients or [],expose_recipients="header",subject=subject,message = message,attachments=attachments,with_container=False)        

def send_email_to_course_advisor(self):
    flag=0
    msg="""<p>Leave Application Submitted Sucessfully by <b> {0}</b>""".format(self.get('student_name') or '-')
    for t in self.get('current_education_details'):
        programs=t.programs
        semesters=t.semesters
        academic_year=t.academic_year
        academic_term=t.academic_term

    get_ca_cm_assignment = frappe.get_all("Course Advisor and Manager Assignment",filters=[['programs','=',programs],['semester','=',semesters],['academic_year','=',academic_year],['academic_term','=',academic_term]],fields=['name','cm_email','ca_email','course_manager_name','course_advisor_name'])

    if get_ca_cm_assignment:
        get_students = frappe.get_all("Course Manager Assignment Student Details", {"parent":get_ca_cm_assignment[0]['name']}, ['student','student_name'])
        if get_students:
            for t in get_students:
                if self.student == t['student']:
                    flag=1

    if flag==1:
        recipients = get_ca_cm_assignment[0]['ca_email']
        course_advisor_name = get_ca_cm_assignment[0]['course_advisor_name']
        send_mail(recipients,'Leave Application Notification',msg)
        frappe.msgprint("Email sent to Course Advisor: %s"%(course_advisor_name))

def send_email_to_course_manager(self):
    flag=0
    msg="""<p>Leave Application Submitted Sucessfully by <b> {0}</b>""".format(self.get('student_name') or '-')
    for t in self.get('current_education_details'):
        programs=t.programs
        semesters=t.semesters
        academic_year=t.academic_year
        academic_term=t.academic_term

    get_ca_cm_assignment = frappe.get_all("Course Advisor and Manager Assignment",filters=[['programs','=',programs],['semester','=',semesters],['academic_year','=',academic_year],['academic_term','=',academic_term]],fields=['name','cm_email','ca_email','course_manager_name','course_advisor_name'])

    if get_ca_cm_assignment:
        get_students = frappe.get_all("Course Manager Assignment Student Details", {"parent":get_ca_cm_assignment[0]['name']}, ['student','student_name'])
        if get_students:
            for t in get_students:
                if self.student == t['student']:
                    flag=1

    if flag==1:
        recipients = get_ca_cm_assignment[0]['cm_email']
        course_manager_name = get_ca_cm_assignment[0]['course_manager_name']
        send_mail(recipients,'Leave Application Notification',msg)
        frappe.msgprint("Email sent to Course Manager: %s"%(course_manager_name))

def send_email_to_student(self):
    flag=0
    for t in self.get('current_education_details'):
        programs=t.programs
        semesters=t.semesters
        academic_year=t.academic_year
        academic_term=t.academic_term

    get_ca_cm_assignment = frappe.get_all("Course Advisor and Manager Assignment",filters=[['programs','=',programs],['semester','=',semesters],['academic_year','=',academic_year],['academic_term','=',academic_term]],fields=['name','cm_email','ca_email','course_manager_name','course_advisor_name'])
    
    if get_ca_cm_assignment:
        course_manager_name = get_ca_cm_assignment[0]['course_manager_name']
        course_advisor_name = get_ca_cm_assignment[0]['course_advisor_name']

        get_student_email = frappe.get_all("Student",{'name':self.student},['student_email_id'])

        if self.get('workflow_state') == "Rejected by Class Advisor":
            msg="""<p>Leave Application <b>{0}</b> has been rejected by <b>{1}</b>""".format(self.get('name') or '-',course_advisor_name)
        elif self.get('workflow_state') == "Rejected":
            msg="""<p>Leave Application <b>{0}</b> has been rejected by <b>{1}</b>""".format(self.get('name') or '-',course_manager_name)
        elif self.get('workflow_state') == "Approved":
            msg="""<p>Leave Application <b>{0}</b> has been approved by <b>{1}</b>""".format(self.get('name') or '-',course_manager_name)
        else :
            pass

        if get_ca_cm_assignment:
            get_students = frappe.get_all("Course Manager Assignment Student Details", {"parent":get_ca_cm_assignment[0]['name']}, ['student','student_name'])
            if get_students:
                for t in get_students:
                    if self.student == t['student']:
                        flag=1
        recipients=[]
        if flag==1:
            recipient1 = get_student_email[0]['student_email_id']
            recipients.append(recipient1)
            recipient2 = get_ca_cm_assignment[0]['ca_email']
            recipients.append(recipient2)
            recipient3 = get_ca_cm_assignment[0]['cm_email']
            recipients.append(recipient3)
            send_mail(recipients,'Leave Application Notification',msg)
            frappe.msgprint("Email sent to Student: %s"%(self.get('student_name')))
            frappe.msgprint("Email sent to Course Advisor: %s"%(course_advisor_name))
            frappe.msgprint("Email sent to Course Manager: %s"%(course_manager_name))

def send_email_to_deputy_director(self):
    flag=0
    for t in self.get('current_education_details'):
        programs=t.programs
        semesters=t.semesters
        academic_year=t.academic_year
        academic_term=t.academic_term

    get_ca_cm_assignment = frappe.get_all("Course Advisor and Manager Assignment",filters=[['programs','=',programs],['semester','=',semesters],['academic_year','=',academic_year],['academic_term','=',academic_term]],fields=['name', 'dd_name', 'dd_email', 'course_manager_name'])
    
    if get_ca_cm_assignment:
        dd_name = get_ca_cm_assignment[0]['dd_name']
        course_manager_name = get_ca_cm_assignment[0]['course_manager_name']

        if self.get('workflow_state') == "Approved":
            msg="""<p>Leave Application <b>{0}</b> has been approved by <b>{1}</b>""".format(self.get('name') or '-',course_manager_name)
        else :
            pass

        if get_ca_cm_assignment:
            get_students = frappe.get_all("Course Manager Assignment Student Details", {"parent":get_ca_cm_assignment[0]['name']}, ['student','student_name'])
            if get_students:
                for t in get_students:
                    if self.student == t['student']:
                        flag=1
        if flag==1:
            recipients = get_ca_cm_assignment[0]['dd_email']
            send_mail(recipients,'Leave Application Notification',msg)
            frappe.msgprint("Email sent to Deputy Director: %s"%(dd_name))

def send_mail_to_students_mweg(self):
    for t in self.get("student_list"):
        student_name=t.student_name
        student_no=t.student_no
        student_emails = frappe.get_all("Student",{'name':student_no},['student_email_id'])
        mail_id=student_emails[0]['student_email_id']
        group_name=t.group_name

        for d in self.get("scheduling_group_exam"):
            if group_name == d.group_name:
                exam_date=d.examination_date
                from_date=d.from_time
                to_time=d.to_time
                msg="""<p>Dear Student, <br>"""
                msg+="""<p>This is to inform you that the <b>{0}</b> for the academic year <b>{1}</b> of <b>{2}</b> will be on <b>{3}</b> from <b>{4}</b> to <b>{5}</b>.<br>""".format(self.get('exam_name'),self.get('academic_year'),self.get('modules_name'),exam_date,from_date,to_time)
                msg+="""<p>The Exam is being conducted for <b>{0}</b> for <b>{1}</b>.""".format(self.get('semester'),self.get('exam_course'))
        recipients = mail_id
        send_mail(recipients,'Exam Schedule Notification',msg)
        frappe.msgprint("Email sent to Student: %s"%(student_name))

def send_mail_to_trainers_mweg(self):
    msg="""<p>Dear Sir/Madam, <br>"""
    msg+="""<p>This is to inform you that the <b>{0}</b> for the academic year <b>{1}</b> of <b>{2}</b> will be from <b>{3}</b> to <b>{4}</b>. <br>""".format(self.get('exam_name'),self.get('academic_year'),self.get('modules_name'),self.get('module_exam_start_date'),self.get('module_exam_end_date'))
    msg+="""<p>The Exam is being conducted for <b>{0}</b> for <b>{1}</b>.""".format(self.get('semester'),self.get('exam_course'))
    marker_name = self.marker_name
    course_manager_name = self.course_manager_name
    checker_name = self.checker
    recepients_list=[]
    marker_emp = frappe.get_all("Instructor",{'name':marker_name},['employee'])
    if marker_emp:
        marker_idx=marker_emp[0]['employee']
        marker_email = frappe.get_all("Employee",{'name':marker_idx},['user_id'])
        if marker_email:
            marker_email_idx = marker_email[0]['user_id']
            recepients_list.append(marker_email_idx)
    
    gust_emp = frappe.get_all("Instructor",{'name':marker_name},['email_id_for_guest_trainers'])
    if gust_emp:
        gust_email=gust_emp[0]['email_id_for_guest_trainers']
        recepients_list.append(gust_email)

    course_manager_emp = frappe.get_all("Instructor",{'name':course_manager_name},['employee'])
    if course_manager_emp:
        cm_idx=course_manager_emp[0]['employee']
        cm_email = frappe.get_all("Employee",{'name':cm_idx},['user_id'])
        if cm_email:
            cm_email_idx = cm_email[0]['user_id']
            recepients_list.append(cm_email_idx)
    
    cm_gust_emp = frappe.get_all("Instructor",{'name':course_manager_name},['email_id_for_guest_trainers'])
    if cm_gust_emp:
        cm_gust_email=cm_gust_emp[0]['email_id_for_guest_trainers']
        recepients_list.append(cm_gust_email)
    
    checker_emp = frappe.get_all("Instructor",{'name':checker_name},['employee'])
    if checker_emp:
        checker_idx=checker_emp[0]['employee']
        checker_email = frappe.get_all("Employee",{'name':checker_idx},['user_id'])
        if checker_email:
            checker_email_idx = checker_email[0]['user_id']
            recepients_list.append(checker_email_idx)
    
    chk_gust_emp = frappe.get_all("Instructor",{'name':checker_name},['email_id_for_guest_trainers'])
    if chk_gust_emp:
        chk_gust_email=gust_emp[0]['email_id_for_guest_trainers']
        recepients_list.append(chk_gust_email)

    for t in self.get("invigilator_details_table"):
        emp = t.trainer
        emp_id_list = frappe.get_all("Instructor", {'name': emp}, ['employee'])
        if emp_id_list:
            emp_id = emp_id_list[0]['employee']
            emp_email_list = frappe.get_all("Employee", {'name': emp_id}, ['user_id'])
            if emp_email_list:
                emp_email = emp_email_list[0]['user_id']
                recepients_list.append(emp_email)

    for t in self.get("invigilator_details_table"):
        emp = t.trainer
        guest_emp = frappe.get_all("Instructor", {'name': emp}, ['email_id_for_guest_trainers'])
        if guest_emp:
            guest_emp_email = guest_emp[0]['email_id_for_guest_trainers']
            recepients_list.append(guest_emp_email)
    
    recepients_list_rem_dup = list(set(recepients_list))
    recepients_list_rem_dup_and_none = list(filter(lambda item: item is not None, recepients_list_rem_dup))
    send_mail(recepients_list_rem_dup_and_none,'Exam Schedule Notification',msg)
    frappe.msgprint("Email sent to Marker, Course Manager, Checker and Invigilator(s)")

    

   #################  Notification Coding for Employee Resignation #######################

def sendHR(doc):
    sub="""<p><b>Employee Resignation</b></p><br>"""
    msg="""<b>---------------------Resignation Details---------------------</b><br>"""
    msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    resignation_url = get_url_to_form('Employee Resignation', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
    msg+="""<p><b>Initiate the Separation Process for the Employee if it is Approved</b></p><br>"""
    send_mail([doc['hr_mail']],sub,msg)
    frappe.msgprint("Confirmation mail sent to HR",[doc['hr_mail']])
def sendEmployee(doc):
    sub="""<p><b>Employee Resignation</b></p><br>"""
    msg="""<b>---------------------Resignation Details---------------------</b><br>"""
    msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    resignation_url = get_url_to_form('Employee Resignation', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
    send_mail([doc['employee_mail']],sub,msg)
    frappe.msgprint("Confirmation mail sent to Employee",[doc['employee_mail']])
def sendRa(doc):
    sub="""<p><b>Employee Resignation</b></p><br>"""
    msg="""<b>---------------------Resignation Details---------------------</b><br>"""
    msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    resignation_url = get_url_to_form('Employee Resignation', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
    send_mail([doc['ra_mail']],sub,msg)
    frappe.msgprint("Mail sent to Reporting Authority for Approval",[doc['ra_mail']])
def sendDh(doc):
    sub="""<p><b>Employee Resignation</b></p><br>"""
    msg="""<b>---------------------Resignation Details---------------------</b><br>"""
    msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    resignation_url = get_url_to_form('Employee Resignation', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
    send_mail([doc['dh_mail']],sub,msg)
    frappe.msgprint("Mail sent to Department Head for Approval",[doc['dh_mail']])
def sendDirector(doc):
    sub="""<p><b>Employee Resignation</b></p><br>"""
    msg="""<b>---------------------Resignation Details---------------------</b><br>"""
    msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
    msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
    resignation_url = get_url_to_form('Employee Resignation', doc['name'])
    msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
    send_mail([doc['director_mail']],sub,msg)
    frappe.msgprint("Mail sent to Director for Approval",[doc['director_mail']])

def mentor_mentee_communication_submit(doc):
    mentor = frappe.db.get_value("Mentor Allocation", {"name":doc.get("mentor")}, "mentor")
    if frappe.session.user == frappe.get_all("Student", {'name':doc.student}, ['user'])[0]["user"]:
        # For mentor
        msg='''<p>{0} has sent you a message in mentor mentee communication channel.</p>'''.format(doc.get('student_name'))
        print("\n\nHello in mentor_mentee_communication_submit")
        send_mail(frappe.db.get_value("Employee",mentor,"user_id"),'Mentor Mentee Communication',msg)
        frappe.msgprint("Email was sent.")
    if frappe.session.user == frappe.get_all("Employee", {"name" : mentor}, ['user_id'])[0]['user_id']:
        # For student
        msg='''<p>{0} has sent you a message in mentor mentee communication channel.'''.format(doc.get('mentor_name'))
        send_mail(frappe.db.get_value("Student",doc.get('student'),"user"),'Mentor Mentee Cmmunication',msg)
        frappe.msgprint("Email was sent to {0}".format(doc.get('student_name'))+".")

def send_notification_to_team_members(doc):
    emails = frappe.get_all(
                "Maintenance Team Member",
                filters={"parent": doc.maintenance_team},
                fields=["team_member"],
            )
    email_list = [email["team_member"] for email in emails]
    tasks =frappe.db.sql("""Select maintenance_task,next_due_date from `tabAsset Maintenance Task` where parent=%s """,doc.name,as_dict=True)
    msg="""<p>You have been assigned with maintance of:</p><br>"""
    msg+="""<b>Item Code:</b>  {0}<br>""".format(doc.get('item_code'))
    msg+="""<b>Item Name:</b>  {0}<br>""".format(doc.get('item_name'))
    msg+="""<b>Asset Category:</b>  {0}<br>""".format(doc.get('asset_category'))
    msg+="""<b>Your Task is:</b>  {0} and next Due Date is {1}<br>""".format(tasks[0]['maintenance_task'],tasks[0]['next_due_date'])
    send_mail(email_list,'Asset Maintenance',msg)
    frappe.msgprint("Email sent to Maintenance Team")


### Student payment notification through email ###    
## Started by Rupali Bhatta 
def email_transaction_status(doc):
   
    msg="""<b>---------------------Transaction Details---------------------</b><br>"""
    msg+="""<b>Payment Entry No.:</b>  {0}<br>""".format(doc.get('name'))
    msg+="""<b>Date:</b>  {0}<br>""".format(doc.get('date_time_of_transaction'))
    msg+="""<p>---------------------Payment From / TO---------------------</p><br>"""
    msg+="""<b>Name:</b>  {0}<br>""".format(doc.get('party_name') or '-')
    msg+="""<b>Roll Number:</b>  {0}<br>""".format(doc.get('roll_no') or '-' )
    msg+="""<b>Total Outstanding Amount :</b>  {0}<br>""".format(doc.get('total_outstanding_amout') or '-' )
    msg+="""<b>Amount Paid:</b>  {0}<br>""".format(doc.get('paying_amount') or '-' )
    msg+="""<b>Transaction Id:</b>  {0}<br>""".format(doc.get('transaction_id') or '-' )
    msg+="""<b>Transaction Status:</b>  {0}<br>""".format(doc.get('transaction_status') or '-' )
    recipients = frappe.db.get_value("Student",doc.get('party'),"student_email_id")
    send_mail(recipients,'Transaction Details',msg)
    
## Ended by Rupali Bhatta     