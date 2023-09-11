# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
import pandas as pd
from pandas import DataFrame
from frappe.model.document import Document

class RankCardPublicationTool(Document):
	def validate(self):
		if frappe.get_all("Rank Card Publication Tool",{"entrance_exam_declaration":self.entrance_exam_declaration,"docstatus":1}):
			frappe.throw("Rank Card Tool is Already Published")

	def on_cancel(self):
		
		for i in self.ranked_students_list:

			student_applicant = frappe.get_doc("Student Applicant" , i.applicant_id)
			student_applicant.student_rank.clear()
			student_applicant.save()	


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):
    
    ############################## Search Field Code#################
    searchfields = frappe.get_meta(doctype).get_search_fields()
    searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)    
    
    data=frappe.db.sql("""
        SELECT `name` FROM `tabEntrance Exam Declaration` WHERE ({key} like %(txt)s or {scond})  AND
            (`exam_start_date` <= now() AND `exam_end_date` >= now())
             and `docstatus`=1 
    """.format(
        **{
            "key": searchfield,
            "scond": searchfields,
            # "info":info
        }),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})

    return data

@frappe.whitelist()
def ranking(list_data , col , rank_name):
	ranked_data = pd.DataFrame.from_records(list_data , columns=col)
	ranked_data[rank_name] = ranked_data['earned_marks'].rank(ascending=False, method='dense')
	ranked_data = ranked_data.to_dict('records')

	return ranked_data

@frappe.whitelist()
def get_qualified_applicants(declaration , rank_card_masters):
	print("\n\n\n\nrank tool")

	rank_card_master_data = frappe.get_all("Rank Card Master" , 
											{
												"name":rank_card_masters
											},
											['maximum_number_of_ranks' , 'all_round_cutoff' , 'no_category_rank_name']
										)	## need to add program grades for result obtaining
	
	all_round_applicant_data = frappe.db.sql("""
		SELECT DISTINCT 
			res.applicant_id , 
			res.applicant_name , 
			res.student_category , 
			res.physically_disabled ,
			res.total_marks ,
			res.earned_marks ,
			res.gender
		FROM `tabEntrance Exam Result Publication` res 
		WHERE res.entrance_exam_declaration="%s" AND res.earned_marks >= %s
		ORDER BY res.earned_marks DESC LIMIT %s
	"""%(declaration,int(rank_card_master_data[0]['all_round_cutoff']),int(rank_card_master_data[0]['maximum_number_of_ranks'])), as_dict=1)
	
	all_round_ranks = ranking(all_round_applicant_data , ['applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physically_disabled' , 'total_marks' , 'earned_marks' ] , "Rank")
	
	for i in all_round_ranks:
		i['rank_type'] = rank_card_master_data[0]['no_category_rank_name']

	print(all_round_applicant_data)
	return all_round_ranks

@frappe.whitelist()
def generate_rank_cards(doc):
	print("\n\n\n")
	data = json.loads(doc)

	declaration = data['entrance_exam_declaration']
	academic_year = data['academic_year']
	academic_term = data['academic_term']
	department =data['departments']
	total_marks = data['total_marks']
	rank_card_master = data['rank_card_masters']

	all_round_ranks = data['ranked_students_list']
	
	ranking_category_data = frappe.get_all("Ranking Category" , 
												{
													'parent':rank_card_master
												},
												["student_category" , 'gender' , 'pwd' , 'category_name']

											)

	# print(all_round_ranks)

	# {'student_category': None, 'gender': None, 'pwd': 1, 'category_name': 'PWD Rank'}

	def list_of_student(student_category,gender,pwd,all_round_ranks):
		out_put=[]
		
		if student_category!=None and gender!=None:
			for t in all_round_ranks:
				if t['student_category']==student_category and t["gender"]==gender and t['physical_disability']==pwd:
					out_put.append(t)
				

		if student_category==None and gender!=None:
			for t in all_round_ranks:
				if t["gender"]==gender and t['physical_disability']==pwd:
					out_put.append(t)	

		if student_category==None and gender==None:
			for t in all_round_ranks:
				if t['physical_disability']==pwd:
					out_put.append(t)

		if student_category!=None and gender==None:
			for t in all_round_ranks:
				if t['student_category']==student_category and t['physical_disability']==pwd:
					out_put.append(t)								
		return out_put

	category_based_ranks = {}
	for i in ranking_category_data:
		category_gender_pwd_data = []
		category_gender_pwd_data=list_of_student(i['student_category'],i['gender'],i['pwd'],all_round_ranks)
		category_based_ranks[i['category_name']] = ranking(category_gender_pwd_data , ['applicant_id' , 'student_category' , 'gender' , 'physical_disability' , 'earned_marks'] , i['category_name'])
		
	# inseting all types of category based ranks in all_round_rank
	for j in all_round_ranks:
		for k in category_based_ranks:
			for l in category_based_ranks[k]:
				if j['applicant_id'] == l['applicant_id']:
					j[k] = l[k]
	count = 0
	for m in all_round_ranks:
		### to check duplicate rank cards
		rank_card_data = frappe.get_all("Rank Card",{"exam":declaration ,"applicant_id":m['applicant_id'] } , ['docstatus'])
		for i in rank_card_data:
			if i['docstatus'] == 0 or i['docstatus'] == 1:
				frappe.throw("Rank Card is Already Published")
		else:		
			rank_data = frappe.new_doc("Rank Card")
			rank_data.exam = declaration
			rank_data.applicant_id = m['applicant_id']
			rank_data.applicant_name = m['applicant_name']
			rank_data.gender = m['gender'] 
			rank_data.student_category = m['student_category']
			rank_data.physically_disabled = m['physical_disability']
			rank_data.academic_year = academic_year
			rank_data.academic_term = academic_term
			rank_data.department = department
			rank_data.total_marks = total_marks
			rank_data.earned_marks = m['earned_marks']
			
			rank_dict = {}
			
			for l in m:
				for n in ranking_category_data:
					if n['category_name'] == l:
						rank_dict[f"{l}"] = m[f"{l}"]
			student_applicant = frappe.get_doc("Student Applicant" , m['applicant_id'])

			rank_data.append("student_ranks_list" , {
					'rank_type': m['rank_type'],
					'rank_obtained' : m['rank']
			})

			student_applicant.append("student_rank" , {
					'rank_type': m['rank_type'],
					'rank_obtained' : m['rank']	
			})

			for t in rank_dict:

				rank_data.append("student_ranks_list" , {
					'rank_type': t,
					'rank_obtained' : rank_dict[t]
				})
		
				student_applicant.append("student_rank" , {
					'rank_type': t,
					'rank_obtained' : rank_dict[t]
				})

			count = count + 1
			rank_data.save()
			# rank_data.submit()
			student_applicant.save()
		
	if count == len(all_round_ranks):
		return 200
	else: 
		return 400

		
