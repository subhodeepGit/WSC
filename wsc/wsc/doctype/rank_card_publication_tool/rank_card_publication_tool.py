# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
import pandas as pd
from pandas import DataFrame
from frappe.model.document import Document

class RankCardPublicationTool(Document):
	pass

@frappe.whitelist()
def ranking(list , col , rank_name):
	
	ranked_data = pd.DataFrame.from_records(list , columns=col)
	ranked_data[rank_name] = ranked_data['earned_marks'].rank(ascending=True, method='dense')
	ranked_data = ranked_data.to_dict('records')

	return ranked_data

@frappe.whitelist()
def get_qualified_applicants(rank_card_master , academic_year , academic_term , department):
	print("\n\n\n\n")
	# category_based_applicants_lists = []
	rank_card_master_data = frappe.get_all("Rank Card Master" , 
											{
												'name':rank_card_master , 
												'academic_year':academic_year , 
												'academic_term':academic_term,
												'department':department
											},
											['entrance_exam_declaration' , 'maximum_number_of_ranks' , 'all_round_cutoff']
										)
	
	ranking_category_data = frappe.get_all("Ranking Category" , 
												{
													'parent':rank_card_master
												},
												["student_category" , 'parent']
											)
	
	all_round_applicant_data = frappe.db.sql("""
		SELECT DISTINCT 
			res.applicant_id , 
			res.applicant_name , 
			res.student_category , 
			res.physically_disabled ,
			res.earned_marks ,
			res.gender
		FROM `tabEntrance Exam Result Publication` res INNER JOIN `tabRank Card Master` rank_master 
		WHERE res.earned_marks >= rank_master.all_round_cutoff ORDER BY res.earned_marks LIMIT {max_rank}
	""".format(max_rank = rank_card_master_data[0]['maximum_number_of_ranks']), as_dict=1)
	
	##no categories considered rank 
	all_round_ranks = ranking(all_round_applicant_data , ['applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physically_disabled' , 'earned_marks'] , "Rank")
	category_based_ranks = {}
	
	## category based

	for i in ranking_category_data:
		list_data = []
		# filtered_df = df.loc[df['student_category'] == i['student_category']]
		# ranked_data = filtered_df.to_dict('records')
		# print(ranked_data)
		category_based_applicant_data = frappe.db.sql("""
			SELECT DISTINCT 
				res.applicant_id ,
				res.earned_marks ,
				res.student_category
			FROM `tabEntrance Exam Result Publication` res INNER JOIN `tabRank Card Master` rank_master 
			WHERE res.student_category = '{category}' AND res.earned_marks >= rank_master.all_round_cutoff AND
			res.student_category != 'General' LIMIT {max_rank}
		""".format(category = i['student_category'] , max_rank = rank_card_master_data[0]['maximum_number_of_ranks']) , as_dict=1)
		
		category_based_ranks[i['student_category']] = ranking(category_based_applicant_data , ['applicant_id' , 'student_category' , 'earned_marks'] , "Rank")
		
		
	# print(category_based_ranks)
	## pwd based ranks
	pwd_applicant_data = frappe.db.sql("""
		SELECT DISTINCT 
			res.applicant_id ,
			res.earned_marks ,
			res.physically_disabled
		FROM `tabEntrance Exam Result Publication` res INNER JOIN `tabRank Card Master` rank_master 
		WHERE res.physically_disabled = 1 AND res.earned_marks >= rank_master.all_round_cutoff LIMIT {max_rank}
	""".format(max_rank = rank_card_master_data[0]['maximum_number_of_ranks']),as_dict=1)

	pwd_based_ranks = ranking(pwd_applicant_data , ['applicant_id' , 'physically_disabled' , 'earned_marks'] , "Rank")

	## inseting category based ranks in all_round_rank
	final_list = []
	for j in all_round_ranks:
		for k in category_based_ranks:
			for l in category_based_ranks[k]:
				if j['applicant_id'] == l['applicant_id'] and j['student_category'] == l['student_category']:
					j[("Category_Rank")] = l['Rank']

	## inseting pwd based ranks in all_round_rank
	for m in all_round_ranks:
		for n in pwd_based_ranks:
			if m['applicant_id'] == n['applicant_id'] and n['physically_disabled'] == m['physically_disabled'] == 1:
				m[("PWD_Rank")] = n['Rank']
	
	return all_round_ranks

@frappe.whitelist()
def generate_rank_cards(data , posting_date , total_marks , department , academic_year , rank_card_master):
	data = json.loads(data)
	rank_data = frappe.new_doc("Entrance Exam Admit Card")
	for i in data:
		rank_data.applicant_id = i['applicant_id']
		rank_data.applicant_name = i['applicant_name']
		rank_data.gender = i['gender']
		rank_data.student_category = i['student_category']
		rank_data.physically_disabled = i['physically_disabled']