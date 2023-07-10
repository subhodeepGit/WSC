# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document

class EmployeeAdditionalCharges(Document):
	def on_submit(self):
		employees = []
		project_name = self.project_name
		start_date=self.from_date
		end_date=self.to_date
		description_of_work=self.description
		office_order=self.work_order
		assigned_by=self.assigned_by

		for employee in self.employee:
			employees.append(employee.employee)

		update_additional_charge(employees, project_name,start_date,end_date,description_of_work,office_order,assigned_by)

def update_additional_charge(employees, project_name,start_date,end_date,description_of_work,office_order,assigned_by):
	for employee in employees:
		employee_doc = frappe.get_doc("Employee", employee)
		print(employee_doc)
		employee_doc.append("additional_charge_details", {
			"project_name": project_name,
			"start_date": start_date,
			"end_date": end_date,
			"description_of_work":description_of_work,
			"office_order":office_order,
			"assigned_by":assigned_by,
		})

		employee_doc.save()







