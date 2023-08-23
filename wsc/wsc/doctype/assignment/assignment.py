# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Assignment(Document):
	pass

@frappe.whitelist()
def get_details(participant_group_id):
	group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
	assessment_criteria = frappe.db.sql(""" SELECT assessment_criteria FROM `tabCredit distribution List` where parent = '%s'"""%(group_details[0]['course']))
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, assessment_criteria]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
	return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_criteria_details(course, assessment_criteria):
	criteria_details = frappe.get_all('Credit distribution List', filters = [['parent', '=', course], ['assessment_criteria', '=', assessment_criteria]], fields = ['total_marks','passing_marks','weightage'])
	return [criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage']]
