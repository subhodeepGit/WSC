# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SelectionRound(Document):
	def on_submit(self):
		# pass
		update_profile(self)

# @frappe.whitelist()
# def update_profile(self):
# 	print(self.student_no)
# 	profile = frappe.get_doc('Student', self.student_no)
# 	profile.append('companies_applied_to',{
# 		'company_name' : self.company_name,
# 		'round_name' : self.round_of_placement,
# 		'round_status' : 'Scheduled'
# 	})
# 	profile.save()
# 	return 'abc'

# new function
@frappe.whitelist()
def update_profile(self):
	profile = frappe.get_doc('Student', self.student_no)
	companies = frappe.get_all('Applied Companies', {'parent': self.student_no},['drive_title'])
	if(len(companies) == 0):
		profile.append('companies_applied_to',{
			'company_name' : self.company_name,
			'drive_title' : self.drive_title,
			'round_name' : self.round_of_placement,
			'round_status' : self.shortlisting_status
		})
		profile.save()
	else:
		for d in companies:
			if(d.drive_title == self.drive_title):
				print('\n\n\n\n\n', 'drive title exists')
				data = frappe.db.sql(""" UPDATE `tabApplied Companies` SET round_name ='%s' 
										where parent='%s' AND drive_title = '%s' """%(self.round_of_placement,self.student_no, self.drive_title))
				# data = frappe.db.sql(""" UPDATE `tabApplied Companies` SET round_name ='%s' where parent='%s' AND drive_title = '%s' """%('apti-2',self.student_no, self.drive_title))
			else:
				profile.append('companies_applied_to',{
					'company_name' : self.company_name,
					'drive_title' : self.drive_title,
					'round_name' : self.round_of_placement,
					'round_status' : 'Scheduled'
				})
				profile.save()