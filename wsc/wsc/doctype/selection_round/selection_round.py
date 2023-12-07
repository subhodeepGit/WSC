# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SelectionRound(Document):
	print("\n\n\n")
	print("of")
	def validate(self):
		print("\n\n\n\n og")
	def on_submit(self):
		print("\n\n\n\n")
		print("on_submit")
		update_profile(self)

	def on_cancel(self):
		print('\n\n\n')
		print('on cance')
		print('\n\n\n')
		update_application(self)

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
def update_application(self):
	# get idx of the placement round based on the placement drive name and the round of placement 
	# subtract 1 from the idx and get the round name from the placement drive child table based on the placement drive name
	placement_round = self.round_of_placement
	placement_drive = self.placement_drive_name
	placement_round_idx = frappe.db.sql(""" SELECT idx FROM `tabRounds of Placement` WHERE parent = '%s' and round_name = '%s'"""%(placement_drive, placement_round))
	frappe.throw(placement_round_idx[0][0])
	pass



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
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class SelectionRound(Document):
	# def on_cancel(self):
	# 	frappe.set_value('Placement Drive Application', self.placement_drive_name, 'status', d.shortlisting_status)
		pass

@frappe.whitelist()
def update_profile(self):
	profile = frappe.get_doc('Student', self.student_no)
	profile.append('companies_applied_to',{
		'company_name' : self.company_name,
		'current_round' : self.round_of_placement,
		'status':'Passed'
	})
	profile.save()
	return 'echo'
