import frappe

def validate(self, doc):
        update_onboarding_status(self)
        # if self.actual_start_date and self.actual_end_date:
        #     if self.actual_start_date > self.actual_end_date:
        #         frappe.throw("Start Date cannot be greater than Actual date")
        update_separation_status(self)

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

def update_separation_status(self):
    
    separation_name = frappe.db.get_value("Employee Separation", {"project": self.project}, "name")
    if separation_name:
        activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": separation_name}, fields=["name","activity_name"])
        
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
            frappe.throw("The Task is not Related to Separation or Onboarding")
    else:
        related_doctype = None
        frappe.throw("The Task is not Related to Separation or Onboarding")
    if doc.is_dependent == 1 :
        doc_name = frappe.db.get_value(related_doctype, {"project": doc.project}, "name")
        # print("Name",doc_name)
        # print("\n\n\n")
        if doc_name:
            activity_records = frappe.get_all("Employee Boarding Activity", filters={"parent": doc_name}, fields=["name","activity_name","task_order","dependent_on_task"]) 
            data = []
            # print("Activity Records",activity_records)
            # print("\n\n\n\n")
            for activity_record in activity_records:
                if activity_record.activity_name in doc.subject:
                    dependent_on = activity_record.dependent_on_task
                    # print(activity_record.dependent_on_task)
                    # print("\n\n")
                    # print(doc.task_order)
                    # print("\n\n")
                    task_doc = frappe.get_all("Task",{"project":doc.project,"task_order":dependent_on},["name"])
                    # print(task_doc)
                    # print("\n\n")
                    data.append(task_doc)
            print("\n\n\n\n\Data")
            print(data)
            return data

   