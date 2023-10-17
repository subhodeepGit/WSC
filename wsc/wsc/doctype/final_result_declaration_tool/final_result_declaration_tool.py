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
		pass			


def get_assignments(frm):
	doc= json.loads(frm)
	participant_id=doc['participant_id']
	list_grp=[]

	for t in doc.get("participant_group"):
		list_grp.append(t['participant_group'])
	
	module_list=[]
	for t in doc.get("modules"):
		module_list.append(t['course'])
		
	credit_distribution_list=[]
	if module_list:
		for t in module_list:
			data=frappe.get_all("Credit distribution List",[["parent","=",t]],['assessment_criteria','weightage','credits','passing_credits','total_marks','passing_marks','parent'])
			for j in data:
				credit_distribution_list.append(j)
		


	grading_scale=doc['grading_scale']

	data=[]
	if list_grp:
		if len(list_grp)==1:
			data=frappe.get_all("Assignment Evaluation",[["docstatus",'=',1],["participant_group","=",list_grp[0]],['participant_id','=',participant_id]],
									['name','assessment_component','total_marks','weightage','passing_marks','marks_earned',
									'module_code','module_name',"select_module"])
		else:
			data=frappe.get_all("Assignment Evaluation",[["docstatus",'=',1],["participant_group","IN",tuple(list_grp)],['participant_id','=',participant_id]],
									['name','assessment_component','total_marks','weightage','passing_marks','marks_earned',
									'module_code','module_name',"select_module"])
		
		for t in credit_distribution_list:
			flag="No"
			for j in data:				
				if j['select_module']==t['parent'] and j['assessment_component']==t['assessment_criteria']:
					flag="Yes"
				if flag=="Yes":
					t["flag"]="Yes"
					break
				else:
					t["flag"]="No"

		for t in credit_distribution_list:
			if t['flag']=="No":
				l=frappe.get_all("Course",{"name":t['parent']},['course_code','course_name'])
				a={}
				a['name']=""
				a['assessment_component']=t["assessment_criteria"]
				a['total_marks']=t['total_marks']
				a['weightage']=t['weightage']
				a['passing_marks']=t['passing_marks']
				a['marks_earned']=0
				a['module_code']=l[0]['course_code']
				a['module_name']=l[0]['course_name']
				a["select_module"]=t['parent']
				data.append(a)
		
		for t in data:
			percentage=(t['marks_earned']/t['total_marks'])*100
			t['percentage']=percentage
			a=get_grade_result(grading_scale,t['marks_earned'],t['total_marks'])
			t['grade_code']=a['grade']
			t['result']=a['result']
	return data

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
