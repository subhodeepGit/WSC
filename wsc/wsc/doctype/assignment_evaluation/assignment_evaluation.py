# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import comma_and, get_link_to_form,get_link_to_form, getdate, formatdate
from frappe import msgprint, _

class AssignmentEvaluation(Document):
	def validate(self):
		self.validate_duplication()



	def validate_duplication(self):
		"""Check if the Assignment Evaluation Record is Unique"""
		assignment_record = None
		
		assignment_record = frappe.db.exists('Assignment Evaluation', {
			'assignment_declaration': self.assignment_declaration,
			'participant_group': self.participant_group,
			'academic_year': self.academic_year,
			'participant_id': self.participant_id,
			'docstatus': ('!=', 2),
			'name': ('!=', self.name)
		})

		if assignment_record:
			record = get_link_to_form('Assignment Evaluation', assignment_record)
			frappe.throw(_('Assignment Evaluation record {0} already exists!')
				.format(record), title=_('Duplicate Entry'))





@frappe.whitelist()
def get_assignment_details(assignment_name = None):
	if(assignment_name == None):
		return ['','','','','', '']
	else:
		count1 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment` WHERE name = '%s'"""%(assignment_name))
		count2 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment Declaration` WHERE name = '%s'"""%(assignment_name))
		if(count1[0][0] > 0):
			criteria_details = frappe.get_all('Assignment', filters = [['name','=',assignment_name]], fields = ['assignment_name','assessment_criteria','total_marks', 'passing_marks', 'weightage'])
			return [criteria_details[0]['assessment_criteria'], criteria_details[0]['total_marks'],criteria_details[0]['passing_marks'],criteria_details[0]['weightage'],criteria_details[0]['assignment_name']]
		elif(count2[0][0] > 0):
			criteria_details = frappe.get_all('Assignment Declaration', filters = [['name','=',assignment_name]], fields = ['assignment_name','select_assessment_criteria','total_marks','pass_marks','weightage'])
			return [criteria_details[0]['select_assessment_criteria'], criteria_details[0]['total_marks'],criteria_details[0]['pass_marks'],criteria_details[0]['weightage'],criteria_details[0]['assignment_name']]


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

# -----------------------------------------------------------------------------------------------------------------------------

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_qualified_participants(doctype, txt, searchfield, start, page_len, filters):
	############################## Search Field Code################# 	
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join("TP."+field + " like %(txt)s" for field in searchfields)
	# data=frappe.db.sql(""" select PT.participant_id, PT.participant_name, PT.status ,
	# 				IF((PT.qualification_check = 1 and PT.status="Not Qualified" ), CONCAT('<b><p style="color: red;">', 'Specially Qualified', '</p></b>'), '') AS specially_qualified
	# 				from `tabParticipant List Table` as PT
	# 				JOIN `tabToT Participant` as TP on TP.name=PT.participant_id
	# 				where (TP.{key} like %(txt)s or {scond}) and 
	# 				PT.parent ='{assignment_declaration}' and PT.qualification_check = 1
	# 					 """.format(
	# 				**{
	# 					"key": searchfield,
	# 					"scond": searchfields,
	# 					"assignment_declaration":filters.get("assignment_declaration"),
	# 				}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	data=frappe.db.sql(""" select PT.participant_id, PT.participant_name, PT.status ,
					IF((PT.qualification_check = 1 and PT.status="Not Qualified" ), CONCAT('<b>', 'Specially Qualified', '</b>'), '') AS specially_qualified
					from `tabParticipant List Table` as PT
					JOIN `tabToT Participant` as TP on TP.name=PT.participant_id
					where (TP.{key} like %(txt)s or {scond}) and 
					PT.parent ='{assignment_declaration}' and PT.qualification_check = 1
						 """.format(
					**{
						"key": searchfield,
						"scond": searchfields,
						"assignment_declaration":filters.get("assignment_declaration"),
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	############################ End Search Field Code ###############
	return data


@frappe.whitelist()
def get_assignments_if_uploaded(assignment_declaration = None, participant_id = None):
	assignments = frappe.get_all("Job sheet", filters=[["parent","=",assignment_declaration],["docstatus","=",1]], fields=["job_sheet_number","job_sheet_name","assessment_criteria","start_date_and_time","total_durationin_hours","total_marks","pass_marks","weightage","end_date_and_time","marks"])
	uploaded_assignments = frappe.get_all("Assignment Upload", filters=[["participant_id","=",participant_id],["docstatus","=",1]], fields=["name","assignment_id"])

	if assignments:
		for i in assignments:
			if uploaded_assignments:
				for j in uploaded_assignments:
					if i['job_sheet_number']==j['assignment_id']:
						i['assignment_upload_status']="Submitted"
						i['assignment_upload_link']=j['name']
					else:
						i['assignment_upload_status']="Not Submitted"
						i['assignment_upload_link']=None
			else:
				i['assignment_upload_status']="Not Submitted"
				i['assignment_upload_link']=None

		return assignments
	
	else: return None