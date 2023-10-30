# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
import json
from education.education.api import get_grade
from frappe.utils import flt


class FinalAssignmentResult(Document):
	def validate(self):
		total=0
		earned_marks=0 
		for t in self.get("assessment_result_item"):
			total+=t.total_marks
			earned_marks+=t.earned_marks
		self.total_marks=total
		self.total_marks_earned=earned_marks
		if(total == 0):
			frappe.throw('total marks cannot be zero')
		self.total_percentage=round((int(earned_marks)/int(total))*100,2)
		if self.is_new():
			duplicate_upload(self)	

			
def duplicate_upload(self):
	data=frappe.get_all("Final Assignment Result",{"tot_participant_enrollment":self.tot_participant_enrollment,"participant_id":self.participant_id,"docstatus":1})
	if data:
		frappe.throw("Result Has Been Declared For The Participant")
	



@frappe.whitelist()
def participant_group(tot_participant_enrollment):
	participant_group_data=[]
	if tot_participant_enrollment:
		participant_group_data=frappe.get_all("Participant Group",{"participant_enrollment_id":tot_participant_enrollment,"disabled":0},
										['name','participant_group','course_type','course','module_name','module_code','mode'])
		return participant_group_data

@frappe.whitelist()
def module(course):
	course_data=[]
	if course:
		course_data=frappe.get_all("Program Course",{"parent":course,"parenttype":"programs"},["parent","name",'course','course_name',"course_code","required","modes","year_end_date","is_disable"])
	return course_data



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_participant_id(doctype, txt, searchfield, start, page_len, filters):
	############################## Search Field Code################# 	
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join("PID."+field + " like %(txt)s" for field in searchfields)
	if filters.get("tot_participant_enrollment"):
		tot_participant_enrollment=filters.get("tot_participant_enrollment")
		data=frappe.db.sql("""select RP.participant,RP.participant_name from `tabReported Participant` as RP
									Join `tabToT Participant` as PID on PID.name=RP.participant
					 				Join `tabToT Participant Enrollment` as PE on PE.name=RP.parent  
									where (PID.{key} like %(txt)s or {scond}) 
									and PE.docstatus=1 and (RP.parent = '{parent}' and RP.is_reported=1)
							""".format(
						**{
							"key": searchfield,
							"scond": searchfields,
							"parent":tot_participant_enrollment,
						}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
		return data



@frappe.whitelist()
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