# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class FacultyWorkAssignment(Document):
	def validate(self):
		distribute_work_assignment(self)

def distribute_work_assignment(self):
	academic_year = self.academic_year
	faculty_details = frappe.get_all("Assign Faculty", {"parent" : self.name}, ["faculty", "faculty_name", "department"])
	task = self.task
	date = self.date
	start_date = datetime.strptime(self.from_date, "%Y-%m-%d")
	end_date = datetime.strptime(self.to_date, "%Y-%m-%d")
	duration = ((end_date - start_date).total_seconds() / 3600) + 24
	if faculty_details:
		for i in range(len(faculty_details)):
			instructor = frappe.get_all("Instructor", {"name" : faculty_details[i].faculty}, "name")
			if instructor:
				parent = frappe.get_doc("Instructor", instructor[0].name)
				new_row = parent.append("other_activities", {})
				new_row.academic_year = academic_year
				new_row.department = faculty_details[i].department
				new_row.activities = task
				new_row.date = date
				new_row.duration = duration
				new_row.instructor_name = faculty_details[i].faculty_name
				parent.save()