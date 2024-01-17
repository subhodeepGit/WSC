import frappe
from datetime import datetime

def validate(self, doc):
        exp_date(self)
        act_date(self)
        update_onboarding_status(self)
        update_separation_status(self)

def after_insert(self):
    email = frappe.get_all('Task Assign' , {'name':self.name},['assign_to'])
    for recipient in email:
        user_perm = frappe.new_doc("User Permission")
        user_perm.user = recipient['assign_to']
        user_perm.allow = self.doctype
        user_perm.for_value = self.name
        user_perm.save()

def exp_date(self):
    if self.exp_start_date and self.exp_end_date:
        if self.exp_start_date>self.exp_end_date:
            frappe.throw("<b>Expected Start Date</b> cannot be greater than <b>Expected End date</b>")

def act_date(self):
    if self.act_start_date and self.act_end_date:
        if self.act_start_date>self.act_end_date:
            frappe.throw("<b>Actual Start Date</b> cannot be greater than <b>Actual End date</b>")


def update_onboarding_status(self):
    onboarding_name = frappe.db.get_value("Employee Onboarding", {"project": self.project}, "name")
    if onboarding_name:
        activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": onboarding_name}, fields=["name","activity_name"])
        
        for activity_record in activity_records:
            # Step v: Update status field to the new status value
            if activity_record.activity_name in self.subject:
                frappe.db.set_value("Employee Boarding Activity", activity_record.name, "status", self.status)

                
                # Step vi: Save changes to each On-boarding Activity document
                frappe.db.commit()
                # frappe.msgprint("Status updated in Employee Onboarding Activities")
            else :
                pass
            
    else:
        return "No employee on-boarding record found for the provided project."


def update_separation_status(self):   
    separation_name = frappe.db.get_value("Employee Separation", {"project": self.project}, "name")
    if separation_name:
        activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": separation_name}, fields=["name","activity_name"])
        
        for activity_record in activity_records:
            # Step v: Update status field to the new status value
            if activity_record.activity_name in self.subject:
                frappe.db.set_value("Employee Boarding Activity", activity_record.name, "status", self.status)

                
                # Step vi: Save changes to each On-boarding Activity document
                frappe.db.commit()
                # frappe.msgprint("Status updated in Employee Onboarding Activities")
            else :
                pass
            
    else:
        return "No employee on-boarding record found for the provided project."

@frappe.whitelist()
def dependency_task(docname):
    doc = frappe.get_doc("Task",docname)
    project = doc.project
    if project:
        if frappe.db.exists("Employee Separation", {"project": project}):
            related_doctype = "Employee Separation"
        elif frappe.db.exists("Employee Onboarding", {"project": project}):
            related_doctype = "Employee Onboarding"
        else:
            related_doctype = None  # Handle other cases if needed
            # frappe.throw("The Task is not Related to Separation or Onboarding")
            pass
    else:
        related_doctype = None
        # frappe.throw("The Task is not Related to Separation or Onboarding")
        pass
    if doc.is_dependent == 1 :
        doc_name = frappe.db.get_value(related_doctype, {"project": doc.project}, "name")
        if doc_name:
            activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": doc_name}, fields=["name","activity_name","task_order","dependent_on_task"]) 
            data = []

            for activity_record in activity_records:
                if activity_record.activity_name in doc.subject:
                    dependent_on = activity_record.dependent_on_task
                    task_doc = frappe.get_all("Task",{"project":doc.project,"task_order":dependent_on},["name"])
                    data.append(task_doc)
            return data

   