# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FinalResultDeclarationTool(Document):

	def validate(self):
		participant_group_id = self.participant_group
		grading_scale = self.grading_scale
		participant_list = self.get('participants')

		for d in participant_list:
			participant_id = d.participant_id
			participant_name = d.participant_name
			assignments = frappe.get_all('Assignment Evaluation', filters = [['participant_group','=', participant_group_id],['participant_id','=', participant_id]], fields = ['select_assignment', 'assessment_criteria', 'marks_earned', 'total_marks', 'assignment_name'])

			parent_doc = frappe.new_doc("Final Assignment Result")
			for d in assignments:
				print('\n\n\n\n')
				print(d)
				print('\n\n\n\n')
				percentage = (d['marks_earned'] / d['total_marks']) * 100
				assignment_data_new = frappe.db.sql("""SELECT result, threshold, grade_code FROM `tabGrading Scale Interval` WHERE parent = '%s' """%(grading_scale))
				list = []
				grade = []
				for i in assignment_data_new:
					list.append(i)
				list.sort(key = lambda x:x[1])
				for i in list:
					if(percentage >= i[1]):
						grade = i
				d['result'] = grade[0]
				d['percentage'] = grade[1]
				d['grade_code'] = grade[2]

				parent_doc.append('assessment_result_item', {
				'assignment_id' : d['select_assignment'],
				'assignment_name' : d['assignment_name'],
				'assessment_criteria' : d['assessment_criteria'],
				'earned_marks' : d['marks_earned'],
				'total_marks' : d['total_marks'],
				'percentage' : d['percentage'],
				'grade' : d['grade_code'],
				'result' : d['result'],		
			})	

			total_percentage = 0
			count = 0

			for i in assignments:
				count += 1
				total_percentage += i['percentage']
			over_all_percentage = (total_percentage / count)
			
			final_list = []
			final_grade_components = []
			for i in assignment_data_new:
				final_list.append(i)
			final_list.sort(key = lambda x:x[1])
			for i in list:
				if(over_all_percentage >= i[1]):
					final_grade_components = i

			final_result = final_grade_components[0]
			final_grade = final_grade_components[2]
			# return([assignments, over_all_percentage, final_grade, final_result])
			

			parent_doc.participant_group = self.participant_group
			parent_doc.course = self.select_course
			parent_doc.course_code = self.course_code
			parent_doc.course_name = self.course_name
			parent_doc.module = self.select_module
			parent_doc.academic_year = self.academic_year
			parent_doc.academic_term = self.academic_term
			parent_doc.participant_id = participant_id
			parent_doc.participant_name = participant_name
			parent_doc.grading_scale = self.grading_scale
			parent_doc.assessment_status = "Completed"		
			parent_doc.overall_percentage = over_all_percentage
			parent_doc.overall_grade = final_grade
			parent_doc.overall_result= final_result

			parent_doc.save()

@frappe.whitelist()
def get_details(participant_group_id):
	total_participants = frappe.db.sql(""" SELECT COUNT(*) FROM `tabParticipant Table` WHERE parent = '%s'"""%(participant_group_id), as_dict=1)
	group_details = frappe.get_all('Participant Group', filters = [['name','=',participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
	course_details = frappe.get_all('Course', filters = [['name', '=', group_details[0]['course']]], fields = ['course_name','course_code'])
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], participants, course_details[0]['course_name'], course_details[0]['course_code'], total_participants[0]['COUNT(*)']]

@frappe.whitelist()
def get_participants(participant_group_id):
	participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
	return participants