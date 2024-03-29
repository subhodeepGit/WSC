# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GrievanceCell(Document):

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
					if items["decision"]!= None:
						frappe.set_value("Students Grievance",self.students_grievance,"status",items["decision"])
						break
					else :
						frappe.set_value("Students Grievance",self.students_grievance,"status","Issue Received By Grievance Cell")
						break

	def on_update(self):
		self.set_value_in_students_grievance()
	# def validate(self):
	# 	data = frappe.get_all("Grievance Cell",{"students_grievance":self.students_grievance,"student":self.student})
	# 	if data:
	# 		frappe.throw("Your Response for this complain Already Exists...")
					


@frappe.whitelist()
def get_workflow_components(type_of_grievance):

	wf_data=frappe.get_all("Standard WorkFlow For Grievance",{"parent":type_of_grievance},
			["name","emp_no","emp_name","department","designation","email_id","idx"],order_by="idx")			
	return wf_data

