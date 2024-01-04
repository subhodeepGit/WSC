# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GrievanceCell(Document):
	def validate(self):
		# validate_date(self)
		# mobile_number_validation(self)
		self.validate_file_date()
		for t in self.get("grievance_status"):
			if t.decision:
				self.status=t.decision


	def on_update(self):
		self.set_value_in_students_grievance()
	# def validate(self):
	# 	data = frappe.get_all("Grievance Cell",{"students_grievance":self.students_grievance,"student":self.student})
	# 	if data:
	# 		frappe.throw("Your Response for this complain Already Exists...")
					

	def set_value_in_students_grievance(self):
		data = frappe.get_all("Grievance status",{"parent":self.name},["emp_no","emp_name","date_of_posting","remarks","decision","file_status"])
		if len(data)==0 :
			pass
		else :
			for items in data:
				if items["file_status"]=="Closed":
					resolution_details = items["remarks"]
					resolution_date = items["date_of_posting"]
					file_status=items["file_status"]
					status = items["decision"]
					frappe.set_value("Students Grievance",self.students_grievance,"resolution_date",resolution_date)
					frappe.set_value("Students Grievance",self.students_grievance,"resolution_detail",resolution_details)
					frappe.set_value("Students Grievance",self.students_grievance,"status",status)

					break
				else :
					if items["decision"]!='':
						frappe.set_value("Students Grievance",self.students_grievance,"status",items["decision"])
						frappe.set_value("Students Grievance",self.students_grievance,"resolution_detail",items["remarks"])
						frappe.set_value("Students Grievance",self.students_grievance,"resolution_date",items["date_of_posting"])
						break
					else :
						frappe.set_value("Students Grievance",self.students_grievance,"status","Issue Received By Grievance Cell")
						frappe.set_value("Students Grievance",self.students_grievance,"resolution_detail",items["remarks"])
						frappe.set_value("Students Grievance",self.students_grievance,"resolution_date",items["date_of_posting"])
						break
	def validate_file_date(self):
		today=frappe.utils.today()
		for t in self.get("grievance_status"):
			if t.date_of_posting:
				if t.date_of_posting>today:
					frappe.throw("Posting Date can't be in Future")			    

# def validate_date(self):
# 	if self.date_of_incident and  self.posting_date and self.date_of_incident > self.posting_date:
# 		frappe.throw("Date of Incident <b>'{0}'</b> Must Be a valid Date <b>'{1}'</b>".format(self.date_of_incident, self.posting_date))
					

def mobile_number_validation(self):
    if self.emergency_phone_no:
        if not (self.emergency_phone_no).isdigit():
            frappe.throw("Field <b>Emergency Phone Number</b> Accept Digits Only")
        if len(self.emergency_phone_no)>10:
            frappe.throw("Field <b>Emergency Phone Number</b> must be 10 Digits")
        if len(self.emergency_phone_no)<10:
            frappe.throw("Field <b>Emergency Phone Number</b> must be 10 Digits")

@frappe.whitelist()
def get_workflow_components(type_of_grievance):

	wf_data=frappe.get_all("Standard WorkFlow For Grievance",{"parent":type_of_grievance},
			["name","emp_no","emp_name","department","designation","email_id","idx"],order_by="idx")			
	return wf_data

