# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _
from wsc.wsc.notification.custom_notification import internship_completion_status_mail

class InternshipCompletionstatus(Document):
	def validate(self):
		internship_completion_status_mail(self)

@frappe.whitelist()
def get_internship_name(internship_id):
	internship_name = frappe.db.sql(""" SELECT title_of_drive FROM `tabInternship Drive` WHERE name = '%s'"""%(internship_id))
	return internship_name[0][0]


@frappe.whitelist()
def get_participant_name(participant_type = None, participant_id = None):
	if(len(participant_id) > 0):
		if(participant_type == 'Student'):
			student_name = frappe.db.sql(""" SELECT student_name FROM `tabStudent` WHERE name ='%s'"""%(participant_id))
			return student_name[0][0]
		elif(participant_type == 'Employee'):
			employee_name = frappe.db.sql(""" SELECT employee_name FROM `tabEmployee` WHERE name ='%s'"""%(participant_id))
			return employee_name[0][0]

@frappe.whitelist()
def participants(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()

	searchfields = " or ".join("TP."+field+" like %(txt)s" for field in searchfields)
	internship_id=filters.get('internship_id')
	participant_type = filters.get('participant_type')
	if(participant_type == 'Student'):
		parent_id = frappe.db.sql("""SELECT name FROM `tabInternship Final List Declaration` WHERE select_internship = '%s'"""%(internship_id))[0][0]
		participant_details = frappe.db.sql(""" SELECT PT.participant_id 
												FROM `tabInternship Selected Participants Table` as PT
												JOIN `tabStudent` as TP on TP.name=PT.participant_id
												where (TP.{key} like %(txt)s or {scond}) and
														PT.parent = '{parent_id}'
												""".format(
													**{
													"key": searchfield,
													"scond": searchfields,
													"parent_id":parent_id
												}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
		if(participant_details):
			return participant_details
		else:
			return []
	elif(participant_type == 'Employee'):
		parent_id = frappe.db.sql("""SELECT name FROM `tabInternship Final List Declaration` WHERE select_internship = '%s'"""%(internship_id))[0][0]
		participant_details = frappe.db.sql(""" SELECT PT.participant_id 
												FROM `tabInternship Selected Participants Table` as PT
												JOIN `tabEmployee` as TP on TP.name=PT.participant_id
												where (TP.{key} like %(txt)s or {scond}) and
														PT.parent = '{parent_id}'
												""".format(
													**{
													"key": searchfield,
													"scond": searchfields,
													"parent_id":parent_id
												}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
		if(participant_details):
			return participant_details
		else:
			return []