# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JobOfferCreationRequest(Document):
    def validate(self):
        # Check for duplicate records based on the 'candidate_name' field
        duplicate_records = self.check_duplicate_records()
        print(duplicate_records)

        if duplicate_records:
            frappe.throw("Duplicate records found for the same details. Please review.")

    def check_duplicate_records(self):
        # Fetch existing records excluding the current one
        existing_records = frappe.get_all('Job Offer Creation Request',filters={"job_opening":self.job_opening,"year":self.year,"designation":self.designation,"docstatus":1,"status":"Approved"},fields=['name'])

        return existing_records


@frappe.whitelist()
def fetch_applicants(job_opening,year):
    applicants = frappe.get_all("Job Applicant",filters={"job_title":job_opening,"current_status":"Selected","application_year":year},fields=["name","applicant_name","email_id",'current_status'])
    print(applicants)
    return applicants
