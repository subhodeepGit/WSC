# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import send_mail_to_jobapplicants_redn
from datetime import datetime, timedelta
from frappe.utils import getdate, today

class RecruitmentExamDeclaration(Document):
	def validate(doc):
		doc.exam_time_validation()
		exam_date = doc.get("exam_date") 
		current_date = today()

		if exam_date <= current_date:
			frappe.throw("Exam date cannot be a past date or the current date.")
		update_job_opening(doc)
		send_mail_to_jobapplicants_redn(doc)
	def exam_time_validation(doc):
		from_time1= datetime.strptime(doc.reporting__entry_time_at_centre_for_first_shift, '%H:%M:%S').time()
		to_time2= datetime.strptime(doc.gate_closing_timing_at_the_centre_first_shift, '%H:%M:%S').time()
		
		from_time3= datetime.strptime(doc.exam_time, '%H:%M:%S').time()
		to_time4= datetime.strptime(doc.exam_end_time_first_shift, '%H:%M:%S').time()
		
		from_time5= datetime.strptime(doc.reporting__entry_time_at_centre_for_second_shift, '%H:%M:%S').time()
		to_time6= datetime.strptime(doc.gate_closing_timing_at_the_centre_second_shift, '%H:%M:%S').time()
	
		from_time7= datetime.strptime(doc.exam_start_time_second_shift, '%H:%M:%S').time()
		to_time8= datetime.strptime(doc.exam_end_time_second_shift, '%H:%M:%S').time()


		if from_time1>=to_time2:
			frappe.throw("<b>Reporting/Entry Time at Centre For (First Shift)</b> cannot be after the <b>Gate Closing Timing at the Centre (First Shift)</b>")
		if to_time2>=from_time3:
			frappe.throw("<b>Gate Closing Timing at the Centre (First Shift)</b> cannot be after the <b>Exam Start Time (First Shift)</b>")
		if from_time5<=to_time4:
			frappe.throw("<b>Reporting/Entry Time at Centre For Second Shift</b> cannot be before the <b>Exam End Time (First Shift)</b>")
		if from_time3>=to_time4:
			frappe.throw("<b>Exam Start Time (First Shift)</b> cannot be after the <b>Exam End Time (First Shift)</b>")
		if from_time5>=to_time6:
			frappe.throw("<b>Reporting/Entry Time at Centre For Second Shift</b> cannot be after the <b>Gate Closing Timing at the Centre Second Shifts</b>")
		if from_time7>=to_time8:
			frappe.throw("<b>Exam Start Time (Second Shift)</b> cannot be after the <b>Exam End Time (Second Shift)</b>")
		if from_time7<=to_time6:
			frappe.throw("<b>Exam Start Time (Second Shift)</b> cannot be before the <b>Gate Closing Timing at the Centre Second Shifts</b>")

def update_job_opening(doc):
	print("Hello")
	job_opening = frappe.get_doc("Job Opening", doc.job_opening)
	job_opening.job_opening = doc.job_opening
	
	for round in job_opening.job_selection_round:
		if round.name_of_rounds == doc.selection_round:
			round.exam_declaration_status = 'Declared'

	job_opening.save()

# @frappe.whitelist()
# def get_selectionrounds(job_opening):
# 	selection_rounds = frappe.get_all('Job Selection Round' ,{'parent':job_opening}, ['name_of_rounds'],order_by='idx asc')
# 	print("\n\n\n")
# 	print(selection_rounds)
# 	return selection_rounds
@frappe.whitelist()
def get_selectionround(doctype, txt, searchfield, start, page_len, filters):
    fltr = {"parent":filters.get("job_opening")}
    # if txt:
    #     fltr.update({'semester': ['like', '%{}%'.format(txt)]})
    return frappe.get_all("Job Selection Round",fltr,['name_of_rounds'], as_list=1)
@frappe.whitelist()
def get_job_applicants(job_opening):
	job_applicants = frappe.db.get_all("Job Applicant",{"job_title":job_opening,},['name','applicant_name','email_id','current_status'])
	applicants = []
	for job_applicant in job_applicants:
		if job_applicant.current_status == 'CV Selected':
			applicants.append(job_applicant)
		elif job_applicant.current_status == 'Qualified':
			applicants.append(job_applicant)
	if not applicants:
		frappe.msgprint("No Applicant Found")    
	return applicants

  

