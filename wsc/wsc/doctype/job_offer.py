
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt, get_link_to_form
from frappe.utils import getdate, today
from wsc.wsc.notification.custom_notification import job_offer_reengagement


class JobOffer(Document):
	def onload(self):
		employee = frappe.db.get_value("Employee", {"job_applicant": self.job_applicant}, "name") or ""
		self.set_onload("employee", employee)

	def validate(self):
		self.validate_vacancies()
		job_offer = frappe.db.exists(
			"Job Offer", {"job_applicant": self.job_applicant, "docstatus": ["!=", 2]}
		)
		if self.offer_date:
			if (self.offer_date) < today():
				frappe.throw("Offer Date cannot be a past date.")
		# if job_offer and job_offer != self.name:
		# 	frappe.throw(
		# 		_("Job Offer: {0} is already for Job Applicant: {1}").format(
		# 			frappe.bold(job_offer), frappe.bold(self.job_applicant)
		# 		)
		# 	)
		self.offer_letter_content = """

    <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With reference to the above-mentioned subject and your participation in the WSC Recruitment process, I am immensely pleased to inform you that you have been selected for the position of {0} at World Skill Center as per the terms and conditions mentioned in the recruitment advertisement, i.e., Detailed Advertisement for _________________________________ Dated - _____________________ and the "WSC Open Market Contractual Appointment Rules".</p><br>

    <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Subsequent upon agreement to the above-mentioned rules and your confirmation of the same via e-mail dated __________________________, I am sending herewith this Offer Letter for the above-mentioned position.

    You are directed to join at World Skill Center within 30 days of the issue of this letter.</p><br> <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Your joining at World Skill Center will be subject to the submission of the pending documents (if any), which were not submitted during the document verification.</p><br>

    	<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	You are requested to send us an acknowledgment of this offer letter indicating your willingness to join along with your expected date of joining at World Skill Center. We look forward to a mutually rewarding professional relationship with you.</p><br>
    """.format(self.get('designation'))

    	
	





	def validate_vacancies(self):
		staffing_plan = get_staffing_plan_detail(self.designation, self.company, self.offer_date)
		check_vacancies = frappe.get_single("HR Settings").check_vacancies
		if staffing_plan and check_vacancies:
			job_offers = self.get_job_offer(staffing_plan.from_date, staffing_plan.to_date)
			if not staffing_plan.get("vacancies") or cint(staffing_plan.vacancies) - len(job_offers) <= 0:
				error_variable = "for " + frappe.bold(self.designation)
				if staffing_plan.get("parent"):
					error_variable = frappe.bold(get_link_to_form("Staffing Plan", staffing_plan.parent))

				frappe.throw(_("There are no vacancies under staffing plan {0}").format(error_variable))

	# def on_change(self):
	# 	update_job_applicant(self.status, self.job_applicant)

	def get_job_offer(self, from_date, to_date):
		"""Returns job offer created during a time period"""
		return frappe.get_all(
			"Job Offer",
			filters={
				"offer_date": ["between", (from_date, to_date)],
				"designation": self.designation,
				"company": self.company,
				"docstatus": 1,
			},
			fields=["name"],
		)
	def on_submit(doc):
		if doc.is_reengagement==1 and doc.status =="Awaiting Response":
			job_offer_reengagement(doc)

# def update_job_applicant(status, job_applicant):
# 	if status in ("Accepted", "Rejected"):
# 		frappe.set_value("Job Applicant", job_applicant, "status", status)


def get_staffing_plan_detail(designation, company, offer_date):
	detail = frappe.db.sql(
		"""
		SELECT DISTINCT spd.parent,
			sp.from_date as from_date,
			sp.to_date as to_date,
			sp.name,
			sum(spd.vacancies) as vacancies,
			spd.designation
		FROM `tabStaffing Plan Detail` spd, `tabStaffing Plan` sp
		WHERE
			sp.docstatus=1
			AND spd.designation=%s
			AND sp.company=%s
			AND spd.parent = sp.name
			AND %s between sp.from_date and sp.to_date
	""",
		(designation, company, offer_date),
		as_dict=1,
	)

	return frappe._dict(detail[0]) if (detail and detail[0].parent) else None


