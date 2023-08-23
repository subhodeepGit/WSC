# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import send_mail_to_jobapplicants_redn

class RecruitmentExamDeclaration(Document):
    def validate(doc):
        update_job_opening(doc)
        send_mail_to_jobapplicants_redn(doc)
def update_job_opening(doc):
    print("Hello")
    job_opening = frappe.get_doc("Job Opening", doc.job_opening)
    job_opening.job_opening = doc.job_opening
    
    for round in job_opening.job_selection_round:
        if round.name_of_rounds == doc.selection_round:
            round.exam_declaration_status = 'Declared'

    job_opening.save()

@frappe.whitelist()
def get_selectionrounds(job_opening):
    selection_rounds = frappe.get_all('Job Selection Round' ,{'parent':job_opening}, ['name_of_rounds'],order_by='idx asc')
    print("\n\n\n")
    print(selection_rounds)
    return selection_rounds

@frappe.whitelist()
def get_job_applicants(job_opening):
    print("\n\n\nHELLO WORLD")
    job_applicants = frappe.db.get_all("Job Applicant",{"job_title":job_opening,},['name','applicant_name','email_id','current_status'])
    applicants = []
    for job_applicant in job_applicants:
        if job_applicant.current_status == 'CV Selected':
            applicants.append(job_applicant)
        elif job_applicant.current_status == 'Qualified':
            applicants.append(job_applicant)
    if not applicants:
        frappe.msgprint("No Applicant Found")    
    print("\n\n\n")
    print(applicants)
    return applicants

  

