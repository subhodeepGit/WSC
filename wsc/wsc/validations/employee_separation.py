
import frappe
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_separation_reporting_authority_mail,employee_separation_department_head_mail,employee_separation_director_mail,employee_separation_hr_mail,employee_separation_final_hr

def validate(self,method):
    if self.workflow_state=="Pending Approval from Reporting Authority":
        employee_separation_reporting_authority_mail(self)
    if self.workflow_state=="Pending Approval from Department Head":
        employee_separation_department_head_mail(self)
    if self.workflow_state=="Approved":
        employee_separation_hr_mail(self)
    if self.workflow_state=="Sent For Approval":
        employee_separation_director_mail(self)
    if self.boarding_begins_on and self.final_working_date:
        if self.boarding_begins_on>self.final_working_date:
            frappe.throw("Separation Begin date should not be after the Final Working Date")
    # if self.boarding_status=="Completed":
    #     update_employee_status(self.employee)
    # # if self.boarding_status == "Pending":
    #     update_employee_status(self.employee,"")
    #     # frappe.msgprint("Final Mail Sent to HR")

# def on_submit(doc,method):
#     frappe.msgprint(doc.mail_sent)
#     if doc.mail_sent==1:
#         frappe.msgprint("Final Mail is sent to HR Admin")

def after_insert(doc,method):
    print("\n\n\nUser Permission")
    set_user_permission(doc)
def set_user_permission(doc):
    if doc.reporting_authority:
        set_attendance_request_permission_reporting_authority(doc)
    
def on_trash(doc):
    delete_permission(doc)
def delete_permission(doc):
    for d in frappe.get_all("User Permission",{"reference_doctype":doc.doctype,"reference_docname":doc.name}):
        frappe.delete_doc("User Permission",d.name)
def set_attendance_request_permission_reporting_authority(doc):
    for emp in frappe.get_all("Employee", {'reporting_authority_email':doc.reporting_authority}, ['reporting_authority_email']):
        if emp.get('reporting_authority_email'):
            print(emp.get('reporting_authority_email'))
            add_user_permission("Employee Separation",doc.name, emp.get('reporting_authority_email'), doc)
        else:
            frappe.msgprint("Reporting Authority Not Found")
def on_cancel(doc,method):
    separation_name = doc.name
    if separation_name:
        frappe.db.set_value(doc.doctype,doc.name, "boarding_status", "Pending")
        frappe.db.set_value(doc.doctype,doc.name,"mail_sent","")
        frappe.db.commit()
####################################################################################

######################MISSION TO ADD DEPENDENCY TASK################################

def on_submit(self,method):
    tasks = frappe.get_all("Task", {"project": self.project},["name","subject"])
    # print("\n\n\n\nTasks")
    # print(tasks)
    activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": self.name}, fields=["name","activity_name","is_dependent","task_order","dependent_on_task"])
    # print("\n\n\n\n\nActivities")
    # print(activity_records)
    for task in tasks :
        for acitivity_record in activity_records:
            if acitivity_record.activity_name in task.subject:
                task_doc = frappe.get_doc("Task",{"subject":task.subject})
                task_doc.is_dependent = acitivity_record.is_dependent
                task_doc.task_order=acitivity_record.task_order   
                # if acitivity_record.is_dependent==1 :
                #     task_order = acitivity_record.task_order
                #     dependency = acitivity_record.dependent_on_task
                #     docs = frappe.get_doc("Task",{"subject":task.subject,"task_order":dependency},["name"])
                #     new_row = task_doc.append("depends_on")
                #     for item in docs:
                #         new_row.task = item.name

                task_doc.save()


def update_onboarding_status(self):
    
    onboarding_name = frappe.db.get_value("Employee Onboarding", {"project": self.project}, "name")
    if onboarding_name:
        activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": onboarding_name}, fields=["name","activity_name"])
        
        for activity_record in activity_records:
            # Step v: Update status field to the new status value
            if activity_record.activity_name in self.subject:
                # print(activity_record.activity_name)
                # print("\n\n\n")
                frappe.db.set_value("Employee Boarding Activity", activity_record.name, "status", self.status)

                
                # Step vi: Save changes to each On-boarding Activity document
                frappe.db.commit()
                # frappe.msgprint("Status updated in Employee Onboarding Activities")
            else :
                pass
        # print("\n\n\n\n")
        # print(onboarding_name.onboarding_status)
            
    else:
        return "No employee on-boarding record found for the provided project."




































#############################################################################################################
@frappe.whitelist()
def is_verified_user(docname):
    doc = frappe.get_doc("Employee Separation",docname)
    reporting_auth_id = doc.reporting_authority
    department_head=doc.department_head
    roles = frappe.get_roles(frappe.session.user)
    if "HR Manager/CS Officer" in roles or "HR Admin" in roles or "Director" in roles or "Admin" in roles or "Administrator" in roles or "Department Head" in roles:
        return True
    if doc.workflow_state=="Draft" and roles=="HR Admin":
        return True
    if doc.workflow_state == "Pending Approval from Reporting Authority" and frappe.session.user ==reporting_auth_id:
        return True
    if doc.workflow_state == "Pending Approval from Department Head" and frappe.session.user ==department_head:
        return True	
    if doc.workflow_state == "Sent For Approval" and roles=="Director":
        return True	    
    else :
        return False	

@frappe.whitelist()
def depart_head(department):
    dept = frappe.get_all('Department', {'name': department}, ['department_head'])
    if dept:
        department_head = dept[0].get('department_head')
        return department_head
    else:
        return None

@frappe.whitelist()
def mail_after_complete(docname):
    separation = frappe.get_doc("Employee Separation",docname)
    data = {}
    data["employee_separation"]=separation.name
    data["current_status"]=separation.boarding_status
    data["department"]=separation.department
    data["employee"]=separation.employee
    data["employee_name"]=separation.employee_name
    print(data)
    employee_separation_final_hr(data)

# @frappe.whitelist()
# def update_employee_status(employee):
#     employee_doc= frappe.get_doc('Employee', employee)
#     print(employee_doc)
#     employee_doc.status="Left"
#     employee_doc.save()

@frappe.whitelist()
def get_onboarding_details(parent,parenttype):
	return frappe.get_all(
		"Employee Boarding Activity",
		fields=[
			"activity_name",
			"role",
			"user",
			"required_for_employee_creation",
			"description",
			"task_weight",
			"begin_on",
			"duration",
            "department",
            "is_dependent",
            "task_order",
            "dependent_on_task"
		],
		filters={"parent": parent,"parenttype": parenttype},
		order_by="idx",
	)
