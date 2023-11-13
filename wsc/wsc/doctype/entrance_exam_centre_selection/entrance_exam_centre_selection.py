# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EntranceExamCentreSelection(Document):
	@frappe.whitelist()
	def selected_centers(self):
		duplicate_check_flag = 0
		for i in self.get('current_centers'):

			center_select_data = frappe.get_all("Entrance exam select", { "center": i.center ,
															   			'academic_year': self.academic_year ,
																		'academic_term':self.academic_term } , ['docstatus' , 'name'])	
			
			print("\n")
			print(center_select_data)
			for j in center_select_data:
				if j['docstatus'] == 0 or j['docstatus'] == 1:
					duplicate_check_flag = 1
					print("\n" , duplicate_check_flag)
					frappe.throw("Record is Already Published")
					
			else:
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

		if duplicate_check_flag == 0:
			frappe.msgprint("Centers Records Created")
			self.flag = 2
			self.save()
		# frappe.db.sql("""
		# 	UPDATE `tabEntrance Exam Centre Selection`
		# 	SET flag = 2
		# 	WHERE name = '{name}'
		# """.format(name = self.name))
		print("\n" , self.flag)
		print("\nFlag Update\n")
		

	def validate(self):
		self.validate_duplicate_record()

	def on_cancel(self):
		# center_select = frappe.get_doc("Entrance exam select" , )
		# self.flag = 0
		print("\n\n")
		print(self.name)
		# frappe.set_value("Entrance Exam Centre Selection",self.name,"flag",0)
		
		# self.cancel()
		for i in self.current_centers:
			center_select_data = frappe.get_all("Entrance exam select" , {'center' : i.center , 'academic_year': self.academic_year , 'academic_term': self.academic_term , "docstatus": 1} , ['name'])
			if len(center_select_data) != 0:
				center_select = frappe.get_doc("Entrance exam select" , center_select_data[0]['name'])
				frappe.db.sql("""
					UPDATE `tabEntrance exam select` SET available_center = 0 WHERE academic_year = '{academic_year}' AND academic_term = '{academic_term}' AND center = '{center}'
				""".format(academic_year = self.academic_year , academic_term = self.academic_term , center = i.center))
				center_select.cancel()
		
		frappe.db.sql("""
			UPDATE `tabEntrance Exam Centre Selection`
			SET flag = 0
			WHERE name = '{name}'
		""".format(name = self.name))
		print("\n" , self.flag)
		

	def validate_duplicate_record(self):
		if self.academic_year and self.academic_term:
			for a in frappe.get_all('Entrance Exam Centre Selection', {'academic_year':self.academic_year, 'academic_term':self.academic_term, 'docstatus':('!=', 2)}):
				if a.name and a.name != self.name:
					frappe.throw("The data is already exist in <b>{0}</b>".format(a.name))
		
