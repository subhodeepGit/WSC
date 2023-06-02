# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EntranceExamCentreSelection(Document):
	@frappe.whitelist()
	def selected_centers(self):
		print("\n\n\n")
		# print(self.get('current_centers'))
		for i in self.get('current_centers'):
			result = frappe.new_doc('Entrance exam select')
			result.academic_year = self.academic_year
			result.academic_term = self.academic_term
			result.center = i.center
			result.center_name = i.center_name
			result.address = i.address
			result.citytownvillage = i.citytownvillage
			result.district = i.district
			result.state = i.state
			result.pincode = i.pincode

			result.save()
			result.submit()

	def validate(self):
		self.validate_duplicate_record()

	def on_cancel(self):
		print("\n\n\n\n")
		print(self.academic_term)
		frappe.db.sql("""
			UPDATE `tabEntrance exam select` SET available_center = '1' WHERE academic_year = '{academic_year}' AND academic_term = '{academic_term}'
		""".format(academic_year = self.academic_year , academic_term = self.academic_term))
		print("cancel")

	def validate_duplicate_record(self):
		if self.academic_year and self.academic_term:
			for a in frappe.get_all('Entrance Exam Centre Selection', {'academic_year':self.academic_year, 'academic_term':self.academic_term, 'docstatus':('!=', 2)}):
				if a.name and a.name != self.name:
					frappe.throw("The data is already exist in <b>{0}</b>".format(a.name))
		

# @frappe.whitelist()
# def centers_cancel(academic_year , academic_term):
# 	print("\n\n\n\n")
# 	centers = frappe.get_all("Entrance exam select" , {'academic_year':academic_year , 'academic_term': academic_term} , ['available_center'])
# 	# res = frappe.get_doc('Entrance exam select')
# 	# print(res)
# 	for i in centers:
# 		i['available_center'] = 1
		
	
