# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd

class LongLeave(Document):
	# @frappe.whitelist()
	def validate(doc):
		validate_pincode(doc)
		space(doc)
		alpha(doc)
		pincode_validation(doc)
		# mobile_number_validation(doc) #v14 phone data type present
		Al_no=doc.allotment_number
		workflow_state=doc.workflow_state
		if workflow_state=="Submit":
			info=''' WHERE `allotment_number`="%s" and  workflow_state!="Close Application" '''%(Al_no)
			long_leave_df=Long_leave_def(info)
			if len(long_leave_df)==0:
				pass
			else:
				frappe.throw("Already Documented")
		elif workflow_state=="Communication to the Student":
			medium_of_communicatinon=doc.medium_of_communicatinon
			if medium_of_communicatinon!="":
				if medium_of_communicatinon=="Telephone":
					phone_no=doc.phone_no
					if phone_no!="":
						pass
					else:
						frappe.throw("Kindly maintained Phone no.")
				elif medium_of_communicatinon=="Email":
					email_attachment=doc.email_attachment
					email_id=doc.email_id
					if email_attachment!="" and email_id!="":
						pass
					else:
						frappe.throw("Kindly Maintain Email id and and Attachment")
				elif medium_of_communicatinon=="Postal":
					address_line_1=doc.address_line_1
					pincode=doc.pincode
					city=doc.city
					state=doc.state
					letter_attacmnent=doc.letter_attacmnent
					if address_line_1!=None and pincode!=None and city!=None and state!=None and letter_attacmnent!=None:
						pass
					else:
						frappe.throw("Address line not Maintainted")
			else:
				frappe.throw("Medium Communication not Maintainted")	
		elif workflow_state=="Proceed for De-allotment":	
			frappe.db.sql("""UPDATE `tabRoom Allotment` SET `end_date`= now(), `allotment_type`="Long Leave De-allotment" WHERE `name`="%s" """%(Al_no))

			status=frappe.get_all("Room Allotment",{"name":doc.allotment_number},['hostel_registration_no','room_id'])
			frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(status[0]['room_id']))
			frappe.db.set_value("Student Hostel Admission",status[0]['hostel_registration_no'], "allotment_status", "De-allotted") 	
											
def validate_pincode(doc):
	if doc.pincode:
		if not contains_only_characters(doc.pincode):
			frappe.throw("Pincode must be 6 digits")

def contains_only_characters(pincode):
    return all(char.isalpha() or char.isspace() or char.isdigit() for char in pincode)
def Long_leave_def(info):
		Long_leave=frappe.db.sql("""SELECT name,allotment_number,student,student_name,hostel,room_number,start_date,data_11,medium_of_communicatinon,
									letter_attacmnent,phone_no,medium_of_communicatinon_from_student,communication_phone_no,reply_of_letter
								from `tabLong Leave`"""+info)

		Long_leave_df=pd.DataFrame({
				'long_leave_doc_no':[],'allotment_number':[],'student':[],'student_name':[],'hostel':[],'room_number':[],
								'start_date':[],'status':[],'medium_of_communicatinon':[],'letter_attacmnent':[],'phone_no':[],
								'medium_of_communicatinon_from_student':[],'communication_phone_no':[],'reply_of_letter':[]
			})
		
		for t in range(len(Long_leave)):
			s=pd.Series([Long_leave[t][0],Long_leave[t][1],Long_leave[t][2],Long_leave[t][3],Long_leave[t][4],Long_leave[t][5],
						Long_leave[t][6],Long_leave[t][7],Long_leave[t][8],Long_leave[t][9],Long_leave[t][10],Long_leave[t][11],
						Long_leave[t][12],Long_leave[t][13]],
								index=['long_leave_doc_no','allotment_number','student','student_name','hostel','room_number',
								'start_date','status','medium_of_communicatinon','letter_attacmnent','phone_no',
								'medium_of_communicatinon_from_student','communication_phone_no','reply_of_letter'])
			Long_leave_df=Long_leave_df.append(s,ignore_index=True)
		return Long_leave_df	

def mobile_number_validation(doc):
	if doc.phone_no:
		if not (doc.phone_no).isdigit():
			frappe.throw("Field Contact Number Accept Digits Only")
		if len(doc.phone_no)>10:
			frappe.throw("Field Contact Number must be 10 Digits")
		if len(doc.phone_no)<10:
			frappe.throw("Field Contact Number must be 10 Digits")
	
def pincode_validation(doc):
	if doc.pincode:
		if not (doc.pincode).isdigit():
			frappe.throw("Field Pincode Accept Digits Only")
		if len(doc.pincode)>6:
			frappe.throw("Field Pincode must be 6 Digits")
		if len(doc.pincode)<6:
			frappe.throw("Field Pincode must be 6 Digits")
	if doc.pincode_student:
		if not (doc.pincode_student).isdigit():
			frappe.throw("Field Pincode Accept Digits Only")
		if len(doc.pincode_student)>6:
			frappe.throw("Field Pincode must be 6 Digits")
		if len(doc.pincode_student)<6:
			frappe.throw("Field Pincode must be 6 Digits")

def alpha(doc):
	if doc.state:
		if not (doc.state).isalpha():
			frappe.throw("Field <b>State</b> Accept Alphabet Only")
	if doc.state_student:
		if not (doc.state_student).isalpha():
			frappe.throw("Field <b>State</b> Accept Alphabet Only")

def space(doc):
	if doc.phone_no is not None:
		if ' ' in doc.phone_no:
			frappe.throw("Spaces are present in the <b>Adminstration Communication Phone Number</b>.")
	if doc.communication_phone_no is not None:
		if ' ' in doc.communication_phone_no:
			frappe.throw("Spaces are present in the <b>Student Communication Phone Number</b>.")
