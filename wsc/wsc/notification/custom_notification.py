from re import L
import frappe
from frappe.utils.data import format_date
from frappe.utils import get_url_to_form
from frappe.utils import cint, cstr, parse_addr

####### Notification for admit card###
def admit_card_submit(doc):
	print("\n\nadmit card notifications")
	print(doc.applicant_id)
	sub = """<p><b>Admit Card for Upcoming Entrance Exam</b></p><br>"""
	msg = """---------------------Admit Card---------------------"""
	msg+= """<b>Entrance Exam:</b>  {0}<br>""".format(doc.get('entrance_exam'))
	msg+= """<b>Applicant Id:</b>  {0}<br>""".format(doc.get('applicant_id'))
	msg+= """<b>Applicant Name:</b>  {0}<br>""".format(doc.get('applicant_name'))
	msg+="""<b>Department:</b>  {0}<br>""".format(doc.get('department'))
	msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year'))
	msg+="""<b>Academic Term:</b>  {0}<br>""".format(doc.get('academic_term'))
	msg+="""<b>Venue:</b>  {0}<br>""".format(doc.get('venue'))
	msg+="""<b>Address:</b>  {0}<br>""".format(doc.get('address'))
	msg+="""<b>District:</b>  {0}<br>""".format(doc.get('district'))
	msg+="""<b>PinCode:</b>  {0}<br>""".format(doc.get('pin_code'))
	msg+="""<b>Slot:</b>  {0}<br>""".format(doc.get('slot'))
	msg+="""<b>Date of Exam:</b>  {0}<br>""".format(doc.get('date_of_exam'))
	msg+="""<b>Exam Start Time:</b>  {0}<br>""".format(doc.get('exam_start_time'))
	msg+="""<b>Exam End Time:</b>  {0}<br>""".format(doc.get('exam_end_time'))
	attachments = [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, print_format='Entrance Exam Admit Card Print Format')]
	# send_mail(recipients,'Payment Successful',msg,attachments)
	send_mail(frappe.db.get_value("Student Applicant" , {"name":doc.applicant_id} , ["student_email_id"]), sub , msg , attachments)

############ Notification For Rank Card####
def rank_card_submit(doc):
	sub = """<p><b>Rank Card for Upcoming Entrance Exam</b></p><br>"""
	msg = """---------------------Admit Card---------------------"""
	msg+= """<b>Entrance Exam:</b>  {0}<br>""".format(doc.get('exam'))
	msg+= """<b>Applicant Id:</b>  {0}<br>""".format(doc.get('applicant_id'))
	msg+= """<b>Applicant Name:</b>  {0}<br>""".format(doc.get('applicant_name'))
	msg+="""<b>Department:</b>  {0}<br>""".format(doc.get('department'))
	msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year'))
	msg+="""<b>Academic Term:</b>  {0}<br>""".format(doc.get('academic_term'))
	msg+="""<b>Total Marks:</b>  {0}<br>""".format(doc.get('total_marks'))
	msg+="""<b>Earned Marks:</b>  {0}<br>""".format(doc.get('earned_marks'))
	msg += """</u></b></p><table class='table table-bordered'><tr>
		<th>Ranks</th>"""
	for  d in doc.get("student_ranks_list"):
		msg += """<tr><td>{0} - {1}</td></tr>""".format(d.get('rank_type') , d.get('rank_obtained'))
	msg += "</table>"
	attachments = [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, print_format='Entrance Exam Rank Card')]
	send_mail(frappe.db.get_value("Student Applicant" , {"name":doc.applicant_id} , ["student_email_id"]), sub , msg , attachments)

