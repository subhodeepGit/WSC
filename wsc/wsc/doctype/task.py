import frappe

def validate(self, doc):
        update_onboarding_status(self)
        # if self.actual_start_date and self.actual_end_date:
        #     if self.actual_start_date > self.actual_end_date:
        #         frappe.throw("Start Date cannot be greater than Actual date")

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