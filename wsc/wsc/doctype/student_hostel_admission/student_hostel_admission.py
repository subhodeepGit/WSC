# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.accounts.general_ledger import make_reverse_gl_entries
import json

class StudentHostelAdmission(Document):
	def validate(doc):
		doc.allotment_status = "Not Reported"
		data=frappe.get_all("Student Hostel Admission",fields=[["student","=",doc.student],["allotment_status","!=","Allotted"],
					["allotment_status","!=","De-Allotted"],["docstatus","=",1]])		
		if len(data)!=0:
			frappe.throw("Student record already present")


	def on_submit(doc):
		if doc.hostel_fee_applicable=="YES":
			fee_structure_id= fee_structure_validation(doc)
			create_fees(doc,fee_structure_id[0],fee_structure_id[1],on_submit=0)
		# fee_structure_id,
		# student = doc.student
		# frappe.db.sql(""" UPDATE `tabStudent Applicant` as SA 
		# 					JOIN `tabStudent` S on S.student_applicant=SA.name
		# 					SET SA.hostel_required = 1
		# 					WHERE S.name="%s" """%(student)) ##### Student Applicant
	# def before_save(doc):
	# 	student = doc.student
	# 	a=frappe.db.sql("""SELECT SA.Name 
	# 					from `tabStudent Applicant` as SA 
	# 					JOIN `tabStudent` S on S.student_applicant=SA.name
	# 					WHERE S.name="%s" """%(student))
	# 	if len(a)!=0:				
	# 		pass
	# 	else:
	# 		frappe.throw("Student Applicant not maintained")##### Student Applicant


	def after_insert(doc):
		frappe.db.set_value("Student Hostel Admission",doc.name, "allotment_status", "Not Reported") 



	def on_cancel(doc):
		cancel_fees(doc)
		student = doc.student
		frappe.db.sql(""" UPDATE `tabStudent Applicant` as SA 
							JOIN `tabStudent` S on S.student_applicant=SA.name
							SET SA.hostel_required = 0
							WHERE S.name="%s" """%(student))
		frappe.msgprint("Your Application is cancelled")
		frappe.db.set_value("Student Hostel Admission",doc.name, "allotment_status", "Cancelled") 



def fee_structure_validation(doc): 
	existed_fs = frappe.db.get_list("Fee Structure Hostel", {"name":doc.hostel_fee_structure,'docstatus':1},["name","cost_center"])
	if len(existed_fs) != 0:
		fee_structure_id =doc.hostel_fee_structure
		cost_center=existed_fs[0]['cost_center']
		return [fee_structure_id,cost_center]
	else:
		frappe.throw("Fee Structure Not Found")


def create_fees(doc,fee_structure_id,cost_center=None,on_submit=0):
	data = frappe.get_all("Student Hostel Admission",{'student':doc.student,'docstatus':1},['name','first_name','roll_no','registration_number','email_address','due_date'],limit=1)
	fees = frappe.new_doc("Hostel Fees")
	fees.student = doc.student
	fees.student_name = doc.first_name    
	fees.due_date = doc.due_date
	fees.student_email=doc.email_address
	fees.hostel_admission = data[0]['name']
	for t in doc.get("current_education_fetch"):
		fees.programs=t.programs
		fees.program=t.semesters
		fees.academic_year=t.academic_year
		fees.academic_term=t.academic_term
		t.term_date = frappe.get_all("Academic Term",{'name': t.academic_term},['term_start_date','term_end_date'])
		fees.valid_from=t.term_date[0]['term_start_date']
		fees.valid_to =t.term_date[0]['term_end_date']             
	fees.hostel_fee_structure = fee_structure_id
	fees.cost_center=cost_center
	ref_details = frappe.get_all("Fee Component",{"parent":fee_structure_id},['fees_category','amount','receivable_account','income_account','company','grand_fee_amount','outstanding_fees'],order_by="idx asc")
	for i in ref_details:
		fees.append("components",{
			'fees_category' : i['fees_category'],
			'amount' : i['amount'],
			'receivable_account' : i['receivable_account'],
			'income_account' : i['income_account'],
			'company' : i['company'],
			'grand_fee_amount' : i['grand_fee_amount'],
			'outstanding_fees' : i['outstanding_fees'],
		})	
	fees.save()
	fees.submit()
	doc.hostel_fees=fees.fees_id
	doc.hostel_fees_id=fees.name
	frappe.db.set_value("Student Hostel Admission",doc.name,"hostel_fees",fees.fees_id)	
	frappe.db.set_value("Student Hostel Admission",doc.name,"hostel_fees_id",fees.name)

def cancel_fees(doc):
	hostel_fee_object= frappe.get_doc("Hostel Fees",doc.hostel_fees_id)
	hostel_fee_object.cancel()
	frappe.msgprint("Hostel Fees is also cancelled")


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def hostel_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT `name`,`hostel_type` from `tabHostel Masters` WHERE `start_date`<=now() and `end_date`>=now()""")


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def room_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT `name`,`feature`,`capacity` from `tabRoom Type` WHERE `start_date`<=now() and `end_date`>=now()""")

@frappe.whitelist()
def fst_query(doc):
	doc = json.loads(doc)
	current_education_fetch=doc.get("current_education_fetch")
	filtered_fst={'programs':current_education_fetch[0]['programs'],
				'semesters':current_education_fetch[0]['semesters'],
				"room_type":doc.get("room_type"),
				'academic_year':current_education_fetch[0]['academic_year'],
				'academic_term':current_education_fetch[0]['academic_term']
				}		
	return filtered_fst
