# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _

class ParticipantAttendanceTool(Document):
	def validate(self):
		pass

	def on_submit(self):
		for d in self.get('participants'):
			new_doc = frappe.new_doc("ToT Participant Attendance")
			new_doc.participant_group = self.participant_group
			new_doc.select_course = self.select_course
			new_doc.select_module = self.select_module
			new_doc.academic_year = self.academic_year
			new_doc.academic_term = self.academic_term
			new_doc.instructor_id = self.instructor_id
			new_doc.instructor_name = self.instructor_name
			new_doc.participant_id = d.participant_id
			new_doc.participant_name = d.participant_name
			new_doc.class_schedule = self.select_class_schedule
			new_doc.date = self.dated
			new_doc.time = self.term
			
			if(d.present == 1):
				new_doc.status = "Present"
			else:
				new_doc.status = "Absent"
			new_doc.save()		
			
@frappe.whitelist()
def get_participant_group(based_on):
	data = frappe.db.sql(""" SELECT name FROM `tabParticipant Group`""")
	return data

@frappe.whitelist()
def get_details(participant_group_id):
	if(participant_group_id == ''):
		return ['','','','', '', '']
	else:
		# dates = frappe.db.sql(""" SELECT scheduled_date FROM `tabToT Class Schedule` WHERE participant_group_id = '%s'"""%(participant_group_id))
		group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
		instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
		# return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, dates]
		return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details]
	
@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	if(participant_group_id == '' or instructor_id == ''):
		return ['','','','']
	else:
		instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
		return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_participants(participant_group_id = None):
	if(participant_group_id == None):
		pass
	else:
		participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
		return participants

# --------------------------------------------------------------------------------
@frappe.whitelist()
def instructor(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

	participant_group_id=filters.get('participant_group_id')
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where ({key} like %(txt)s or {scond}) and
				    parent = '{participant_group_id}'
				    """.format(
						**{
						"key": searchfield,
						"scond": searchfields,
						"participant_group_id":participant_group_id
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return instructor_details

@frappe.whitelist()
def get_classes(participant_group=None):
	course_schedule=[]
	if participant_group != None:
		course_schedule=frappe.get_all("ToT Class Table",filters=[["parent","=",participant_group]],fields=['scheduled_date','room_name','room_number','from_time','to_time','duration','re_scheduled','is_scheduled','is_canceled','tot_class_schedule'])
	return course_schedule
