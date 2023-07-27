# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ToTParticipantReporting(Document):
	pass

# data = frappe.get_all("Course Schedule",{'name':"EDU-CSH-2023-00004"})
# data = frappe.get_all('Rounds of Placement', filters = [['parent','=',drive_name],['round_name','=',round_name]],fields=['date','reporting_time'])

@frappe.whitelist()
def get_participant_details(participant_id):
	print('\n\n\n\n')
	print(participant_id)
	print('\n\n\n\n')
	# data = frappe.get_all("ToT Participant", {'participant_id': participant_id}, fields=['first_name'])
	data = frappe.get_all('ToT Participant', filters = {'name': participant_id}, fields=['first_name', 'middle_name', 'last_name', 'department', 'designation', 'name_of_the_institute'])
	print('\n\n\n\n')
	print(data)
	print('\n\n\n\n')
	name = data[0]['first_name'] + ' ' +  data[0]['middle_name'] +' ' +  data[0]['last_name']
	department =  data[0]['department']
	designation =  data[0]['designation']
	institute =  data[0]['name_of_the_institute']
	return [name, department, designation, institute]