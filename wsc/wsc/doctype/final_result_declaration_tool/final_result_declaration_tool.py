# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class FinalResultDeclarationTool(Document):

	def validate(self):
		pass
# 		participant_group_id = self.participant_group
# 		grading_scale = self.grading_scale
# 		participant_list = self.get('participants')

# 		for d in participant_list:
# 			participant_id = d.participant_id
# 			participant_name = d.participant_name

# 			assignments = frappe.get_all('Assignment Evaluation', filters = [['participant_group','=', participant_group_id],['participant_id','=', participant_id]], fields = ['select_assignment', 'assessment_criteria', 'marks_earned', 'total_marks', 'assignment_name'])
# 			assignment_data_new = ''
# 			parent_doc = frappe.new_doc("Final Assignment Result")
# 			list = []
# 			for d in assignments:
# 				percentage = (d['marks_earned'] / d['total_marks']) * 100
# 				assignment_data_new = frappe.db.sql("""SELECT result, threshold, grade_code FROM `tabGrading Scale Interval` WHERE parent = '%s' """%(grading_scale))
				
# 				grade = []
# 				for i in assignment_data_new:
# 					list.append(i)
# 				list.sort(key = lambda x:x[1])
# 				for i in list:
# 					if(percentage >= i[1]):
# 						grade = i
# 				d['result'] = grade[0]
# 				d['percentage'] = grade[1]
# 				d['grade_code'] = grade[2]

# 				parent_doc.append('assessment_result_item', {
# 				'assignment_id' : d['select_assignment'],
# 				'assignment_name' : d['assignment_name'],
# 				'assessment_criteria' : d['assessment_criteria'],
# 				'earned_marks' : d['marks_earned'],
# 				'total_marks' : d['total_marks'],
# 				'percentage' : d['percentage'],
# 				'grade' : d['grade_code'],
# 				'result' : d['result'],		
# 			})	

# 			total_percentage = 0
# 			count = 0
# 			over_all_percentage = 0

# 			for i in assignments:
# 				count += 1
# 				total_percentage += i['percentage']

# 			if(count == 0 and total_percentage == 0):
# 				over_all_percentage = 0
# 			else:
# 				over_all_percentage = (total_percentage / count)
			
# 			final_list = []
# 			final_grade_components = []

# 			for i in assignment_data_new:
# 				final_list.append(i)
# 			final_list.sort(key = lambda x:x[1])
# 			for i in list:
# 				if(over_all_percentage >= i[1]):
# 					final_grade_components = i
# 			print('')
# 			final_result = final_grade_components[0]
# 			final_grade = final_grade_components[2]


# 			# Calculating attendance
# 			participant_classes = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Class Table` WHERE parent = '%s'"""%(participant_group_id))
# 			participant_present_for = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Participant Attendance` WHERE participant_id = '%s' AND participant_group = '%s'"""%(participant_id, participant_group_id))
# 			final_attendance = (participant_present_for[0][0]/participant_classes[0][0])*100
			

# 			parent_doc.participant_group = self.participant_group
# 			parent_doc.course = self.select_course
# 			parent_doc.course_code = self.course_code
# 			parent_doc.course_name = self.course_name
# 			parent_doc.module = self.select_module
# 			parent_doc.academic_year = self.academic_year
# 			parent_doc.academic_term = self.academic_term
# 			parent_doc.participant_id = participant_id
# 			parent_doc.participant_name = participant_name
# 			parent_doc.grading_scale = self.grading_scale
# 			parent_doc.assessment_status = "Completed"		
# 			parent_doc.overall_percentage = over_all_percentage
# 			parent_doc.overall_grade = final_grade
# 			parent_doc.overall_result= final_result
# 			parent_doc.attendance_percentage= final_attendance
# 			parent_doc.save()

# @frappe.whitelist()
# def get_details(participant_group_id):
# 	total_participants = frappe.db.sql(""" SELECT COUNT(*) FROM `tabParticipant Table` WHERE parent = '%s'"""%(participant_group_id), as_dict=1)
# 	group_details = frappe.get_all('Participant Group', filters = [['name','=',participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
# 	participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
# 	course_details = frappe.get_all('Course', filters = [['name', '=', group_details[0]['course']]], fields = ['course_name','course_code'])
# 	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], participants, course_details[0]['course_name'], course_details[0]['course_code'], total_participants[0]['COUNT(*)']]

@frappe.whitelist()
def get_participants(frm):
	doc= json.loads(frm)
	print("\n\n\n\n\n")
	print("ok")
	tot_participant_enrollment=doc['tot_participant_enrollment']
	list_grp=[]

	for t in doc.get("participant_group"):
		list_grp.append(t['participant_group'])

	participant_list=[]
	for t in list_grp:
		assignment_declaration_data= frappe.get_all('Assignment Declaration', filters = [["participant_group","=",t],["docstatus","=",1]], fields = ["name"])
		for j in assignment_declaration_data:
			participant_l= frappe.get_all('Participant List Table', filters = [["parent","=",j],], fields = ['participant_id','participant_name','participant_attendance'])
			for k in participant_l:
				if k not in participant_list:
					participant_list.append(k)
	print(participant_list)
					


	# return participants


# # ---------------------------------------------------------------------------------------------
# @frappe.whitelist()
# def instructor(doctype, txt, searchfield, start, page_len, filters):
# 	searchfields = frappe.get_meta(doctype).get_search_fields()
# 	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

# 	participant_group_id=filters.get('participant_group_id')
# 	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where ({key} like %(txt)s or {scond}) and
# 				    parent = '{participant_group_id}'
# 				    """.format(
# 						**{
# 						"key": searchfield,
# 						"scond": searchfields,
# 						"participant_group_id":participant_group_id
# 					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
# 	return instructor_details

# @frappe.whitelist()
# def participant(doctype, txt, searchfield, start, page_len, filters):
# 	searchfields = frappe.get_meta(doctype).get_search_fields()
# 	searchfields = " or ".join("TP."+field + " like %(txt)s" for field in searchfields)
# 	participant_group_id=filters.get('participant_group_id')
# 	participant_details = frappe.db.sql(""" SELECT TP.name 
# 											FROM `tabParticipant Table` as PT
# 											JOIN `tabToT Participant` as TP on TP.name=PT.participant
# 											where (TP.{key} like %(txt)s or {scond}) and
# 													PT.parent = '{participant_group_id}'
# 											""".format(
# 												**{
# 												"key": searchfield,
# 												"scond": searchfields,
# 												"participant_group_id":participant_group_id
# 											}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
# 	return participant_details
# # -----------------------------------------------------------------------------------------------------------------------------