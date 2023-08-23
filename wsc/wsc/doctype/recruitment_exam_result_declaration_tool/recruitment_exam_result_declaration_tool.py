# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import send_mail_to_jobapplicants_rerd

class RecruitmentExamResultDeclarationTool(Document):
    def validate(doc):
        send_mail_to_jobapplicants_rerd(doc)
    @frappe.whitelist()
    def create_result(self):
        for d in self.get('applicant_details'):
            result = frappe.new_doc('Recruitment Exam Result Declaration')
            result.exam_declaration = self.exam_declaration
            result.job_selection_round = self.job_selection_round
            result.job_opening= self.job_opening
            result.job_applicant_id = d.job_applicant
            result.job_applicant_name = d.applicant_name
            result.job_applicant_email = d.applicant_mail_id
            result.result_status = d.result_status
            result.save()
            result.submit()
        
    @frappe.whitelist()
    def update_job_opening(self):
        job_opening = frappe.get_all("Recruitment Exam Declaration",{"name":self.exam_declaration},["job_opening"])
        if len(job_opening)==0:
            frappe.msgprint("No job Opening Found")
        else :
            job_opening= job_opening[0].job_opening
        selection_round_details = frappe.get_all("Recruitment Exam Declaration",{"name":self.exam_declaration},["selection_round"])
        if len(selection_round_details)==0:
            frappe.msgprint("No Selection Round Found")
        else :
            selection_round= selection_round_details[0]["selection_round"]
        job_opening_details = frappe.get_doc("Job Opening", job_opening)
        job_opening_details.job_opening = job_opening
        for round in job_opening_details.job_selection_round:
            if round.name_of_rounds==selection_round:
                round.result_declaration_status="Declared"
                
        job_opening_details.save()
            
        
@frappe.whitelist()
def fetch_applicants(recruitment_exam_declaration):
    applicants = frappe.get_all("Job Applicant Details",filters={"parent":recruitment_exam_declaration},fields=["job_applicant","applicant_name","applicant_mail_id"])
    print(applicants)
    return applicants 

@frappe.whitelist()
def update_job_opening(self):
    job_opening = frappe.get_all("Recruitment Exam Declaration",{"name":self.exam_declaration},["job_opening"])
    if len(job_opening)==0:
        frappe.msgprint("No job Opening Found")
    else :
        job_opening= job_opening[0].job_opening
    selection_round_details = frappe.get_all("Recruitment Exam Declaration",{"name":self.exam_declaration},["selection_round"])
    if len(selection_round_details)==0:
        frappe.msgprint("No Selection Round Found")
    else :
        selection_round= selection_round_details[0]["selection_round"]
    job_opening_details = frappe.get_doc("Job Opening", job_opening)
    job_opening_details.job_opening = job_opening
    for round in job_opening_details.job_selection_round:
        if round.name_of_rounds==selection_round:
            round.result_declaration_status="Declared"
            
    job_opening_details.save()

