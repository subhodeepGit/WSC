# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class GenerateCertificate(Document):
	pass
# ----------------------------------------------------------------------------------------------------------------------
@frappe.whitelist()
def get_program_id(event_id):
	program_id = frappe.db.sql(""" SELECT in_a_program, select_program FROM `tabTnP Event` where name = '%s'"""%(event_id))
	if(program_id[0][0] == 0):
		return [0]
	else:
		return [program_id[0][0], program_id[0][1]]
	

@frappe.whitelist()
def get_participants(event_id):
	participant_id = frappe.db.sql(""" SELECT participant_id FROM `tabParticipant Registration` WHERE select_event = '%s'"""%(event_id))
	return participant_id

@frappe.whitelist()
def get_participant_name(event_id, participant_id):
	participant_details = frappe.db.sql(""" SELECT participant_name, participant_type FROM `tabParticipant Registration` WHERE select_event = '%s' AND participant_id = '%s'"""%(event_id, participant_id))
	return [participant_details[0][0], participant_details[0][1]]