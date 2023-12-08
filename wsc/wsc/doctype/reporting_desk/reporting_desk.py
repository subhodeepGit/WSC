  # Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReportingDesk(Document):
	def validate(self):
		if self.is_new():
			if frappe.get_all("Reporting Desk",{"applicant_id":self.applicant_id,"docstatus":1}):
				frappe.throw("<b>Student Has Reported at Reporting Desk</b>")

	def on_submit(self):
		# applicant_id = frappe.get_all("Rank Card" , { 'name' : self.applicant_id } , ['applicant_id'])
		applicant_id =self.applicant_id
		
		frappe.db.set_value("Student Applicant" ,applicant_id, {
			'couselling_start':1,
		})

		email = frappe.get_all('Student Applicant' , {'name':self.applicant_id},['student_email_id'])
	
		user_perm = frappe.new_doc("User Permission")
		user_perm.user = email[0]['student_email_id']
		user_perm.allow = self.doctype
		user_perm.for_value = self.name

		user_perm.save()

	def on_cancel(self):
		applicant_id =self.applicant_id
		
		frappe.db.set_value("Student Applicant" ,applicant_id, {
			'couselling_start':0,
		})
	
	def on_trash(self):
		# perm_data = frappe.get_all('User Permission' , {'for_value':self.name} , ['name' , 'for_value'])
		perm_data = frappe.db.sql("""
			SELECT
				name , for_value 
			FROM `tabUser Permission` 
			WHERE for_value = '{reporting_desk}';
		""".format(reporting_desk = self.name) , as_dict=1)

		if perm_data:
			user_perm_data = frappe.get_doc('User Permission' , perm_data[0]['name'])

			user_perm_data.delete()
		
@frappe.whitelist()
def reporting(applicant_id):

	if applicant_id:
		data_basic = frappe.get_all("Rank Card" , 
								{'applicant_id':applicant_id} ,
								['name' , 'applicant_name' ,
								'gender' , 'student_category' , 'physically_disabled' ,
								'academic_year' , 'academic_term' , 'department' ,
								'total_marks' , 'earned_marks'
								])
		
		
		data_rank = frappe.get_all("Student Ranks List" ,
								{'parent': data_basic[0]['name']} ,
								['rank_type',
								'rank_obtained'
								])
		data = []

		data.append(data_basic)
		data.append(data_rank)

		return data

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query3(doctype, txt, searchfield, start, page_len, filters):
    
	# print(filters)
    ############################## Search Field Code#################
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)    
    
	data=frappe.db.sql("""
        SELECT 
            rank.applicant_id , 
            rank.name ,
            rank.exam 
        FROM 
            `tabRank Card` rank 
        INNER JOIN 
            `tabApplicant List` applicant
        ON 
            rank.exam = applicant.parent 
        INNER JOIN 
            `tabStudent Applicant` student_applicant 
        ON 
            rank.applicant_id = student_applicant.name 
        WHERE 
            rank.exam = '{declartion}' AND
            rank.docstatus = 1 AND
			student_applicant.couselling_start = 0 AND
            student_applicant.application_status != 'Approved' AND
            student_applicant.application_status != 'Enrolled' 
        GROUP BY rank.applicant_id;
    """.format(
        **{
            "key": searchfield,
            "scond": searchfields,
            "declartion":filters['entrance_exam_declaration']
            # "info":info
        }),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
    
	return data