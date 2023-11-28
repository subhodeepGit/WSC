# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import comma_and, get_link_to_form,get_link_to_form, getdate, formatdate
from frappe import msgprint, _

class AssignmentDeclaration(Document):
	def validate(self):
		self.validate_duplication()
		self.is_assignment_created()
		self.is_assignment_completed()

	def is_assignment_created(self):
		for t in self.get('job_sheet'):
			if not t.job_sheet_number:
				frappe.throw("No Assignment has been created for %s"%(t.job_sheet_name))

	def is_assignment_completed(self):
		for t in self.get('job_sheet'):
			output=frappe.db.count("Assignment Upload",filters=[['assignment_id',"=",t.job_sheet_number],['docstatus',"In",(0,1)]])
			if output == 0:
				frappe.throw("Assignment(s) not created in Assignment Upload screen")

	def validate_duplication(self):
		"""Check if the Assignment Declaration Record is Unique"""
		assignment_record = None
		
		assignment_record = frappe.db.exists('Assignment Declaration', {
			'select_assessment_criteria': self.select_assessment_criteria,
			'module': self.module,
			'course': self.course,
			'academic_year': self.academic_year,
			'docstatus': ('!=', 2),
			'name': ('!=', self.name),
			"participant_group":self.participant_group
		})

		if assignment_record:
			record = get_link_to_form('Assignment Declaration', assignment_record)
			frappe.throw(_('Assignment Declaration record {0} already exists!')
				.format(record), title=_('Duplicate Entry'))


@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	if(participant_group_id == '' or instructor_id == ''):
		return ['','','','','', '', '']
	else:
		instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
		return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_criteria_details(course, assessment_criteria):
	if(course == '' or assessment_criteria == ''):
		return ['','','','','', '', '']
	else:
		criteria_details = frappe.get_all('Credit distribution List', filters = [['parent', '=', course], ['assessment_criteria', '=', assessment_criteria]], fields = ['total_marks','passing_marks','weightage'])
		if criteria_details:
			return [criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage']]
		else:
			frappe.throw("<b>Passing Marks and Weightage not defined in Component Distribution table of Module</b>")


@frappe.whitelist()
def get_participants(participant_group_id = None, attendance_applicable = 0, attendance_percentage = 0):
	if(participant_group_id == None):
		pass
	else:
		participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
		for d in participants:
			participant_classes = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Class Table` WHERE parent = '%s'"""%(participant_group_id))
			participant_present_for = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Participant Attendance` WHERE participant_id = '%s' AND participant_group = '%s' AND docstatus = 1 AND status = 'Present'"""%(d.participant, participant_group_id))
			try:
				final_attendance = (participant_present_for[0][0]/participant_classes[0][0])*100
			except ZeroDivisionError:
				final_attendance = 0
			# final_attendance = (participant_present_for[0][0]/participant_classes[0][0])*100
			d['attendance'] = "{:.2f}".format(final_attendance)	
					
			if(attendance_applicable == '1'):
				if(final_attendance >= int(attendance_percentage)):
					d['status'] = 'Qualified'
					d['qualification_check']=1
					pass
				else:
					d['status'] = 'Not Qualified'
					d['qualification_check']=0
			else:
				d['status'] = 'Qualified'
				d['qualification_check']=1
		return participants



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
	criteria_details = frappe.db.sql(""" SELECT assessment_criteria FROM `tabCredit distribution List` where ({key} like %(txt)s or {scond}) and
													parent = '{course}'
											""".format(
												**{
												"key": searchfield,
												"scond": searchfields,
												"course": course
											}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return criteria_details
# -----------------------------------------------------------------------------------------------------------------------------

@frappe.whitelist()
def get_assignments(participant_group=None,select_assessment_criteria=None,module=None):

	assignments = []
	if participant_group != None:
		amd_data=frappe.get_all("Assignment Marks Distribution",{"course":module,"assessment_criteria":select_assessment_criteria},['name','assessment_criteria'])
		amd_data_child=[]
		for t in amd_data:
			amd_data_child=frappe.get_all("Assignment Marks Distribution Child",{"parent":t['name']},['name',"assignment_name","total_marks","weightage","passing_marks"],order_by="idx asc")
			for j in amd_data_child:
				j['assessment_criteria']=t['assessment_criteria']
		assignments = frappe.get_all("Assignment",filters=[["participant_group","=",participant_group],
													 ["assessment_criteria","=",select_assessment_criteria],['course',"=",module],["docstatus","=",1],["evaluate","=",1]],
													 fields=['name','assignment_name','assessment_criteria','weightage','total_marks','passing_marks','start_date',
					  								'end_date','total_duration'],group_by="name")
		
		final_list=[]
		for t in amd_data_child:
			a={}
			a['assignment_name']=t['assignment_name']
			a['assessment_criteria']=t['assessment_criteria']
			a['weightage']=t["weightage"]
			a['total_marks']=t['total_marks']
			a["passing_marks"]=t["passing_marks"]
			for j in assignments:
				if j['assignment_name']==t['assignment_name']:
					a['name']=j['name']
					a['start_date']=j['start_date']
					a['end_date']=j['end_date']
					a['total_duration']=j['total_duration']
			final_list.append(a)			
		assignments=final_list
	return assignments