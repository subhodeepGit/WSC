# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PlacementDriveCalendar(Document):
	pass
	# def validate(self):
	# 	self.some_func(self)

	# def some_func(self):
	# 	placement_drive = frappe.get_all('Placement Drive' , ['name'])

	# 	for i in placement_drive:
	# 		data = frappe.get_all('Rounds of Placement' , {'parent':i} , ['reporting_date' , 'round_name' , 'reporting_time' , 'location'])
	# 		print(data)


def get_rounds(placement_drive):
	# print(placement_drive)
	rounds = frappe.get_all("Rounds of Placement" , {'parent':placement_drive} , ['round_name' , 'date' ,  'reporting_time' , 'location'])
	print(rounds)