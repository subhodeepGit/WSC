# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import json
from frappe import _, scrub

class Assignment(Document):
	def validate(self):
		self.duplicate_assignment()
		self.assignment_creation_status="Pending"	

	def duplicate_assignment(self):
		data=frappe.get_all("Assignment",{"docstatus":1,
			       					'programs':self.programs,
									"participant_group":self.participant_group,
									"assignment_name":self.assignment_name,
									"programs":self.programs,
									"course":self.course,
									"course":self.course})
		if data:
			frappe.throw("Assignment Name already exist")

@frappe.whitelist()
def get_details(participant_group_id):
	if(participant_group_id == ''):
		return ['','','','','', '']
	else:
		group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
		instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
		assessment_criteria = frappe.db.sql(""" SELECT assessment_criteria FROM `tabCredit distribution List` where parent = '%s'"""%(group_details[0]['course']))
		return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, assessment_criteria]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	if(participant_group_id == '' or instructor_id == ''):
		return ''
	else:
		instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
		return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_criteria_details(course, assessment_criteria):
	if(course == '' or assessment_criteria == ''):
		return ['','','']
	else:
		criteria_details = frappe.get_all('Credit distribution List', 
										filters = [['parent', '=', course], ['assessment_criteria', '=', assessment_criteria]], 
										fields = ['total_marks','passing_marks','weightage'])
		return [criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage']]
	
@frappe.whitelist()
def get_criteria_details_amd(course, assessment_criteria,assignment_name):
	final_data=[]
	if course and assessment_criteria and assignment_name:
		amd_data=frappe.get_all("Assignment Marks Distribution",{"course":course,"assessment_criteria":assessment_criteria},['name'])
		total_marks=''
		passing_marks=''
		weightage=''
		for t in amd_data:
			amd_child_data=frappe.get_all("Assignment Marks Distribution Child",{"parent":t['name'],
																		"assignment_name":assignment_name},
																		['name',"total_marks","weightage","passing_marks"])
			for j in amd_child_data:
				total_marks=j["total_marks"]
				passing_marks=j["passing_marks"]
				weightage=j["weightage"]

		final_data=[total_marks, passing_marks,weightage]	
			
	return final_data
		


# ---------------------------------------------------------------------------------------------
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
def participant(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join("TP."+field + " like %(txt)s" for field in searchfields)
	participant_group_id=filters.get('participant_group_id')
	participant_details = frappe.db.sql(""" SELECT TP.name 
											FROM `tabParticipant Table` as PT
											JOIN `tabToT Participant` as TP on TP.name=PT.participant
											where (TP.{key} like %(txt)s or {scond}) and
													PT.parent = '{participant_group_id}'
											""".format(
												**{
												"key": searchfield,
												"scond": searchfields,
												"participant_group_id":participant_group_id
											}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return participant_details


@frappe.whitelist()
def criteria(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)
	course =filters.get('course')
	assignment_name=filters.get('assignment_name')
	final_list=[]
	assignment_marks_distribution_list=frappe.get_all("Assignment Marks Distribution",{"course":course},['name',"assessment_criteria"])
	for t in assignment_marks_distribution_list:
		name=t['name']
		amd_child=frappe.get_all("Assignment Marks Distribution Child",{"parent":name,"assignment_name":assignment_name})
		if amd_child:
			data=[t['assessment_criteria']]
			final_list.append(tuple(data))
	final_list=tuple(final_list)			
	criteria_details=final_list


	# criteria_details = frappe.db.sql(""" SELECT assessment_criteria FROM `tabCredit distribution List` where ({key} like %(txt)s or {scond}) and
	# 												parent = '{course}'
	# 										""".format(
	# 											**{
	# 											"key": searchfield,
	# 											"scond": searchfields,
	# 											"course": course
	# 										}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	# print(criteria_details)
	return criteria_details
# -----------------------------------------------------------------------------------------------------------------------------

@frappe.whitelist()
def create_assignment(frm):
	frappe.enqueue(assignment_enqueue, frm=frm, queue="long")
	doc= frappe.get_doc("Assignment",frm)
	doc.assignment_creation_status="Completed"
	doc.save() 
	assignment_enqueue(frm)

def assignment_enqueue(frm):
	doc= frappe.get_doc("Assignment",frm)
	participant_group=doc.participant_group
	participant_list=frappe.get_all("Participant Table",{"parent":participant_group,'active':1},['name','participant','participant_name','active'])
	# count = 0
	for t in participant_list:
		doc_data=frappe.new_doc("Assignment Upload")
		doc_data.participant_group=participant_group
		doc_data.start_date=doc.start_date 
		doc_data.end_date=doc.end_date
		doc_data.course=doc.course
		doc_data.programs=doc.programs
		doc_data.academic_year=doc.academic_year
		doc_data.academic_term=doc.academic_term
		doc_data.semester=doc.semester
		doc_data.participant_id=t.participant
		doc_data.assignment_id=doc.name
		doc_data.save()
	# 	count += 1
	
	# frappe.publish_progress(count * 100 / len(participant_list), title=_("Creating Dimensions..."))
	# frappe.clear_cache()



