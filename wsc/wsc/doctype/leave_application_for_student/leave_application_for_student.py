# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from frappe import msgprint, _


class LeaveApplicationforStudent(Document):
	def on_submit(self):
		if self.workflow_state == "Approved":
			get_previous_attendance = frappe.get_all("Student Attendance",filters=[["student","=",self.student],["date","between", [self.from_date,self.to_date]],["status","=","Absent"],["docstatus","=",1]],fields=["name","status","date"])
			for t in get_previous_attendance:
				frappe.db.set_value("Student Attendance", t['name'], "status", "On Leave")
			hostel_leave(self)

	def validate(self):
		check_list=[]
		for t in self.get('class_wise_leave'):
			check_list.append(t.leave_applicability_check)
		all_zero_or_none = all(element == 0 or element is None for element in check_list)
		if all_zero_or_none:
			frappe.throw("You have not selected any class for leave application!!")

		if self.workflow_state == "Sent for Approval to Class Advisor" or "Sent for Approval to Course Manager":
			pass
		else:
			duplicate_application = frappe.db.sql("""SELECT `name`, `from_date`, `to_date` FROM `tabLeave Application for Student` WHERE `student` = '%s' AND ((from_date >= '%s' AND to_date <= '%s') OR (from_date <= '%s' AND to_date >= '%s'))"""%(self.student,self.from_date,self.to_date,self.to_date,self.from_date),as_dict=1)
			if duplicate_application:
				for t in duplicate_application:
					duplicate_from_date = t['from_date']
					duplicate_to_date = t['to_date']
					duplicate_application_no = t['name']
					frappe.throw(_("You have already applied for leave from <b>{0}</b> to <b>{1}</b> and your application number is <b>{2}</b>!!".format(duplicate_from_date.strftime("%d-%m-%Y"),duplicate_to_date.strftime("%d-%m-%Y"),duplicate_application_no)))

		if self.workflow_state == "Sent for Approval to Class Advisor":
			send_email_to_course_advisor(self)
		if self.workflow_state == "Sent for Approval to Course Manager":
			send_email_to_course_manager(self)



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
		send_mail(recipients,'Project and Task Report',msg)
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
		send_mail(recipients,'Project and Task Report',msg)
		frappe.msgprint("Email sent to Course Manager: %s"%(course_manager_name))


def send_mail(recipients,subject,message):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients,subject=subject,message = message)

def has_default_email_acc():
    for d in frappe.get_all("Email Account", {"default_outgoing":1}):
       return "true"
    return ""
	
def hostel_leave(self):
	if self.leave_applicability_hostel == "Academics and Hostel":
		ra_id=frappe.get_all("Room Allotment",filters={"student" : self.student, "docstatus": 1, "allotment_type" : "Allotted"},fields=["name","hostel_id","room_id","room_type"],limit=1)
		if ra_id != []:
			hostel_leave=frappe.new_doc("Student Leave Process")
			hostel_leave.allotment_number=ra_id[0]["name"]
			hostel_leave.student=self.student
			hostel_leave.student_name=self.student_name
			hostel_leave.roll_no=self.roll_no
			hostel_leave.registration_number=self.registration_no
			hostel_leave.start_date=self.from_date
			hostel_leave.end_date=self.to_date
			hostel_leave.hostel=ra_id[0]["hostel_id"]
			hostel_leave.room_number=ra_id[0]["room_id"]
			hostel_leave.room_type=ra_id[0]["room_type"]
			hostel_leave.comment=self.reason
			hostel_leave.save()
			hostel_leave.submit()


@frappe.whitelist()
def get_classes(from_date=None,to_date=None,curr=None,leave_criteria=None):
	course_schedule=[]
	if from_date != None and to_date != None and curr != None and leave_criteria == "Class-Wise Leave":
		curr1=json.loads(curr)
		semester=curr1[0]["semesters"]
		course_schedule=frappe.get_all("Course Schedule",filters=[["program","=",semester],['schedule_date',"between", [from_date,to_date]]],fields=['name','course_name','room_name','schedule_date','from_time','to_time'],group_by="name")
	elif from_date != None and to_date != None and curr != None and leave_criteria == "Full Day":
		curr1=json.loads(curr)
		semester=curr1[0]["semesters"]
		course_schedule=frappe.get_all("Course Schedule",filters=[["program","=",semester],['schedule_date',"between", [from_date,to_date]]],fields=['name','course_name','room_name','schedule_date','from_time','to_time'],group_by="name")
		for t in course_schedule:
			t['check'] = 1
	return course_schedule

@frappe.whitelist()
def current_education(student_no):
	current_education_data=frappe.get_all("Current Educational Details",{"parent":student_no},['programs','semesters','academic_year','academic_term'])
	return current_education_data