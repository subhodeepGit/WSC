# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from education.education.api import get_grade
from frappe.utils import flt

class FinalResultDeclarationTool(Document):
	def validate(self):
		if self.is_new():
			duplicate_upload(self)

	def on_submit(self):
		get_assignments(self)		


def get_assignments(self):
	module_list=[]
	for t in self.get("modules"):
		module_list.append(t.course)

	credit_distribution_list=[]
	if module_list:
		for t in module_list:
			data=frappe.get_all("Credit distribution List",[["parent","=",t]],['assessment_criteria','weightage','credits','passing_credits','total_marks','passing_marks','parent'])
			for j in data:
				credit_distribution_list.append(j)		

	grading_scale=self.grading_scale

	list_grp=[]
	for t in self.get("participant_group"):
		list_grp.append(t.participant_group)	
	

	if list_grp:
		for t in self.get("participants"):
			data=[]
			participant_id=t.participant_id

			if len(list_grp)==1:
				data=frappe.get_all("Assignment Evaluation",[["docstatus",'=',1],["participant_group","=",list_grp[0]],['participant_id','=',participant_id]],
										['name','assessment_component','total_marks','weightage','passing_marks','marks_earned',
										'module_code','module_name',"select_module"])
			else:
				data=frappe.get_all("Assignment Evaluation",[["docstatus",'=',1],["participant_group","IN",tuple(list_grp)],['participant_id','=',participant_id]],
										['name','assessment_component','total_marks','weightage','passing_marks','marks_earned',
										'module_code','module_name',"select_module"])
				
			for k in credit_distribution_list:
				flag="No"
				for j in data:				
					if j['select_module']==k['parent'] and j['assessment_component']==k['assessment_criteria']:
						flag="Yes"
					if flag=="Yes":
						k["flag"]="Yes"
						break
					else:
						k["flag"]="No"	

			for k in credit_distribution_list:
				if k['flag']=="No":
					l=frappe.get_all("Course",{"name":k['parent']},['course_code','course_name'])
					a={}
					a['name']=""
					a['assessment_component']=k["assessment_criteria"]
					a['total_marks']=k['total_marks']
					a['weightage']=k['weightage']
					a['passing_marks']=k['passing_marks']
					a['marks_earned']=0
					a['module_code']=l[0]['course_code']
					a['module_name']=l[0]['course_name']
					a["select_module"]=k['parent']
					data.append(a)	
			
			for k in data:
				percentage=(k['marks_earned']/k['total_marks'])*100
				k['percentage']=percentage
				a=get_grade_result(grading_scale,k['marks_earned'],k['total_marks'])
				k['grade_code']=a['grade']
				k['result']=a['result']

			doc=frappe.new_doc("Final Assignment Result")
			doc.tot_participant_enrollment=self.tot_participant_enrollment 
			doc.tot_participant_batch=self.tot_participant_batch 
			doc.programs=self.programs
			doc.academic_year=self.academic_year
			doc.academic_term=self.academic_term
			doc.semester=self.semester
			for k in self.get("participant_group"):
				doc.append("participant_group",{
					'participant_group' : k.participant_group,
					'participant_group_name':k.participant_group_name,
					'course_type':k.course_type,
					'course':k.course,
					'module_name':k.module_name,
					'module_code':k.module_code,
					'mode':k.mode
				})
			for k in self.get("modules"):
				doc.append("modules",{
					'course':k.course,
					"course_name":k.course_name,
					"required":k.required
				})
			doc.participant_id=participant_id
			doc.participant_name=t.participant_name 
			doc.grading_scale=grading_scale
			for k in data:
				doc.append("assessment_result_item",{
					"assignment_evaluation":k['name'],
					"course":k['select_module'],
					"module_name":k['module_name'],
					"assessment_criteria":k['assessment_component'],
					"earned_marks":k['marks_earned'],
					"total_marks":k['total_marks'],
					"percentage":k['percentage'],
					"result":k['result'],
					"grading":k['grade_code'],
				})
			doc.save()	


def get_grade_result(grading_scale, earned_marks, total_marks):
    grade = get_grade(grading_scale, (flt(earned_marks)/flt(total_marks))*100)
    for g in frappe.get_all("Grading Scale Interval",{"parent":grading_scale,"grade_code":grade},['result']):
        if g.result=="PASS":
            result="PASS"
        else:
            result="FAIL"
        return {'grade': grade, 'result':result}



def duplicate_upload(self):
	data=frappe.get_all("Final Result Declaration Tool",{"tot_participant_enrollment":self.tot_participant_enrollment,"docstatus":1})
	if data:
		frappe.throw("Result Has Been Declared For The Participant Enrollment")			



@frappe.whitelist()
def get_participants(frm):
	doc= json.loads(frm)
	list_grp=[]

	for t in doc.get("participant_group"):
		list_grp.append(t['participant_group'])

	participant_list=[]
	for t in list_grp:
		assignment_declaration_data= frappe.get_all('Assignment Declaration', filters = [["participant_group","=",t],["docstatus","=",1]], fields = ["name"])
		for j in assignment_declaration_data:
			participant_l= frappe.get_all('Participant List Table', filters = [["parent","=",j['name']]], fields = ['participant_id','participant_name','participant_attendance'])
			for k in participant_l:
				if k not in participant_list:
					participant_list.append(k)				
	return {"participant_list":participant_list,"count":len(participant_list)}
