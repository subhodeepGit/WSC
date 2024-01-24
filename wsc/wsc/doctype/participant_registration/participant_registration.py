# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantRegistration(Document):
	def validate(self):
		# super(ParticipantRegistration, self).validate()
		# self.validate_user_field()
		pass
	# def validate_user_field(self):
	# 	current_user = frappe.session.user
	# 	self.set_user_field_filter(current_user)
	# def set_user_field_filter(self, current_user):
	# 	user_field_name = "participant_id"
	# 	self.set_link_field_query(user_field_name, current_user)
	# def set_link_field_query(self, participant_id, current_user):
	# 	query = """
	# 		SELECT `tabUser`.`name`
	# 		FROM `tabUser`
	# 		WHERE `tabUser`.`name` = '{0}'
	# 	""".format(current_user)
	# 	self.set(participant_id, "options", query)

@frappe.whitelist()
def get_program_name(program_id = None):
	program_name = frappe.db.sql("""SELECT program_name FROM `tabTnP Program` WHERE name = '%s'"""%(program_id))
	if(len(program_name) > 0):
		return program_name[0][0]

@frappe.whitelist()
def get_event_details(event_id):
	event_details = frappe.db.sql(""" SELECT event_name, event_start_date, start_time FROM `tabTnP Event` WHERE name = '%s' """%(event_id))
	program_details = frappe.db.sql(""" SELECT in_a_program FROM `tabTnP Event` WHERE name = '%s'"""%(event_id))
	if(program_details[0][0] == 0):
		return [program_details[0][0], event_details[0][0], event_details[0][1], event_details[0][2]]
	elif(program_details[0][0] == 1):
		program_id = frappe.db.sql(""" SELECT select_program FROM `tabTnP Event` WHERE name ='%s'"""%(event_id))
		return [program_details[0][0], program_id[0][0], event_details[0][0], event_details[0][1], event_details[0][2]]

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
@frappe.validate_and_sanitize_search_inputs
def get_participant_id(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)
	data=[]
	user_roles = frappe.get_roles(frappe.session.user)
	user_email = (frappe.session.user)

	if("System Administrator" in user_roles):
		if(doctype=="Student"):
			data=frappe.db.sql("""select name,student_name from `tabStudent` where ({key} like %(txt)s or {scond}) 
	 					 and enabled={enabled}
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"enabled":filters.get("enabled"),
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
			return data
		elif(doctype=="Employee"):
			data=frappe.db.sql("""select name,employee_name from `tabEmployee` where ({key} like %(txt)s or {scond}) 
	 					 and status='{status}'
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"status":filters.get("status")
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
			return data
		pass
	elif("Training and Placement Administrator" in user_roles or "Training Events Coordinator" in user_roles):
		if(doctype=="Student"):
			data=frappe.db.sql("""select name,student_name from `tabStudent` where ({key} like %(txt)s or {scond}) 
	 					 and enabled={enabled}
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"enabled":filters.get("enabled"),
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
			return data
		elif(doctype=="Employee"):
			data=frappe.db.sql("""select name,employee_name from `tabEmployee` where ({key} like %(txt)s or {scond}) 
	 					 and status='{status}'
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"status":filters.get("status")
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
			return data
	elif("Employee" in user_roles and "Student" not in user_roles and "Training and Placement Administrator" not in user_roles):
		if(doctype=="Employee"):
			data=frappe.db.sql("""select name,employee_name from `tabEmployee` where ({key} like %(txt)s or {scond}) 
						and status='{status}' and prefered_email = '{prefered_email}'
						""".format(
				**{
					"key": searchfield,
					"scond": searchfields,
					"status":filters.get("status"),
					"prefered_email":user_email
				}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
			return data
		else:
			return []
	elif("Student" in user_roles and "Employee" not in user_roles and "Training and Placement Administrator" not in user_roles):
		if(doctype=="Student"):
			data=frappe.db.sql("""select name,student_name from `tabStudent` where ({key} like %(txt)s or {scond}) 
						and enabled={enabled} and student_email_id='{student_email_id}'
						""".format(
				**{
					"key": searchfield,
					"scond": searchfields,
					"enabled":filters.get("enabled"),
					"student_email_id":user_email
				}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
			return data
		else:
			return []


	if("Student" in user_roles and "Employee" not in user_roles and "Training and Placement Administrator" not in user_roles): # for students
		if(doctype=="Student"):
				data=frappe.db.sql("""select name,student_name from `tabStudent` where ({key} like %(txt)s or {scond}) 
	 					 and enabled={enabled} and student_email_id='{student_email_id}'
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"enabled":filters.get("enabled"),
						"student_email_id":user_email
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
				return data
		else:
			return []
	elif("Student" not in user_roles and "Employee" in user_roles and "Training and Placement Administrator" not in user_roles): #for employees
			if(doctype=="Employee"):
				data=frappe.db.sql("""select name,employee_name from `tabEmployee` where ({key} like %(txt)s or {scond}) 
	 					 and status='{status}' and prefered_email = '{prefered_email}'
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"status":filters.get("status"),
						"prefered_email":user_email
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
				return data
			else:
				return []
	elif("Student" not in user_roles and "Training and Placement Administrator" in user_roles): #for Training and Placement Administrator
		if(doctype=="Student"):
			data=frappe.db.sql("""select name,student_name from `tabStudent` where ({key} like %(txt)s or {scond}) 
	 					 and enabled={enabled}
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"enabled":filters.get("enabled"),
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
			return data
		elif(doctype=="Employee"):
			data=frappe.db.sql("""select name,employee_name from `tabEmployee` where ({key} like %(txt)s or {scond}) 
	 					 and status='{status}'
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"status":filters.get("status")
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
			return data
	else:
		return []