# def student_applicant_submit(doc):
#     sub="""<p><b>Application Form is Sucessfully Submitted</b></p><br>"""
#     msg="""<b>---------------------Applicant Details---------------------</b><br>"""
#     msg+="""<b>Student Name:</b>  {0}{1}<br>""".format(doc.get('first_name'), doc.get('last_name'))
#     msg+="""<b>Application Number:</b>  {0}<br>""".format(doc.get('name'))
#     msg+="""<b>Department:</b>  {0}<br>""".format(doc.get('department'))
#     msg+="""<b>Course Type:</b>  {0}<br>""".format(doc.get('program_grade'))
#     msg+="""<p>Course Preferences: </p>"""
#     msg += """</u></b></p><table class='table table-bordered'><tr>
#         <th>Courses</th>"""
#     for d in doc.get("program_priority"):
#         msg += """<tr><td>{0}</td></tr>""".format(str(d.get('programs'))) 
#     msg += "</table>"
#     send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg)
def student_applicant_submit(doc):

	sub = """<p><b>Application Form is Sucessfully Submitted</b></p><br>"""
	
	msg="""<p>Thank you for submitting your details. You have been provisionally allotted a seat in the trade <b> {0} </b> in World Skill Center. 
				Your final admission is subjected to the following:</p><br>""".format(doc.get('programs_'))
	msg+="""•     Verification of all the submitted documents<br>"""
	msg+="""•     Payment of fees for the 1st semester, i.e.- INR 10,000 only<br>"""
	msg+="""•     Any other condition, as prescribed<br>"""
	msg+="""The verification of all your submitted documents is pending. You will be intimated after the verification of all the submitted 
				documents for the payment of fees for the 1st semester, i.e.- INR 10,000 only.<br>"""
	msg+="""<p><b>WSC reserves the right to reject any application if any of the above conditions are not met and the decision is final.</b></p>"""
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
##################################################################################
def employee_grievance_member(doc):
	sub = "Reg:Employee Grievance Details</b></p><br>"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Grievance Details below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg = "<b>---------------------Employee Grievance Details---------------------</b><br>"

	msg += "<b>Employee Grievance ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Raised By:</b> {0}<br>".format(doc.get('raise_by'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Date:</b> {0}<br>".format(doc.get('date'))

	grievance_app_url = get_url_to_form('Employee Grievance', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(grievance_app_url)

	recipients = frappe.get_all("User", filters={'role': 'Grievance Cell Member'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]
	if len(recipient_emails)!=0 :


		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Email sent to Grievance Cell Members")
	else :
		frappe.throw("Grievance Cell Members has not assigned the role Grievance Cell Member !")

def employee_grievance_employee_mail(doc):
	sub = "Reg:Employee Grievance Status"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Grievance Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg = "<b>---------------------Employee Grievance Status Details---------------------</b><br>"

	msg += "<b>Employee Grievance ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Date:</b> {0}<br>".format(doc.get('date'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('status'))

	grievance_app_url = get_url_to_form('Employee Grievance', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(grievance_app_url)

	if doc.employee_email :

		send_mail(frappe.db.get_value("Employee Grievance",doc.get('name'),"employee_email"),sub,msg)
		frappe.msgprint("Status details is sent to the Employee")
	else :
		frappe.msgprint("User ID of Employee Not found")

def employee_grievance_hr_mail(doc):
	sub = "Reg:Employee Grievance Status"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Grievance Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg = "<b>---------------------Employee Grievance Status Details---------------------</b><br>"

	msg += "<b>Employee Grievance ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Date:</b> {0}<br>".format(doc.get('date'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('status'))

	grievance_app_url = get_url_to_form('Employee Grievance', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(grievance_app_url)

	recipients = frappe.get_all("User", filters={'role': 'HR Admin'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]
	print("\n\n\n\n")
	print(recipient_emails)
	if len(recipient_emails)!= 0:

		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Email sent to HR Admin")
	else :
		frappe.throw("HR Admin email id not found !")
########################################################################
def employee_separation_reporting_authority_mail(doc):
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

def employee_separation_final_hr(doc):
	sub = "Reg:Employee Separation Status Detail"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Separation Details Status below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Employee Separation Status---------------------</b><br>"

	msg += "<b>Employee Separation ID:</b> {0}<br>".format(doc["employee_separation"])
	msg += "<b>Employee ID:</b> {0}<br>".format(doc["employee"])
	msg += "<b>Employee Name:</b> {0}<br>".format(doc["employee_name"])
	msg += "<b>Department:</b> {0}<br>".format(doc["department"])
	# msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))
	msg += "<b>Status:</b> {0}<br>".format(doc["current_status"])

	separation_app_url = get_url_to_form('Employee Separation', doc["employee_separation"])
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(separation_app_url)

	recipients = frappe.get_all("User", filters={'role':'HR Admin'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	send_mail(recipient_emails, sub, msg)
	# frappe.msgprint("Employee Separation Details status is sent to the HR")

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
	msg+="""<b>Application Number:</b>  {0}<br>""".format(doc.get('student_application_id'))
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
	msg+="""<b>Application Number:</b>  {0}<br>""".format(doc.get('student_application_id'))
	send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg)
  

def program_enrollment_admitted(doc):
	sub="""Welcome to World Skill Center"""

	msg="""Dear {0},<br>""".format(doc.get('student_name'))
	msg+="""<p>We are pleased to inform you that you have been successfully allotted a seat in the course - <b>{0}</b> for the Academic Year <b>{1}</b> in World Skill Center, Bhubaneswar.</p><br>""".format(doc.get('programs'),doc.get('academic_year'))

	send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),sub,msg)

# def program_enrollment_provisional_admission(doc):
#     msg="""<p>You are Provisionaly Admitted in the Course <b>{0}</b></p><br>""".format(doc.get('programs'))
#     msg+="""<b>---------------------Student Details---------------------</b><br>"""
#     msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
#     msg+="""<b>Student Batch:</b>  {0}<br>""".format(doc.get('student_batch_name') or '-')
#     # msg+="""<b>Permanent Registration Number:</b>  {0}<br>""".format(doc.get('permanant_registration_number') or '-' )
#     msg+="""<b>Course:</b>  {0}<br>""".format(doc.get('programs'))
#     msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('program'))
#     msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
#     msg+="""<b>Academic Term:</b> {0}<br>""".format(doc.get('academic_term') or '-')

#     send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application status',msg)

def program_enrollment_provisional_admission(doc):
	msg="""<p>You are Provisionaly Admitted in the Course <b>{0}</b></p><br>""".format(doc.get('programs'))
	msg+="""We are pleased to inform you that the verification of all your submitted documents is completed and found to be in order. 
			You are hereby requested to make the payment of fees for the 1st semester, i.e.- INR 10,000 only by <b> 06 th  October 2023 </b> positively<br>"""
	msg+="""<b>WSC reserves the right to reject any application if the full payment of the for the 1 st  semester is not received and the decision is final.</b> """
	
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
	msg+="""<b>Course:</b>  {0}<br>""".format(doc.get('program') or '-')
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
		msg+="""<b>Course:</b>  {0}<br>""".format(doc.get('program') or '-')
		msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('semester') or '-')
		msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))

		send_mail(frappe.db.get_value("Student",st.get('student'),"student_email_id"),'Mentor Allocation',msg)


def exam_declaration_submit(doc):
	sub = "Exam has been declared for your program {0}".format(doc.exam_program)
	msg="""<p>--------Exam Details----------</p>"""
	msg+="""<p>Exam Declaration Id : {0}</p>""".format(doc.name)
	msg+="""<p>Exam Course : {0}</p>""".format(doc.exam_program)
	msg+="""<p>Application start date : {0}</p>""".format(doc.application_form_start_date)
	msg+="""<p>Application End Date : {0}</p>""".format(doc.application_form_end_date)
	msg+="""<p>Blocklist Date:{0}</p>""".format(doc.block_list_display_date)
	# msg+="""<p>Admit Card Issue Date : {0}</p>""".format(doc.admit_card_issue_date)
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
	msg+="""<p>Exam Course : {0}</p>""".format(ed_doc.exam_program)
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
	msg+="""<p>Exam Course : {0}</p>""".format(doc.exam_program)

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
	sub="""<p><b>Reg : Profile Updation Notification</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Profile Updation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Employee Details---------------------</b><br>"""
	msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc['employee_name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	emp_profile_updation = get_url_to_form('Employee Profile Updation', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(emp_profile_updation)

	send_mail([doc['reporting_authority_email']],sub,msg)

	frappe.msgprint("Email sent to reporting authority")
def employee_hr(doc):
	sub="""<p><b>Reg : Profile Updation Notification</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Profile Updation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Employee Details---------------------</b><br>"""
	msg+="""<b>Employee Name:</b>  {0}<br>""".format(doc['employee_name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	emp_profile_updation = get_url_to_form('Employee Profile Updation', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(emp_profile_updation)
	send_mail([doc['hr_email']],sub,msg)
	frappe.msgprint("Email sent to HR",[doc['hr_email']])

#######################Leave Policy #########################
def send_mail_to_director(doc):
	sub="""<p><b>Reg : Leave Policy Request</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Leave Policy Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Leave Policy Details---------------------</b><br>"""
	msg+="""<b>Leave polciy:</b>  {0}<br>""".format(doc['leave_policy'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	leave_policy_url = get_url_to_form('Leave Policy', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(leave_policy_url)
	send_mail([doc['director_mail']],sub,msg)
	frappe.msgprint("Email sent to Director",[doc['director_mail']])
def send_mail_to_hr(doc):
	sub="""<p><b>Reg : Leave Policy Request</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Leave Policy Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Leave Policy Details---------------------</b><br>"""
	msg+="""<b>Leave polciy:</b>  {0}<br>""".format(doc['leave_policy'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	leave_policy_url = get_url_to_form('Leave policy', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(leave_policy_url)
	send_mail([doc['hr_mail']],sub,msg)
	frappe.msgprint("Email sent to HR",[doc['hr_mail']])

#Notification for Employee onboarding :
def maildirector(doc):
	sub="""<p><b>Reg : Employee Onboarding Request</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Onboarding Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Employee Onboarding Details---------------------</b><br>"""
	msg+="""<b>Employee Onboarding:</b>  {0}<br>""".format(doc['employee_onboarding'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	emp_onboarding_url = get_url_to_form('Employee Onboarding', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(emp_onboarding_url)
	send_mail([doc['director_mail']],sub,msg)
	frappe.msgprint("Email sent to Director",[doc['director_mail']])
def mailhr(doc):
	sub="""<p><b> Reg :Employee Onboarding Request</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Onboarding Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Employee Onboarding Details---------------------</b><br>"""
	msg+="""<b>Employee Onboarding:</b>  {0}<br>""".format(doc['employee_onboarding'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	emp_onboarding_url = get_url_to_form('Employee Onboarding', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(emp_onboarding_url)
	send_mail([doc['hr_mail']],sub,msg)
	frappe.msgprint("Email sent to HR",[doc['hr_mail']])
def mailhr_aftercomplete(doc):
	sub="""<p><b>Reg : Employee Onboarding Request</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Onboarding Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Employee Onboarding Details---------------------</b><br>"""
	msg+="""<b>Onboarding Tasks Completed for the following Onboarding Process"""
	msg+="""<b>Employee Onboarding:</b>  {0}<br>""".format(doc['employee_onboarding'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	emp_onboarding_url = get_url_to_form('Employee Onboarding', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(emp_onboarding_url)
	send_mail([doc['hr_mail']],sub,msg)
	# print("Working")
	frappe.msgprint("Email sent to HR",[doc['hr_mail']])
###########################################################################

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
	sub="""<p><b>Reg : Employee Suggestion</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Suggestion Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Employee Suggestion Details---------------------</b><br>"""
	msg+="""<b>Employee Suggestion:</b>  {0}<br>""".format(doc['employee_suggestion'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	employee_suggestion_url = get_url_to_form('Employee Suggestion', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(employee_suggestion_url)
	send_mail([doc['hr_email']],sub,msg)
	frappe.msgprint("Email sent to HR",[doc['hr_email']])
def notify_director(doc):
	sub="""<p><b> Reg : Employee Suggestion</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Suggestion Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Employee Suggestion Details---------------------</b><br>"""
	msg+="""<b>Employee Suggestion:</b>  {0}<br>""".format(doc['employee_suggestion'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	employee_suggestion_url = get_url_to_form('Employee Suggestion', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(employee_suggestion_url)
	send_mail([doc['director_email']],sub,msg)
	frappe.msgprint("Email sent to Director",[doc['director_email']])
def notify_employee(doc):
	sub="""<p><b> Reg :Employee Suggestion</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Suggestion Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Employee Suggestion Details---------------------</b><br>"""
	msg+="""<b>Employee Suggestion:</b>  {0}<br>""".format(doc['employee_suggestion'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	employee_suggestion_url = get_url_to_form('Employee Suggestion', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(employee_suggestion_url)
	send_mail([doc['employee_email']],sub,msg)
	frappe.msgprint("Email sent to Employee",[doc['employee_email']])

def notify_committee(doc):
	sub = "Reg:Employee Suggestion </b></p><br>"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Suggestion Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg = "<b>---------------------Employee Suggestion Details---------------------</b><br>"

	msg+="""<b>Employee Suggestion:</b>  {0}<br>""".format(doc.get('name'))
	msg+="""<b>Status:</b>  {0}<br>""".format(doc.get('workflow_state'))
	employee_suggestion_url = get_url_to_form('Employee Suggestion', doc.get('name'))
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(employee_suggestion_url)

	recipients = frappe.get_all("User", filters={'role': 'Suggestion Committee Member'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]
	if len(recipient_emails)!=0 :


		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Email sent to Suggestion Committee")
	else :
		frappe.throw("No mail id found for the Committee Members !")

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
	msg="""<b>---------------------Empanelled Price Changed for Item {0}---------------------</b><br>""".format(doc.get('item_name'))
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
	receipients = [item['name'] for item in receipient]
	attachments = None
	send_mail(receipients,'Material Request',msg,attachments)

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
		frappe.sendmail(recipients=recipients or [], expose_recipients="header",subject=subject,message = message,attachments=attachments,with_container=False)        
		
def send_mail_cc(recipients=None,cc=None,subject=None,message=None,attachments=None):
	if has_default_email_acc(): 
		frappe.sendmail(recipients=recipients or [], cc=cc, expose_recipients="header",subject=subject,message = message,attachments=attachments,with_container=False)


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
	sub="""<p><b>Reg : Employee Resignation</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Resignation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Resignation Details---------------------</b><br>"""
	msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	resignation_url = get_url_to_form('Employee Resignation', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
	msg+="""<p><b>Initiate the Separation Process for the Employee if it is Approved</b></p><br>"""
	send_mail([doc['hr_mail']],sub,msg)
	frappe.msgprint("Confirmation mail sent to HR",[doc['hr_mail']])
def sendEmployee(doc):
	sub="""<p><b>Reg : Employee Resignation</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Resignation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Resignation Details---------------------</b><br>"""
	msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	resignation_url = get_url_to_form('Employee Resignation', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
	send_mail([doc['employee_mail']],sub,msg)
	frappe.msgprint("Confirmation mail sent to Employee",[doc['employee_mail']])
def sendRa(doc):
	sub="""<p><b>Reg : Employee Resignation</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Resignation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Resignation Details---------------------</b><br>"""
	msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	resignation_url = get_url_to_form('Employee Resignation', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
	send_mail([doc['ra_mail']],sub,msg)
	frappe.msgprint("Mail sent to Reporting Authority for Approval",[doc['ra_mail']])
def sendDh(doc):
	sub="""<p><b>EReg : mployee Resignation</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Resignation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Resignation Details---------------------</b><br>"""
	msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	resignation_url = get_url_to_form('Employee Resignation', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
	send_mail([doc['dh_mail']],sub,msg)
	frappe.msgprint("Mail sent to Department Head for Approval",[doc['dh_mail']])
def sendDirector(doc):
	sub="""<p><b>Reg : Employee Resignation</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Resignation Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Resignation Details---------------------</b><br>"""
	msg+="""<b>Resignation:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	resignation_url = get_url_to_form('Employee Resignation', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(resignation_url)
	send_mail([doc['director_mail']],sub,msg)
	frappe.msgprint("Mail sent to Director for Approval",[doc['director_mail']])


################################ Notification for Appraisal ######################################################################

def sendHR_appraisal(doc):
	sub="""<p><b>Reg : Employee Appraisal</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Appraisal Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Appraisal Details---------------------</b><br>"""
	msg+="""<b>Appraisal:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	msg+="""<b>Appraisal Cycle:</b>  {0}<br>""".format(doc['appraisal_cycle'])
	appraisal_url = get_url_to_form('Employee Appraisal Portal', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(appraisal_url)
	send_mail([doc['hr_mail']],sub,msg)
	frappe.msgprint("Confirmation mail sent to HR",[doc['hr_mail']])
def sendRa_appraisal(doc):
	sub="""<p><b>Reg :Employee Appraisal</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Appraisal Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Appraisal Details---------------------</b><br>"""
	msg+="""<b>Appraisal:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	msg+="""<b>Appraisal Cycle:</b>  {0}<br>""".format(doc['appraisal_cycle'])
	appraisal_url = get_url_to_form('Employee Appraisal Portal', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(appraisal_url)
	send_mail([doc['ra_mail']],sub,msg)
	frappe.msgprint("Mail sent to Reporting Authority for Approval",[doc['ra_mail']])

def sendDh_appraisal(doc):
	sub="""<p><b>Reg : Employee Appraisal</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Appraisal Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Appraisal Details---------------------</b><br>"""
	msg+="""<b>Appraisal:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	msg+="""<b>Appraisal Cycle:</b>  {0}<br>""".format(doc['appraisal_cycle'])
	appraisal_url = get_url_to_form('Employee Appraisal Portal', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(appraisal_url)
	send_mail([doc['dh_mail']],sub,msg)
	frappe.msgprint("Mail sent to Department Head for Approval",[doc['dh_mail']])
def sendDirector_appraisal(doc):
	sub="""<p><b>Reg : Employee Appraisal</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Appraisal Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Appraisal Details---------------------</b><br>"""
	msg+="""<b>Appraisal:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	msg+="""<b>Appraisal Cycle:</b>  {0}<br>""".format(doc['appraisal_cycle'])
	appraisal_url = get_url_to_form('Employee Appraisal Portal', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(appraisal_url)
	send_mail([doc['director_mail']],sub,msg)
	frappe.msgprint("Mail sent to Director for Approval",[doc['director_mail']])


##############################################################################################################################

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

###################################################Notification for Goal Setting ############################################################

def sendHR_goal(doc):
	sub="""<p><b>Reg : Employee Goal Setting</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Gaol Setting Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Goal Setting Details---------------------</b><br>"""
	msg+="""<b>Goal Setting:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	goal_url = get_url_to_form('Goal Setting', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(goal_url)
	msg+="""<p><b>Final Status of Goal Setting.</b></p><br>"""
	send_mail([doc['hr_mail']],sub,msg)
	frappe.msgprint("Confirmation mail sent to HR",[doc['hr_mail']])

def sendRa_goal(doc):
	sub="""<p><b>Reg :Employee Goal Setting</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Goal Setting Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Goal Setting Details---------------------</b><br>"""
	msg+="""<b>Goal Setting:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	goal_url = get_url_to_form('Goal Setting', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(goal_url)
	send_mail([doc['ra_mail']],sub,msg)
	frappe.msgprint("Mail sent to Reporting Authority for Approval",[doc['ra_mail']])

def sendDh_goal(doc):
	sub="""<p><b>Reg : Employee Goal Setting</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Goal Setting Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Goal Setting Details---------------------</b><br>"""
	msg+="""<b>Goal Setting:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	goal_url = get_url_to_form('Goal Setting', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(goal_url)
	send_mail([doc['dh_mail']],sub,msg)
	frappe.msgprint("Mail sent to Department Head for Approval",[doc['dh_mail']])

def sendDirector_goal(doc):
	sub="""<p><b>Reg : Employee Goal Setting</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Goal Setting Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Goal Setting Details---------------------</b><br>"""
	msg+="""<b>Goal Setting:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	goal_url = get_url_to_form('Goal Setting', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(goal_url)
	send_mail([doc['director_mail']],sub,msg)
	frappe.msgprint("Mail sent to Director for Approval",[doc['director_mail']])

def sendEmployee_goal(doc):
	sub="""<p><b>Reg : Employee Goal Setting</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Goal Setting Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Goal Setting Details---------------------</b><br>"""
	msg+="""<b>Goal Setting:</b>  {0}<br>""".format(doc.get('name'))
	msg+="""<b>Status:</b>  {0}<br>""".format(doc.get("status"))
	goal_url = get_url_to_form('Goal Setting', doc.get("name"))
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(goal_url)
	send_mail([doc.get("email")],sub,msg)
	frappe.msgprint("Mail sent to Employee",[doc.get("email")])

####################################Recruitment Exam Declaration Notification#####################################################################################
def send_mail_to_jobapplicants_redn(self):
	for t in self.get("applicant_details"):
		applicant_name=t.applicant_name
		applicant_email=t.applicant_mail_id

		msg="""<p>Dear Applicant, <br>"""
		msg+="""<p>This is to inform you that the for Job Opnening <b>{0}</b> exam for the round<b>{1}</b>  is declared. The examination will be held on <b>{2}</b> The admit card for the same will be shared soon.""".format(self.get('job_opening'),self.get('selection_round'),self.get('exam_date'))
		recipients = applicant_email
		send_mail(recipients,'WSC Job Opening Notification',msg)
		frappe.msgprint("Email sent to Job Applicants")

################################################################################################################################################################  
#####################################Recruitment Exam Result Declaration#################################################################################      
def send_mail_to_jobapplicants_rerd(self):
	for t in self.get("applicant_details"):
		applicant_name=t.applicant_name
		applicant_email=t.applicant_mail_id
		result_status=t.result_status
		if result_status == "Qualified":
			msg="""<p>Dear Applicant,<br>"""
			msg+="""<p>Congratualtions!!!<br>"""
			msg+="""<p>This is to inform you that the for Job Opnening <b>{0}</b> and exam round <b>{1}</b> ,you have been SELECTED.""".format(self.get('job_opening'),self.get('job_selection_round'))
			msg+="""<p>Further Process will be informed soon</p>"""
			recipients = applicant_email
			send_mail(recipients,'WSC Exam Result Notification',msg)
			frappe.msgprint("Email sent to Job Applicants")
		# if result_status == "Disqualified":
		#     msg="""<p>Dear Applicant,<br>"""
		#     msg+="""<p>Greetings!!!<br>"""
		#     msg+="""<p>This is to inform you that the for Job Opnening <b>{0}</b> and exam round <b>{1}</b> ,you have been not been selected.""".format(self.get('job_opening'),self.get('job_selection_round'))
		#     msg+="""<p>All the Best for your future.</p>"""
		#     recipients = applicant_email
		#     send_mail(recipients,'WSC Exam Result Notification',msg)
		#     frappe.msgprint("Email sent to Job Applicants")
###############################################Compensatory Leave Request Notification#############################################
def employee_comp_reporting_authority_email(doc):
	sub = "Reg:Compensatory Leave Request Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Compensatory Leave Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Employee Compensatory Leave Request Details---------------------</b><br>"

	msg += "<b>Employee Compensatory Leave Request ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Leave Type:</b> {0}<br>".format(doc.get('leave_type'))
	msg += "<b>Work From Date:</b> {0}<br>".format(doc.get('work_from_date'))
	msg += "<b>Work End Date:</b> {0}<br>".format(doc.get('work_end_date'))

	comp_app_url = get_url_to_form('Compensatory Leave Request', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(comp_app_url)

	send_mail(frappe.db.get_value("Compensatory Leave Request",doc.get('name'),"reporting_authority_email"),sub,msg)
	frappe.msgprint("Employee Compensatory Leave Request Details is sent to the Reporting Authority")

def employee_comp_leave_approver_email(doc):
	sub = "Reg:Compensatory Leave Request Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Compensatory Leave Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Employee Compensatory Leave Request Details---------------------</b><br>"

	msg += "<b>Employee Compensatory Leave Request ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Leave Type:</b> {0}<br>".format(doc.get('leave_type'))
	msg += "<b>Work From Date:</b> {0}<br>".format(doc.get('work_from_date'))
	msg += "<b>Work End Date:</b> {0}<br>".format(doc.get('work_end_date'))

	comp_app_url = get_url_to_form('Compensatory Leave Request', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(comp_app_url)

	send_mail(frappe.db.get_value("Compensatory Leave Request",doc.get('name'),"leave_approver"),sub,msg)
	frappe.msgprint("Employee Compensatory Leave Request Details is sent to the Leave Approver")

def employee_comp_hr_email(doc):

	sub = "Reg:Compensatory Leave Request Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Compensatory Leave Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Employee Compensatory Leave Request Details---------------------</b><br>"

	msg += "<b>Employee Compensatory Leave Request ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Leave Type:</b> {0}<br>".format(doc.get('leave_type'))
	msg += "<b>Work From Date:</b> {0}<br>".format(doc.get('work_from_date'))
	msg += "<b>Work End Date:</b> {0}<br>".format(doc.get('work_end_date'))

	comp_app_url = get_url_to_form('Compensatory Leave Request', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(comp_app_url)
	recipients = frappe.get_all("User", filters={'role': 'HR Admin'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]
	send_mail(recipient_emails,sub,msg)
	frappe.msgprint("Email sent to HR") 

def employee_comp_employee_email(doc):

	sub = "Reg:Compensatory Leave Request Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Compensatory Leave Request Details below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Employee Compensatory Leave Request Details---------------------</b><br>"

	msg += "<b>Employee Compensatory Leave Request ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Leave Type:</b> {0}<br>".format(doc.get('leave_type'))
	msg += "<b>Work From Date:</b> {0}<br>".format(doc.get('work_from_date'))
	msg += "<b>Work End Date:</b> {0}<br>".format(doc.get('work_end_date'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('status'))

	comp_app_url = get_url_to_form('Compensatory Leave Request', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(comp_app_url)
	send_mail(frappe.db.get_value("Compensatory Leave Request",doc.get('name'),"employee_email"),sub,msg)
	frappe.msgprint("Email sent to Employee") 
############################################################################################################################################

#Employee Re-engagement Notification

def employee_reengagement_reporting_authority_mail(doc):
	sub = "Reg:Employee Renewal Details"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Renewal Application Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Employee Renewal Application Details---------------------</b><br>"
	msg += "<b>Employee Renewal Form ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

	reengagement_app_url = get_url_to_form('Employee Renewal Form', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(reengagement_app_url)

	send_mail(frappe.db.get_value("Employee Renewal Form",doc.get('name'),"reporting_authority"),sub,msg)
	frappe.msgprint("Employee Renewal Application Details is sent to the Reporting Authority")

def employee_reengagement_department_head_mail(doc):
	sub = "Reg:Employee Renewal Details"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Renewal Application Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Employee Renewal Details---------------------</b><br>"
	msg += "<b>Employee Renewal Form ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

	reengagement_app_url = get_url_to_form('Employee Renewal Form', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(reengagement_app_url)

	send_mail(frappe.db.get_value("Employee Separation",doc.get('name'),"department_head"),sub,msg)
	frappe.msgprint("Employee Renewal Application Details is sent to the Department Head")    

def employee_reengagement_director_mail(doc):
	sub = "Reg:Employee Renewal Details"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Renewal Application Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Employee Renewal Details---------------------</b><br>"
	msg += "<b>Employee Renewal Form ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

	reengagement_app_url = get_url_to_form('Employee Renewal Form', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(reengagement_app_url)

	recipients = frappe.get_all("User", filters={'role': 'Director'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	if len(recipient_emails)==0 or recipient_emails==[" "]:
		frappe.throw("Director Email not found")
	else :

		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Employee Renewal Application Details is sent to Director.")

def employee_reengagement_hr_mail(doc):
	sub = "Reg:Employee Renewal Details"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Employee Renewal Application Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Employee Renewal Details---------------------</b><br>"
	msg += "<b>Employee Renewal Form ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Employee Name:</b> {0}<br>".format(doc.get('employee_name'))
	msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

	reengagement_app_url = get_url_to_form('Employee Renewal Form', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(reengagement_app_url)

	recipients = frappe.get_all("User", filters={'role':'HR Admin'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	if len(recipient_emails)==0 or recipient_emails==[" "]:
		frappe.throw("HR Admin Email not found")
	else :

		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Employee Renewal Application Details is sent to HR Admin.")

#####################################Recruitment Final Exam Result Declaration#################################################################################      
def send_mail_to_jobapplicants_final_notification(doc):
	if doc['current_status']=="Selected":
		msg = """<html>
			<body>
				<p>Dear Applicant,</p>
				<p>Congratulations!!!</p>
				<p>This is to inform you that for the job opening <b>{0}</b>, you have been SELECTED.</p>
				<p>Further process details will be provided soon.</p>
			</body>
		</html>""".format(doc['job_title'])

		send_mail([doc['email_id']], "Regarding WSC Recruitment Result Status", msg)
		frappe.msgprint("Email sent to Job Applicants")
	if doc['current_status']=="Rejected":
		msg = """<html>
			<body>
				<p>Dear Applicant,</p>
				<p>Warm Greetings!!!</p>
				<p>I hope this message finds you well. We appreciate the time and effort you put into your application for the Job Opening<b>{0}</b>.We regret to inform you that you have not been Selected for the further round.</p>
				<p>All the best for your future!!!</p>
			</body>
		</html>""".format(doc['job_title'])

		send_mail([doc['email_id']],"Reg:WSC Recruitment Result Status",msg)
		frappe.msgprint("Email sent to Job Applicants")
##########################################################################################################################################################################################
### Student payment notification through email ###    
## Started by Rupali Bhatta 

def email_transaction_status(doc): 
	course_details = frappe.get_value("Current Educational Details", {"parent":doc.get("party")},["programs","academic_term"])
	enrol_course= course_details[0]
	enrol_semester= course_details[1]
	msg = """<p>Dear Student,</p><br>"""
	msg+= """<p>We are pleased to inform you that the payment of the fees for the {0} of </p><br>""".format(enrol_semester) or '-' 
	msg+="""<b>INR </b>  {0}<br>""".format(doc.get('paying_amount') or '-' )   
	msg+= """<p>You have been successfully allotted a seat in the</p><br>"""
	
	msg += "<b>trade:</b> {0}<br>".format(enrol_course) or '-' 
	msg+= """<p>.in World Skill Center.</p><br>"""
	msg+= """<p>You will be intimated about the orientation and admission in World Skill Center in due time.</p><br>"""
	   
	recipients = frappe.db.get_value("Student",doc.get('party'),"student_email_id")
	send_mail(recipients,'Transaction Details',msg)
	
## Ended by Rupali Bhatta
##############################################################################################################################################################################################
####Job Requisition Notification#######
def job_requisition_director(doc):
	sub = "Reg:Job Requisition Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Requisition below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Job Requisition Details---------------------</b><br>"

	msg += "<b>Job Requisition ID:</b> {0}<br>".format(doc['name'])
	msg += "<b>Department:</b> {0}<br>".format(doc['department'])
	msg += "<b>Designation:</b> {0}<br>".format(doc['designation'])
	msg += "<b>Number of Positions:</b> {0}<br>".format(doc['no_of_positions'])
	msg += "<b>Status:</b> {0}<br>".format(doc['workflow_state'])

	jobrequisition_app_url = get_url_to_form('Job Requisition', doc['name'])
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jobrequisition_app_url)

	recipients = frappe.get_all("User", filters={'role': 'Director'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	send_mail(recipient_emails, sub, msg)
	frappe.msgprint("Job Requisition Details is sent to the Director")

def job_requisition_cfo(doc):
	sub = "Reg:Job Requisition Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Requisition below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Job Requisition Details---------------------</b><br>"

	msg += "<b>Job Requisition ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	msg += "<b>Number of Positions:</b> {0}<br>".format(doc.get('no_of_positions'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('workflow_state'))


	jobrequisition_app_url = get_url_to_form('Job Requisition', format(doc.get('name')))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jobrequisition_app_url)

	recipients = frappe.get_all("User", filters={'role': 'CFO'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	send_mail(recipient_emails, sub, msg)
	frappe.msgprint("Job Requisition Details is sent to the CFO")


def job_requisition_ceo(doc):
	sub = "Reg:Job Requisition Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Requisition below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Job Requisition Details---------------------</b><br>"

	msg += "<b>Job Requisition ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	msg += "<b>Number of Positions:</b> {0}<br>".format(doc.get('no_of_positions'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('workflow_state'))


	jobrequisition_app_url = get_url_to_form('Job Requisition', format(doc.get('name')))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jobrequisition_app_url)

	recipients = frappe.get_all("User", filters={'role': 'CEO'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	send_mail(recipient_emails, sub, msg)
	frappe.msgprint("Job Requisition Details is sent to the CEO")


def job_requisition_coo(doc):
	sub = "Reg:Job Requisition Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Requisition below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Job Requisition Details---------------------</b><br>"

	msg += "<b>Job Requisition ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	msg += "<b>Number of Positions:</b> {0}<br>".format(doc.get('no_of_positions'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('workflow_state'))


	jobrequisition_app_url = get_url_to_form('Job Requisition', format(doc.get('name')))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jobrequisition_app_url)

	recipients = frappe.get_all("User", filters={'role': 'COO'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	send_mail(recipient_emails, sub, msg)
	frappe.msgprint("Job Requisition Details is sent to the COO")

def job_requisition_hr(doc):
	sub = "Reg:Job Requisition Details"
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Requisition below and navigate to the form by clicking on "Open Now".</p></br>"""

	msg += "<b>---------------------Job Requisition Details---------------------</b><br>"

	msg += "<b>Job Requisition ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Department:</b> {0}<br>".format(doc.get('department'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	msg += "<b>Number of Positions:</b> {0}<br>".format(doc.get('no_of_positions'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('workflow_state'))


	jobrequisition_app_url = get_url_to_form('Job Requisition', format(doc.get('name')))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jobrequisition_app_url)

	recipients = frappe.get_all("User", filters={'role': 'HR Admin'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	send_mail(recipient_emails, sub, msg)
	frappe.msgprint("Job Requisition Details is sent to the HR")
###########################################################################################################################################################
############job applicant notification
def send_mail_to_jobapplicants_notification(doc):
	if doc['current_status']=="CV Selected":
		print("\n\n\nHello")
		msg = """<html>
			<body>
				<p>Dear Applicant,</p>
				<p>Congratulations!!!</p>
				<p>This is to inform you that for the job opening <b>{0}</b>, your CV have been SELECTED.</p>
				<p>Further process details will be provided soon.</p>
			</body>
		</html>""".format(doc['job_title'])

		send_mail([doc['email_id']], "Regarding WSC Recruitment Result Status", msg)
		frappe.msgprint("Email sent to Job Applicants")

########################################################### Job Offer Creation Request #################################################

def jocr_director_mail(doc):
	sub = "Reg:Job Offer Creation Request"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Offer Creatioin Request below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Job Offer Creation Request---------------------</b><br>"
	msg += "<b>Job Offer Creation Request ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Job Opening:</b> {0}<br>".format(doc.get('job_opening'))
	msg += "<b>Year:</b> {0}<br>".format(doc.get('year'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	msg+="""<b>Status:</b>  {0}<br>""".format(doc.get('status'))

	jocr_app_url = get_url_to_form('Job Offer Creation Request', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jocr_app_url)

	recipients = frappe.get_all("User", filters={'role': 'Director'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	if len(recipient_emails)==0 or recipient_emails==[" "]:
		frappe.throw("Director Email not found")
	else :

		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Job Offer Creation Request is sent to Director.")

def jocr_hr_mail(doc):
	sub = "Reg:Job Offer Creation Request"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Offer Creatioin Request below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Job Offer Creation Request---------------------</b><br>"
	msg += "<b>Job Offer Creation Request ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Job Opening:</b> {0}<br>".format(doc.get('job_opening'))
	msg += "<b>Year:</b> {0}<br>".format(doc.get('year'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	msg+="""<b>Status:</b>  {0}<br>""".format(doc.get('status'))

	jocr_app_url = get_url_to_form('Job Offer Creation Request', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jocr_app_url)

	recipients = frappe.get_all("User", filters={'role': 'Director'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]
	if len(recipient_emails)==0 or recipient_emails==[" "]:
		frappe.throw("HR Admin Email not found")
	else :

		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Job Offer Creation Request is sent to HR Admin.")

def jocr_coo_mail(doc):
	sub = "Reg:Job Offer Creation Request"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Offer Creatioin Request below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Job Offer Creation Request---------------------</b><br>"
	msg += "<b>Job Offer Creation Request ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Job Opening:</b> {0}<br>".format(doc.get('job_opening'))
	msg += "<b>Year:</b> {0}<br>".format(doc.get('year'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	msg+="""<b>Status:</b>  {0}<br>""".format(doc.get('status'))

	jocr_app_url = get_url_to_form('Job Offer Creation Request', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jocr_app_url)

	recipients = frappe.get_all("User", filters={'role': 'COO'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]
	if len(recipient_emails)==0 or recipient_emails==[" "]:
		frappe.throw("COO Email not found")
	else :

		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Job Offer Creation Request is sent to COO.")


def jocr_ceo_mail(doc):
	sub = "Reg:Job Offer Creation Request"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Job Offer Creatioin Request below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Job Offer Creation Request---------------------</b><br>"
	msg += "<b>Job Offer Creation Request ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Job Opening:</b> {0}<br>".format(doc.get('job_opening'))
	msg += "<b>Year:</b> {0}<br>".format(doc.get('year'))
	msg += "<b>Designation:</b> {0}<br>".format(doc.get('designation'))
	msg+="""<b>Status:</b>  {0}<br>""".format(doc.get('status'))

	jocr_app_url = get_url_to_form('Job Offer Creation Request', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(jocr_app_url)

	recipients = frappe.get_all("User", filters={'role': 'CEO'}, fields=['email'])
	recipient_emails = [recipient.get('email') for recipient in recipients]

	if len(recipient_emails)==0 or recipient_emails==[" "]:
		frappe.throw("CEO Email not found")
	else :

		send_mail(recipient_emails, sub, msg)
		frappe.msgprint("Job Offer Creation Request is sent to CEO.")

#---------------------------------------------------------------------------------------------------------------------------------------
#  for TnP

def participant_registration_mail(doc):
	sub = """Registration successful for{0}""".format(doc.get('event_name'))
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """Your registration for{0}""".format(doc.get('event_name'))
	msg += """with event ID: {0}""".format(doc.get('select_event'))
	msg += """has been successfully submitted"""
	msg += """Thank you"""
	get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(doc.participant_id))
	send_mail(get_mail[0][0], sub, msg)

def participant_attendance_mail(doc):
	sub = """Attendance record for{0}""".format(doc.get('event_name'))
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """Your attendance for{0}""".format(doc.get('event_name'))
	msg += """with event ID: {0}""".format(doc.get('select_event'))
	msg += """has been successfully recorded"""
	msg += """Thank you"""
	for d in doc.get('selected_participants_table'):
		get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(d.participant_id))
		send_mail(get_mail[0][0], sub, msg)

def event_feedback_mail(doc):
	sub = """Thank you for your feedback regarding {0}""".format(doc.get('event_name'))
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """Your feedback for{0}""".format(doc.get('event_name'))
	msg += """with event ID: {0}""".format(doc.get('select_event'))
	msg += """has been successfully submitted"""
	msg += """Thank you"""
	get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(doc.participant_id))
	send_mail(get_mail[0][0], sub, msg)

def internship_application_mail(doc):
	sub = """Registration successful for{0}""".format(doc.get('internship_drive_name'))
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """Your registration for{0}""".format(doc.get('internship_drive_name'))
	msg += """with internship ID: {0}""".format(doc.get('select_internship'))
	msg += """has been successfully submitted"""
	msg += """Thank you"""
	if(doc.participant_type == 'Student'):
		get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(doc.participant_id))
		send_mail(get_mail[0][0], sub, msg)
	elif(doc.participant_type == 'Employee'):
		get_mail = frappe.db.sql(""" SELECT company_email FROM `tabEmployee` WHERE name = '%s'"""%(doc.participant_id))
		send_mail(get_mail[0][0], sub, msg)

def internship_final_list_declaration_mail(doc):
	sub = """Attendance record for{0}""".format(doc.get('event_name'))
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """Your application has been selected for the {0}""".format(doc.get('internship_name'))
	msg += """with internship ID: {0}.""".format(doc.get('select_internship'))
	msg += """Kindly contact the Training and Placement department for further details."""
	msg += """Thank you"""
	for d in doc.get('selected_participants_list'):
		if(d.participant_type == 'Student'):
			get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(d.participant_id))
			send_mail(get_mail[0][0], sub, msg)
		elif(d.participant_type == 'Employee'):
			get_mail = frappe.db.sql(""" SELECT company_email FROM `tabEmployee` WHERE name = '%s'"""%(d.participant_id))
			send_mail(get_mail[0][0], sub, msg)

def internship_completion_status_mail(doc):
	sub = """Completed {0}""".format(doc.get('internship_name'))
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """Congratulations on your successful completion of the {0}""".format(doc.get('internship_name'))
	msg += """with internship ID: {0}""".format(doc.get('select_internship'))
	msg += """Thank you"""
	if(doc.participant_type == 'Student'):
		get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(doc.select_participant))
		send_mail(get_mail[0][0], sub, msg)
	elif(doc.participant_type == 'Employee'):
		get_mail = frappe.db.sql(""" SELECT company_email FROM `tabEmployee` WHERE name = '%s'"""%(d.participant_id))
		send_mail(get_mail[0][0], sub, msg)
	

def placement_drive_mail(doc):
	sub = """ Eligible for {0} Placement Drive""".format(doc.get('placement_company'))
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """This mail is to inform you that you are eligible for the <b>{0}</b>""".format(doc.get('title'))
	msg += """of<b>{0}>/b>.<br>""".format(doc.get('placement_company'))
	msg += """You can apply for the drive between {0}""".format(doc.get('application_Start_date'))
	msg += """and {0}""".format(doc.get('application_end_date'))
	msg += """Thank you."""
	for d in doc.get('eligible_student'):
		get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(d.student_doctype_name))
		send_mail(get_mail[0][0], sub, msg)

def placement_drive_application_mail(doc):
	sub = """Submission of placement drive application"""
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """Your application for {0} placement drive""".format(doc.get(''))
	msg += """with drive ID: {0}""".format(doc.get(''))
	msg += """has been successfully submitted"""
	msg += """Thank you"""
	get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(doc.student))
	send_mail(get_mail[0][0], sub, msg)

def placement_tool_mail(doc):
	placement_drive_title = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(doc.placement_drive_name))
	if(doc.round_status == ''):
		sub = """Result declaration for the {0} round""".format(doc.get('round_of_placement'))
		sub += """of {0}""".format(doc.get('placement_drie_title'))
		sub += """(drive id:{0})""".format(doc.get('placement_drie_name'))
	elif(doc.round_status == 'Round Result Declaration'):
		sub = """Result declaration for the {0} round""".format(doc.get(''))
		sub += """of {0}""".format(doc.get(''))
		sub += """(drive id:{0})""".format(doc.get(''))

	msg = """Dear Sir/Ma'am,<br>"""

	for d in doc.get('student_list'):
		if(d.shortlisting_status == 'Hired'):
			msg += """Congratulations you have been hired for the {0}""".format(placement_drive_title)
			msg += """with drive ID: {0}""".format(doc.get('placement_drive_name'))
		elif(d.shortlisting_status == 'Shortlisted'):
			msg += """Congratulations you have been shortlisted for the {0}""".format(doc.get('round_of_placement'))
			msg += """of {0}""".format(placement_drive_title)
			msg += """with drive ID: {0}""".format(doc.get('placement_drive_name'))
		elif(d.shortlisting_status == 'Rejected'):
			msg += """It is with great regret that we are informing you about your rejection from the {0} round""".format(doc.get('round_of_placement'))
			msg += """of the {0} """.format(placement_drive_title)
			msg += """with drive id: {0}""".format(doc.get('placement_drive_name'))
		msg += """Thank you."""
		get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(d.student_no))
		send_mail(get_mail[0][0], sub, msg)

		
	sub = """ Eligible for {0} Placement Drive""".format(doc.get('placement_company'))
	msg = """Dear Sir/Ma'am,<br>"""
	msg += """This mail is to inform you that you are eligible for the <b>{0}</b>""".format(doc.get('title'))
	msg += """of<b>{0}>/b>.<br>""".format(doc.get('placement_company'))
	msg += """You can apply for the drive between {0}""".format(doc.get('application_Start_date'))
	msg += """and {0}""".format(doc.get('application_end_date'))
	msg += """Thank you."""
	for d in doc.get('eligible_student'):
		get_mail = frappe.db.sql(""" SELECT student_email_id FROM `tabStudent` WHERE name = '%s'"""%(d.student_doctype_name))
		send_mail(get_mail[0][0], sub, msg)

# --------------------------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
@frappe.whitelist()
def job_offerapplicant(doc):
	import json
	doc = json.loads(doc)
	sub = "Reg:Job Offer"

	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Congratulations!! We are pleased to extend an offer of employment for the position of {0} at {1}. If you accept this offer, kindly sign and return a copy of this letter as a symbol of your acceptance. Kindly find your job offer in the attachment for the same.</p></br>""".format(doc.get('designation'), doc.get('company'))

	attachments = [frappe.attach_print(doc['doctype'], doc['name'], file_name=doc['name'], print_format='WSC Job Offer')]
	send_mail(frappe.db.get_value("Job Applicant", {"name": doc['job_applicant_id']}, ["email_id"]), sub, msg, attachments)
	frappe.msgprint("Email Sent to the Applicant")

def job_offer_reengagement(doc):
    sub = "Reg: Contract Renewal"

    msg = """<p>Dear Ma'am/Sir,</p><br>"""
    msg += """<p> I am writing to inform you that we are pleased to extend an offer for the renewal of your employment contract with {0} for the position of {1}. Your dedication and contributions to the team have been invaluable, and we are eager to continue our professional relationship with you.</p></br>""".format(doc.company, doc.designation)

    attachments = [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, print_format='WSC Re-engagement Job Offer')]

    employee_user_id = frappe.db.get_value("Employee", {"name": doc.employee}, ["user_id"])

    send_mail(employee_user_id, sub, msg, attachments)
    frappe.msgprint("Email Sent to the Employee")

##################################################################################################################################################################

###############################################		Infrastructre Notification Start	##########################################################################
def task_delay_reminder(doc):
	sub = "Reg:Task Delay"
	msg="""<b>Task {0} with Subject {1} has exceeded its expected end date</b><br>""".format(doc.get('name'), doc.get('subject'))
	msg += """Thank You<br>"""
	
	recipients_list = frappe.get_all("Task Assign", {'parent':doc.name},['assign_to'])
	recipient_emails = [recipient['assign_to'] for recipient in recipients_list]

	cc_dict = frappe.get_all("Task",{'name':doc.name},["project_manager"])
	cc_emails = [recipient['project_manager'] for recipient in cc_dict]

	send_mail_cc(recipient_emails,cc_emails,'Material Request',msg)
###############################################		Infrastructre Notification Ends	##########################################################################
	
################################Dynamic Workflow for Goal Setting ############################################
	
def notify_level(doc):
	sub = "Reg:Goal Setting"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Goal Setting Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Goal Setting Details---------------------</b><br>"
	msg += "<b>Goal Setting ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('status'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

	goal_app_url = get_url_to_form('Goal Setting', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(goal_app_url)

	send_mail([doc.get("email")],sub,msg)
	frappe.msgprint("Mail Sent to {}".format(doc.get("email")))  

def notify_employee_goal(doc):
	sub = "Reg:Goal Setting"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Goal Setting Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Goal Setting Details---------------------</b><br>"
	msg += "<b>Goal Setting ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('status'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

	goal_app_url = get_url_to_form('Goal Setting', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(goal_app_url)

	send_mail([doc.get("email")],sub,msg)
	frappe.msgprint("Mail Sent to {}".format(doc.get("email")))

################################## Dynamic Workflow Appraisal ###################################
	
def notify_level_app(doc):
	sub = "Reg:Appraisal"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Appraisal Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Appraisal Details---------------------</b><br>"
	msg += "<b>Appraisal ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('status'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

	app_url = get_url_to_form('Employee Appraisal Portal', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(app_url)

	send_mail([doc.get("email")],sub,msg)
	frappe.msgprint("Mail Sent to {}".format(doc.get("email")))  

def notify_employee_app(doc):
	sub = "Reg:Appraisal"
	
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Appraisal Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg += "<b>---------------------Appraisal Details---------------------</b><br>"
	msg += "<b>Appraisal ID:</b> {0}<br>".format(doc.get('name'))
	msg += "<b>Employee ID:</b> {0}<br>".format(doc.get('employee'))
	msg += "<b>Status:</b> {0}<br>".format(doc.get('status'))
	# msg += "<b>Final Working Date:</b> {0}<br>".format(doc.get('final_working_date'))

	app_url = get_url_to_form('Employee Appraisal Portal', doc.get('name'))
	msg += "<b>Open Now:</b> <a href='{0}'>Click here</a><br>".format(app_url)

	send_mail([doc.get("email")],sub,msg)
	frappe.msgprint("Mail Sent to {}".format(doc.get("email")))

def sendHR_app(doc):
	sub="""<p><b>Reg : Appraisal</b></p><br>"""
	msg = """<p>Dear Ma'am/Sir,</p><br>"""
	msg += """<p>Kindly refer to the Appraisal Details below and navigate to the form by clicking on "Open Now".</p></br>"""
	msg="""<b>---------------------Appraisal Details---------------------</b><br>"""
	msg+="""<b>Appraisal ID:</b>  {0}<br>""".format(doc['name'])
	msg+="""<b>Status:</b>  {0}<br>""".format(doc['current_status'])
	app_url = get_url_to_form('Employee Appraisal Portal', doc['name'])
	msg += """<b>Open Now:</b>  <a href="{0}">Click here</a><br>""".format(app_url)
	msg+="""<p><b>Final Status of Appraisal</b></p><br>"""
	send_mail([doc['hr_mail']],sub,msg)
	frappe.msgprint("Confirmation mail sent to HR",[doc['hr_mail']])

	#######################Notification code to job applicants on updation of Application Deadline ###############################

def send_mail_to_jobapplicants(doc):
	job_applicants = frappe.get_all("Job Applicant",{"job_title":"software-developer",'workflow_state':['in', ['Draft', 'Submitted']]},['name','applicant_name','email_id'])

	applicants = []
	for job_applicant in job_applicants:
		applicants.append(job_applicant)
	if not applicants:
		frappe.msgprint("No Applicant Found")    
	else :
		for t in applicants:
			applicant_name=t.applicant_name
			msg="""<p>Dear Applicant, <br>"""
			msg+="""<p>This is to inform you that the for Job Opnening <b>{0}</b> the deadline to submit the form has been updated. The Deadline to submit the form is  <b>{1}</b> """.format(doc.name,doc.application_deadline)
			recipients = t.email_id
			send_mail(recipients,'WSC Job Opening Notification',msg)
		frappe.msgprint("Email sent to Job Applicants")