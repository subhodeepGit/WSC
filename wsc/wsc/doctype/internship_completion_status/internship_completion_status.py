# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _
from wsc.wsc.notification.custom_notification import internship_completion_status_mail

class InternshipCompletionstatus(Document):
	def validate(self):
		if(self.docstatus == 1):
			internship_completion_status_mail(self)

@frappe.whitelist()
def get_internship_name(internship_id):
	internship_name = frappe.db.sql(""" SELECT title_of_drive FROM `tabInternship Drive` WHERE name = '%s'"""%(internship_id))
	return internship_name[0][0]

# @frappe.whitelist()
# def participants(doctype, txt, searchfield, start, page_len, filters):
# 	searchfields = frappe.get_meta(doctype).get_search_fields()
# 	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

# 	internship_id=filters.get('internship_id')
# 	parent_id = frappe.db.sql("""SELECT name FROM `tabInternship Final List Declaration` WHERE select_internship = '%s'"""%(internship_id))[0][0]
# 	print('\n\n\n')
# 	print(searchfields)
# 	print('\n\n\n')
# 	participant_details = frappe.db.sql(""" SELECT participant_id FROM `tabInternship Selected Participants Table` where ({key} like %(txt)s or {scond}) and
# 									 parent = '{parent_id}'
# 				    """.format(
# 						**{
# 						"key": searchfield,
# 						"scond": searchfields,
# 						"parent_id":parent_id
# 					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
# 	return participant_details



@frappe.whitelist()
def participants(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	print(searchfields)
	searchfields = " or ".join("TP."+field+" like %(txt)s" for field in searchfields)
	print(searchfields)
	internship_id=filters.get('internship_id')
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
	return participant_details