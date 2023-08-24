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
	# print("\n\n\nranking")
	ranked_data = pd.DataFrame.from_records(list , columns=col)
	ranked_data[rank_name] = ranked_data['earned_marks'].rank(ascending=False, method='dense')
	ranked_data = ranked_data.to_dict('records')

	return ranked_data

@frappe.whitelist()
def get_qualified_applicants(declaration , academic_year , academic_term , department):
	print("\n\n\n\n")


	rank_card_master_data = frappe.get_all("Rank Card Master" , 
											{
												'entrance_exam_declaration':declaration , 
												'academic_year':academic_year , 
												'academic_term':academic_term,
												'department':department
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
		FROM `tabEntrance Exam Result Publication` res INNER JOIN `tabRank Card Master` rank_master
		ON res.entrance_exam_declaration = rank_master.entrance_exam_declaration 
		WHERE res.earned_marks >= rank_master.all_round_cutoff ORDER BY res.earned_marks LIMIT {max_rank}
	""".format(max_rank = rank_card_master_data[0]['maximum_number_of_ranks']), as_dict=1)
	
	all_round_ranks = ranking(all_round_applicant_data , ['applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physically_disabled' , 'total_marks' , 'earned_marks' ] , "Rank")
	
	for i in all_round_ranks:
		i['rank_type'] = rank_card_master_data[0]['no_category_rank_name']

	# print(all_round_ranks)
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
	all_round_ranks = data['ranked_students_list']

	
	final_applicant_list = []
	for i in all_round_ranks:
		dict_data = {}
		dict_data['applicant_id'] = i['applicant_id']
		dict_data['applicant_name'] = i['applicant_name']
		dict_data['gender'] = i['gender']
		dict_data['student_category'] = i['student_category']
		dict_data['physical_disability'] = i['physical_disability']
		dict_data['total_marks'] = total_marks
		dict_data['earned_marks'] = i['earned_marks']
		dict_data['rank'] = i['rank']
		final_applicant_list.append(dict_data)

	##all of ranking
	rank_card_master_data = frappe.get_all("Rank Card Master" , 
											{
												'entrance_exam_declaration':declaration , 
												'academic_year':academic_year , 
												'academic_term':academic_term,
												'department':department
											},
											['name' , 'maximum_number_of_ranks' , 'all_round_cutoff' , 'no_category_rank_name']
										)	## need to add program grades for result obtaining
	
	
	
	ranking_category_data = frappe.get_all("Ranking Category" , 
												{
													'parent':rank_card_master_data[0]['name']
												},
												["student_category" , 'gender' , 'pwd' , 'category_name']

											)

	category_based_ranks = {} ### not necessary
	
	## category based
	for i in ranking_category_data:
		list_data = []
		
		category_name = ""
		if i['student_category'] != None and i['gender'] != None:
			if i['pwd'] == 1:
				
				category_gender_pwd_data = frappe.db.sql("""
					SELECT DISTINCT 
					    res.applicant_id ,
					    res.earned_marks ,
					    res.student_category , res.gender , res.physically_disabled 
					FROM `tabEntrance Exam Result Publication` res
					INNER JOIN `tabRank Card Master` rank_master
					WHERE
					     res.earned_marks >= rank_master.all_round_cutoff AND
					     res.student_category = '{category}' AND 
					     res.gender = '{gender}' AND
					     res.physically_disabled = 1
					ORDER BY res.earned_marks
					LIMIT {max_rank}
				""".format( max_rank = rank_card_master_data[0]['maximum_number_of_ranks'] ,
							category = i['student_category'] , 
							gender = i['gender']
							) ,
							as_dict=1)
				
				category_based_ranks[i['category_name']] = ranking(category_gender_pwd_data , ['applicant_id' , 'student_category' , 'gender' , 'physically_disabled' , 'earned_marks'] , i['category_name'])

				# print(category_name)
				# print(category_gender_pwd_rank)
		
			else:
				category_gender_data = frappe.db.sql("""
					SELECT DISTINCT 
					    res.applicant_id ,
					    res.earned_marks ,
					    res.student_category , res.gender , res.physically_disabled 
					FROM `tabEntrance Exam Result Publication` res
					INNER JOIN `tabRank Card Master` rank_master
					WHERE
					     res.earned_marks >= rank_master.all_round_cutoff AND
					     res.student_category = '{category}' AND 
					     res.gender = '{gender}'
					ORDER BY res.earned_marks
					LIMIT {max_rank}
				""".format( max_rank = rank_card_master_data[0]['maximum_number_of_ranks'] ,
							category = i['student_category'] , 
							gender = i['gender']
							) ,
							as_dict=1)

				category_based_ranks[i['category_name']] = ranking(category_gender_data , ['applicant_id' , 'student_category' , 'gender' , 'physically_disabled' , 'earned_marks'] , i['category_name'])

				# print(category_name)
				# print(category_gender_rank)
			### 2 queries 111 & 110

		elif i['gender'] == None:
			# print("\n\n\ncon2")
			### 3 queries  100 , 101 , 001
			
			if i['student_category'] != None and i['pwd'] != 1:
				# print(i)
				category_data = frappe.db.sql("""
					SELECT DISTINCT 
					    res.applicant_id ,
					    res.earned_marks ,
					    res.student_category , res.gender , res.physically_disabled 
					FROM `tabEntrance Exam Result Publication` res
					INNER JOIN `tabRank Card Master` rank_master
					WHERE
					     res.earned_marks >= rank_master.all_round_cutoff AND
					     res.student_category = '{category}'
					ORDER BY res.earned_marks
					LIMIT {max_rank}
				""".format( max_rank = rank_card_master_data[0]['maximum_number_of_ranks'] ,
							category = i['student_category'] 
							) ,
							as_dict=1)
				
				category_name = i['student_category']

				category_based_ranks[i['category_name']] = ranking(category_data , ['applicant_id' , 'student_category' , 'gender' , 'physically_disabled' , 'earned_marks'] , i['category_name'])

				### query is running thrice due to because in 'i' there is 101 and 100 is considered same in this condition
				
		
			elif i['student_category'] == None and i['pwd'] == 1:
				# print(i)
				pwd_data = frappe.db.sql("""
					SELECT DISTINCT 
					    res.applicant_id ,
					    res.earned_marks ,
					    res.student_category , res.gender , res.physically_disabled 
					FROM `tabEntrance Exam Result Publication` res
					INNER JOIN `tabRank Card Master` rank_master
					WHERE
					     res.earned_marks >= rank_master.all_round_cutoff AND
					     res.physically_disabled = 1
					ORDER BY res.earned_marks
					LIMIT {max_rank}
				""".format( max_rank = rank_card_master_data[0]['maximum_number_of_ranks'] ) ,
							as_dict=1)

				category_name = "PWD"

				category_based_ranks[i['category_name']] = ranking(pwd_data , ['applicant_id' , 'student_category' , 'gender' , 'physically_disabled' , 'earned_marks'] , i['category_name'])
				# print(pwd_rank)

			if i['student_category'] != None and i['pwd'] == 1:
				# print(i)
				category_pwd_data = frappe.db.sql("""
					SELECT DISTINCT 
					    res.applicant_id ,
					    res.earned_marks ,
					    res.student_category , res.gender , res.physically_disabled 
					FROM `tabEntrance Exam Result Publication` res
					INNER JOIN `tabRank Card Master` rank_master
					WHERE
					     res.earned_marks >= rank_master.all_round_cutoff AND
					     res.student_category = '{category}' AND
				      	 res.physically_disabled = 1
					ORDER BY res.earned_marks
					LIMIT {max_rank}
				""".format( max_rank = rank_card_master_data[0]['maximum_number_of_ranks'] ,
							category = i['student_category'] 
							) ,
							as_dict=1)
				
				category_name = i['student_category'] + '-' + "PWD"

				category_based_ranks[i['category_name']] = ranking(category_pwd_data , ['applicant_id' , 'student_category' , 'gender' , 'physically_disabled' , 'earned_marks'] , i['category_name'])
				
				# print(category_pwd_rank)	

		elif i['student_category'] == None:

			### 2 queries 011 & 010 
			
			if i['pwd'] == 1:
				gender_pwd_data = frappe.db.sql("""
					SELECT DISTINCT 
					    res.applicant_id ,
					    res.earned_marks ,
					    res.student_category , res.gender , res.physically_disabled 
					FROM `tabEntrance Exam Result Publication` res
					INNER JOIN `tabRank Card Master` rank_master
					WHERE
					     res.earned_marks >= rank_master.all_round_cutoff AND
					     res.gender = '{gender}' AND
				    	 res.physically_disabled = 1
					ORDER BY res.earned_marks
					LIMIT {max_rank}
				""".format( max_rank = rank_card_master_data[0]['maximum_number_of_ranks'] ,
							gender = i['gender']
							) ,
							as_dict=1)
				
				category_name = i['gender'] + '-' + "PWD"

				category_based_ranks[i['category_name']] = ranking(gender_pwd_data , ['applicant_id' , 'student_category' , 'gender' , 'physically_disabled' , 'earned_marks'] , i['category_name'])

				# print(gender_pwd_rank)
			else:
				gender_data = frappe.db.sql("""
					SELECT DISTINCT 
					    res.applicant_id ,
					    res.earned_marks ,
					    res.student_category , res.gender , res.physically_disabled 
					FROM `tabEntrance Exam Result Publication` res
					INNER JOIN `tabRank Card Master` rank_master
					WHERE
					     res.earned_marks >= rank_master.all_round_cutoff AND
					     res.gender = '{gender}' 
					ORDER BY res.earned_marks
					LIMIT {max_rank}
				""".format( max_rank = rank_card_master_data[0]['maximum_number_of_ranks'] ,
							gender = i['gender']
							) ,
							as_dict=1)
				
				category_name = i['gender']

				category_based_ranks[i['category_name']] = ranking(gender_data , ['applicant_id' , 'student_category' , 'gender' , 'physically_disabled' , 'earned_marks'] , i['category_name'])

	# inseting all types of category based ranks in all_round_rank
	for j in final_applicant_list:
		for k in category_based_ranks:
			for l in category_based_ranks[k]:
				if j['applicant_id'] == l['applicant_id']:
					j[k] = l[k]
	
	# print(final_applicant_list)

	# for i in final_applicant_list:
	# 	for j in ranking_category_data:
	# 		# print(j)
	# 		rank_type = j['category_name']
	# 		# print(rank_type)
	# 		if j['category_name'] in i:
	# 			print(i)
	# 	print("\n")	
	print(final_applicant_list)
	for m in final_applicant_list:

		rank_data = frappe.new_doc("Rank Card")
		rank_data.applicant_id = m['applicant_id']
		rank_data.applicant_name = m['applicant_name']
		rank_data.gender = m['gender'] 
		rank_data.student_category = m['student_category']
		rank_data.physically_disabled = m['physical_disability']
		rank_data.academic_year = academic_year
		rank_data.academic_term = academic_term
		rank_data.department = department
		rank_data.no_category_rank = m['rank']
		rank_data.total_marks = m['total_marks']
		rank_data.earned_marks = m['earned_marks']
		
		# for  n in ranking_category_data:
		# 	if n['category_name'] in m:
		rank_dict = {}
		
		for l in m:
			for n in ranking_category_data:
				if n['category_name'] == l:
					# print(m[l] , l , m['applicant_id'])
					# rank_list[l] = m[l]
					rank_dict[f"{l}"] = m[f"{l}"]
					# rank_list.append(m[l])
			# print(rank_dict)		
		student_applicant = frappe.get_doc("Student Applicant" , m['applicant_id'])

		for t in rank_dict:

			rank_data.append("student_ranks_list" , {
				'rank_type': t,
				'rank_obtained' : rank_dict[t]
			})
	
			student_applicant.append("student_rank" , {
				'rank_type': t,
				'rank_obtained' : rank_dict[t]
			})
		
		rank_data.save()
		rank_data.submit()
		student_applicant.save()
		

		
