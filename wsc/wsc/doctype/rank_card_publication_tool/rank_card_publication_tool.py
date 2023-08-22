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
def get_qualified_applicants(rank_card_master , academic_year , academic_term , department):
	print("\n\n\n\n")

	## need to add program grades for result obtaining
	applicant_results = frappe.get_all("Entrance Exam Result Publication" , 
				    						{
												'academic_year':academic_year , 
												'academic_term':academic_term,
												'department':department
											} , 
											['applicant_id' , 'applicant_name' , 'student_category' , 'gender' , 'physically_disabled']
										)
	
	print(applicant_results)
	# category_based_applicants_lists = []
	
	return applicant_results

@frappe.whitelist()
def generate_rank_cards(rank_card_master , academic_year , academic_term , department ):
	print("\n\n\n")
	
	##all of ranking
	rank_card_master_data = frappe.get_all("Rank Card Master" , 
											{
												'name':rank_card_master , 
												'academic_year':academic_year , 
												'academic_term':academic_term,
												'department':department
											},
											['entrance_exam_declaration' , 'maximum_number_of_ranks' , 'all_round_cutoff' , 'no_category_rank_name']
										)
	
	ranking_category_data = frappe.get_all("Ranking Category" , 
												{
													'parent':rank_card_master
												},
												["student_category" , 'gender' , 'pwd' , 'category_name']

											)
	
	## need to update queries as per department and course type
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
		WHERE res.earned_marks >= rank_master.all_round_cutoff ORDER BY res.earned_marks LIMIT {max_rank}
	""".format(max_rank = rank_card_master_data[0]['maximum_number_of_ranks']), as_dict=1)
	
	##no categories considered rank 
	all_round_ranks = ranking(all_round_applicant_data , ['applicant_id' , 'applicant_name' , 'gender' , 'student_category' , 'physically_disabled' , 'total_marks' , 'earned_marks'] , f"{rank_card_master_data[0]['no_category_rank_name']} Rank")
	
	category_based_ranks = {} ### not necessary
	
	## category based
	for i in ranking_category_data:
		list_data = []
		
		category_name = ""
		if i['student_category'] != None and i['gender'] != None:
			if i['pwd'] == 1:
				# print(i['category_name'] , i)
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
				
				category_name = i['student_category'] + '-' + i['gender'] + '-' + 'PWD'

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
				
				category_name = i['student_category'] + '-' + i['gender'] 

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

	## inseting all types of category based ranks in all_round_rank
	for j in all_round_ranks:
		for k in category_based_ranks:
			for l in category_based_ranks[k]:
				if j['applicant_id'] == l['applicant_id']:
					j[k] = l[k]
	
	final_student_list=[]
	for a in category_based_ranks:
    # print(a)
    # print(data[a])
		for j in category_based_ranks[a]:
        # print(j)
			j.update({"rank_type":a})
        # print(j)
			final_student_list.append(j)
	
	for t in all_round_ranks:
		print("t",t)
		for j in final_student_list:
			if j['applicant_id']==t['applicant_id']:
				print("j",j)
				print(j['%s'%(j['rank_type'])])
		print("\n\n\n")   

	
	# for m in ranking_category_data:
	# 	for n in all_round_ranks:
	# 		print(m , n)
			# if m['category_name'] == n[]
		# rank_data = frappe.new_doc("Rank Card")
		# rank_data.applicant_id = i['applicant_id']
		# rank_data.applicant_name = i['applicant_name']
		# rank_data.gender = i['gender'] 
		# rank_data.student_category = i['student_category']
		# rank_data.physically_disabled = i['physical_disability']
		# rank_data.academic_year = academic_year
		# rank_data.academic_term = academic_term
		# rank_data.department = department

		# rank_data.total_marks = m['total_marks']
		# rank_data.earned_marks = m['earned_marks']
		
	# 	rank_data.append("student_ranks_list" , {
	# 		'general_rank' : i['all_student_based_rank'],
	# 		'category_based_rank' : i['category_based_rank'],
	# 		'pwd_based_rank' : i['pwd_based_rank']
	# 	})

	# 	# print(rank_data)
	# 	rank_data.save()
	# 	rank_data.submit()
		
	# 	student_applicant = frappe.get_doc("Student Applicant" , i['applicant_id'])
		
	# 	if(len(student_applicant.student_rank) == 0):
	# 		student_applicant.append("student_rank" , {
	# 			'general_rank' : i['all_student_based_rank'],
	# 			'category_based_rank' : i['category_based_rank'],
	# 			'pwd_based_rank' : i['pwd_based_rank']
	# 		})

	# 	student_applicant.save()
		# student_applicant.update()
		# student_applicant.submit()


		
