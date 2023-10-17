# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EntranceExamCentreSelection(Document):
	@frappe.whitelist()
	def selected_centers(self):
		print("\n\n\n",self)
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
			result.available_center = 1
			result.save()
			result.submit()

		frappe.msgprint("Centers Records Created")
		self.flag = 2
		self.save()
		print(self.flag)

	def validate(self):
		self.validate_duplicate_record()

	def on_cancel(self):
		# center_select = frappe.get_doc("Entrance exam select" , )
		self.flag = 0
		# self.cancel()
		print("\n\nhello" , self.flag)
		for i in self.current_centers:
			center_select_data = frappe.get_all("Entrance exam select" , {'center' : i.center , 'academic_year': self.academic_year , 'academic_term': self.academic_term , "docstatus": 1} , ['name'])
			if len(center_select_data) != 0:
				center_select = frappe.get_doc("Entrance exam select" , center_select_data[0]['name'])
				frappe.db.sql("""
					UPDATE `tabEntrance exam select` SET available_center = 0 WHERE academic_year = '{academic_year}' AND academic_term = '{academic_term}' AND center = '{center}'
				""".format(academic_year = self.academic_year , academic_term = self.academic_term , center = i.center))
				center_select.cancel()
		

	def validate_duplicate_record(self):
		if self.academic_year and self.academic_term:
			for a in frappe.get_all('Entrance Exam Centre Selection', {'academic_year':self.academic_year, 'academic_term':self.academic_term, 'docstatus':('!=', 2)}):
				if a.name and a.name != self.name:
					frappe.throw("The data is already exist in <b>{0}</b>".format(a.name))
		
