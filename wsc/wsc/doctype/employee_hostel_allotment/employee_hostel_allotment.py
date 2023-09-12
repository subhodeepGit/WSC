# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeHostelAllotment(Document):
	# @frappe.whitelist()
	def validate(doc):
		Emp=doc.employees
		Emp_hostel_al=doc.hostel_masters
		hostel_val=frappe.db.sql("""select * from `tabHostel Masters` where name="%s" and (start_date<=now() and end_date>= now()); """%(Emp_hostel_al))
		if len(hostel_val)!=0:
			emp_info=frappe.db.sql("""select * from `tabEmployee Hostel Allotment` where employees="%s" and hostel_masters="%s" 
										and (start_date<=now() and end_date>= now());"""%(Emp,Emp_hostel_al))						
			if len(emp_info)==0 or emp_info[0][0]==doc.name:
				pass
			else:
				frappe.throw("Employee is already allotted doc no %s"%(emp_info[0][0]))	
				return
		else:
			frappe.throw("Hostel is closed. Please contact to the Admin.")										

	@frappe.whitelist()
	def get_emp_data(self):
		if self.employees:
			data=frappe.db.get_all("Employee",{"name":self.employees},["employee_name","user_id","designation"])
			return data[0]