# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta
from frappe import utils
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.notification.custom_notification import employee_reengagement_reporting_authority_mail,employee_reengagement_department_head_mail,employee_reengagement_director_mail,employee_reengagement_hr_mail


class EmployeeRenewalForm(Document):
    def validate(self):
        if self.new_contract_start_date and self.new_contract_end_date:
            self.date_validation()
            self.elegibilty()
            self.contract_validation()

            ####Notification Code#######
        if self.workflow_state=="Approved" or self.workflow_state=="Rejected":
            employee_reengagement_hr_mail(self)

        if self.workflow_state=="Reporting Authority Approval":
            employee_reengagement_reporting_authority_mail(self)
        if self.workflow_state=="Department Head Approval":
            employee_reengagement_department_head_mail(self)
        if self.workflow_state=="Approved":
            employee_reengagement_hr_mail(self)
        if self.workflow_state=="Director Admin Approval":
            employee_reengagement_director_mail(self)

            ######Notification Code########

    def after_insert(self):
        user_perimssion_report_manager(self)
        pass		

    def on_submit(self):
        if self.new_contract_start_date and self.new_contract_end_date:
            pass
        else:
            frappe.throw("Please Maintain <b> New Contract Start Date </b> and <b> New Contract Start Date </b> ")
        if  not self.revised_ctc or self.revised_ctc==0:
            frappe.throw("Revised CTC Can't be Zero")

        if self.new_contract_start_date and self.new_contract_end_date:
            self.contract_validation()


        self.emp_profile_update()

    def emp_profile_update(self):
        doc=frappe.get_doc("Employee",self.employee)
        doc.present_contract_start_date=self.new_contract_start_date
        doc.present_contract_end_date=self.new_contract_end_date
        doc.ctc=self.revised_ctc
        doc.append("internal_work_history",
                     {"branch":self.branch,
                      "department":self.department,
                    "designation":self.designation,
                    "from_date":self.new_contract_start_date,
                    "to_date":self.new_contract_end_date, 
                  })
        doc.save()
    
    def contract_validation(self):
        no_months=calculate_months_between_dates(self.new_contract_start_date,self.new_contract_end_date)
        if no_months>=12:
            pass
        else:
            frappe.throw("Contract Can't Be Less Then 12 Months")


    def elegibilty(self):
        if self.present_contract_start_date and self.present_contract_end_date:
            start_date=self.present_contract_end_date
            end_date=utils.today()
            no_months=calculate_months_between_dates(start_date,end_date)
        else:
            start_date=self.date_of_joining 
            end_date=utils.today()
            if not isinstance(start_date, str):
                start_date=str(start_date)
            no_months=calculate_months_between_dates(start_date,end_date)
        if no_months>=9:
            pass
        else:
            frappe.throw("Currently Not Entitled For Submission Of Form")

    def date_validation(self):
        if self.present_contract_start_date and self.present_contract_end_date:
            if isinstance(self.present_contract_end_date, str):
                present_contract_end_date=datetime.strptime(self.present_contract_end_date, '%Y-%m-%d').date()
            else:
                present_contract_end_date=self.present_contract_end_date
    
            if datetime.strptime(self.new_contract_start_date, '%Y-%m-%d').date()>present_contract_end_date \
                and datetime.strptime(self.new_contract_end_date, '%Y-%m-%d').date()>present_contract_end_date: 
                pass
            else:
                frappe.throw("<b> New Contract Start Date </b>should be greater then previous <b>  Present Contract End Date </b>")

        elif self.date_of_joining:
            if self.new_contract_start_date and self.new_contract_end_date:

                if isinstance(self.date_of_joining, str):
                    date_of_joining=datetime.strptime(self.date_of_joining, '%Y-%m-%d').date()
                else:
                    date_of_joining=self.date_of_joining

                if isinstance(self.new_contract_start_date,str):

                    if date_of_joining<datetime.strptime(self.new_contract_start_date, '%Y-%m-%d').date():
                        pass
                    else:
                        frappe.throw("<b> New Contract Start Date </b>should be greater then <b> Date of Joining </b>")
                else :
                    if date_of_joining<self.new_contract_start_date:
                        pass
                    else :
                        frappe.throw("<b> New Contract Start Date </b>should be greater then <b> Date of Joining </b>")
        else:
            frappe.throw("Please Maintain Joining Date In Employee")


def calculate_months_between_dates(start_date, end_date):
    if isinstance(start_date, str):
        pass
    else:
        start_date=str(start_date)
    if isinstance(end_date, str):
        pass
    else:
        end_date=str(end_date)	
    # Convert strings to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Calculate the difference between the dates using relativedelta
    delta = relativedelta(end_date, start_date)

    # Calculate the total number of months with calendar days
    total_months = delta.years * 12 + delta.months

    # Adjust for any remaining days within the last month
    if end_date.day >= start_date.day:
        total_months += 1

    return total_months		



def user_perimssion_report_manager(self):
    department_head=frappe.get_all("Department",{"name":self.department},['department_head'])
    if department_head:
        if not frappe.get_all("User Permission",{"reference_docType":"Employee Renewal Form","reference_docname":department_head[0]['department_head']}):
            add_user_permission("Employee Renewal Form",self.name, department_head[0]['department_head'], self)
    else:
        frappe.throw("Department Head not found")

@frappe.whitelist()
def get_appraisal_details(employee,date):
    appraisal_documents = frappe.get_all(
        "Employee Appraisal Portal",
        filters={
            "employee": employee,
            "docstatus": 1,
        },
        fields=["name","final_grade"],
        order_by="date DESC",  # Adjust the field name as per your actual field
        limit=1  # You may adjust the limit based on your requirements
    )
    print(appraisal_documents)
    for i in appraisal_documents:
        if i["name"]:
            doc_name = i["name"]
            final_grade = i["final_grade"]
            goal_documents = frappe.get_all("Key Work Goals",filters={"parent":doc_name},fields=["goal","category","due_date","employee_comment","status","uplaod_document","ros_comment"])
            print(goal_documents)
            return {"doc_name":doc_name,"final_grade":final_grade,"goal_documents":goal_documents}
            
