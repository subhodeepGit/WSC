import frappe
# Adding Data in Previous Application Details Table
@frappe.whitelist()
def previous_applied(aadhar_number):
    job_applicant = frappe.get_all('Job Applicant',{'aadhar_card_number':aadhar_number},['name','applicant_name','aadhar_card_number','job_title'])
    print("\n\n\n")
    print(job_applicant)
    return job_applicant