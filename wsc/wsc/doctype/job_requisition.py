import frappe
from frappe import _
from frappe.utils import getdate, today
from wsc.wsc.notification.custom_notification import job_requisition_director,job_requisition_coo,job_requisition_hr,job_requisition_ceo
from datetime import datetime, timedelta
from frappe.utils import getdate, today

def approver_mail(self):
	data={}
	data["name"]=self.name
	data["designation"]=self.designation
	data["department"]=self.department
	data["no_of_positions"]=self.no_of_positions
	data["workflow_state"]=self.workflow_state
	job_requisition_director(data)




def validate(self,method):
	if self.no_of_positions:
		if self.no_of_positions<0:
			frappe.throw("Enter valid value for No.of Positions")
	if self.expected_compensation:
		if self.expected_compensation<=0:
			frappe.throw("Enter valid value for Expected Compensation")
	if self.expected_by < self.posting_date:
		frappe.throw("Expected date cannot be earlier than the posting date.")
	
	if self.today_date is None:
		frappe.throw("Today's date is missing. Please provide a valid date.")

	if isinstance(self.today_date, str):
		try:
			today_date = datetime.strptime(self.today_date, "%Y-%m-%d")
		except ValueError as ve:
			frappe.throw(f"Error parsing Today's date: {ve}")
	else:
		today_date = self.today_date

	if self.posting_date is not None:
		if isinstance(self.posting_date, str):
			try:
				posting_date = datetime.strptime(self.posting_date, "%Y-%m-%d")
			except ValueError as ve:
				frappe.throw(f"Error parsing Posting Date: {ve}")
		else:
			posting_date = self.posting_date

		if today_date > posting_date:
			frappe.throw("Posting Date must be a future date or today's date.")

	if self.workflow_state=="Pending Approval from Director Admin":
		approver_mail(self)
	if self.workflow_state=="Pending Approval from COO":
		job_requisition_coo(self)
	if self.workflow_state=="Pending Approval From CEO":
		job_requisition_ceo(self)
	if self.workflow_state=="Approved by COO" or self.workflow_state=="Approved by CEO" or self.workflow_state=="Rejected by CEO" or self.workflow_state=="Rejected by COO" :
		job_requisition_hr(self)
	



	