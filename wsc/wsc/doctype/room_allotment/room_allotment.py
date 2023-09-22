# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

from dataclasses import fields
import re
import frappe
from frappe import _
import frappe.model
import frappe.utils
from frappe.model.document import Document
import pandas as pd
import datetime
from datetime import date
from wsc.wsc.doctype.user_permission import add_user_permission


class RoomAllotment(Document):
	# @frappe.whitelist()
	def validate(doc):
		student=doc.student
		df1=vacancy_quety_vali("Student_info",student)					
		if len(df1)==0:
			pass
		else:
			ck_data=df1[(df1['start_date']<=datetime.date.today())&(df1['end_date']>=datetime.date.today())].reset_index()
			if len(ck_data)!=0:
				frappe.throw("%s is already allotted in %s, Room No. %s (%s)"%(ck_data['student_name'][0],ck_data['hostel_id'][0],ck_data['Room_No'][0],ck_data['room_id'][0]))	
			else:
				room_id=doc.room_id
				room_info_vac=vacancy_quety_vali("Genaral",room_id)
				if room_info_vac["validity"][0]=="Approved":
					if room_info_vac["Room_al_status"][0]=="Allotted":
						if room_info_vac["Vacancy"][0]>0:
							ck_data=df1[(df1['allotment_type']=="Debar") | (df1['allotment_type']=="University Debar") | (df1['allotment_type']=="Passout")
										| (df1['allotment_type']=="Cancellation of Admission") | (df1['allotment_type']=="Death") ].reset_index()
							if len(ck_data)==0:
								pass
							else:
								frappe.throw("Student can't be allotted")
						else:
							Al_stu=vacancy_quety_vali("Alloted_student",room_id)
							a=""
							for t in range(len(Al_stu)):
								b="%s "%(Al_stu["Al_no"][t])
								a=a+b
							frappe.throw("Already Room is full with allotment No. "+a)
					else:
						frappe.throw("Room is not allottable for the student")
				else:
					frappe.throw("Room is not valid")	
				
	# @frappe.whitelist()
	def on_submit(doc):
		print('\n\n\n')
		room_id=doc.room_id
		# room_info_vac=vacancy_quety_vali("Genaral",room_id)
		# if room_info_vac["validity"][0]=="Approved":
		# 	if room_info_vac["Room_al_status"][0]=="Allotted":
		# 		if room_info_vac["Vacancy"][0]>0:
		# 			room_id=doc.room_id
		# 			frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`-1 WHERE `name`="%s" """%(room_id)) 
		# 			frappe.db.set_value("Student Hostel Admission",doc.hostel_registration_no, "allotment_status", "Allotted") 
		# 			pass
		# 		else:
		# 			Al_stu=vacancy_quety_vali("Alloted_student",room_id)
		# 			a=""
		# 			for t in range(len(Al_stu)):
		# 				b="%s "%(Al_stu["Al_no"][t])
		# 				a=a+b
		# 			frappe.throw("Already Room is full with Allotment No. "+a)
		# 	else:
		# 		frappe.throw("Room is not allottable to the student")
		# else:
		# 	frappe.throw("Room is not valid")
		frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`-1 WHERE `name`="%s" """%(room_id)) 
		frappe.db.set_value("Student Hostel Admission",doc.hostel_registration_no, "allotment_status", "Allotted") 
		stu_user=frappe.get_all("Student",{'name':doc.student},['user'])
		if len(stu_user)>0:
			add_user_permission("Room Allotment",doc.name,stu_user[0]['user'],doc)

	# @frappe.whitelist()
	def on_cancel(doc):
		room_id=doc.room_id
		frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(room_id))
		frappe.db.set_value("Student Hostel Admission",doc.hostel_registration_no, "allotment_status", "Cancelled") 
		cancel_hostel_admission(doc)
		doc.delete_permission()

	def delete_permission(self):
		for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
			frappe.delete_doc("User Permission",d.name)
	


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def test_query(doctype, txt, searchfield, start, page_len, filters):
	User=frappe.session.user
	if frappe.session.user=="Administrator" or "Student" in frappe.get_roles(frappe.session.user):
		return frappe.db.sql("""
				SELECT `hostel_name` from `tabHostel Masters` WHERE `start_date`<=now() and `end_date`>=now()""")
		
	else:
		return frappe.db.sql("""
				SELECT `hostel_masters` from `tabEmployee Hostel Allotment` WHERE user_name="%s" and
				(`start_date`<=now() and `end_date`>=now())"""%(User))		
			
def cancel_hostel_admission(doc):
	if doc.hostel_registration_no:
		hostel_admission_object= frappe.get_doc("Student Hostel Admission",doc.hostel_registration_no)
		if hostel_admission_object.docstatus!=2 and hostel_admission_object.docstatus!=0:
			hostel_admission_object.cancel()
		frappe.msgprint("Hostel admission is also cancelled")



def vacancy_quety_vali(flag,info):
	if flag=="Genaral":
		vac_info=frappe.db.sql("""SELECT HR.name,HR.room_number,HR.actual_capacity,HR.hostel_id,HR.validity,HR.room_description,HR.status,
								(HR.actual_capacity-(SELECT count(RA.room_id)
								from `tabRoom Allotment` RA
								WHERE RA.room_id=HR.name
								And (RA.start_date<=now() and RA.end_date>=now()) and RA.docstatus!=2 and RA.docstatus!=0
								))AS Vacancy 
								from `tabRoom Masters` as HR
								where HR.name="%s" """%(info))					
		df1=pd.DataFrame({
			"Room_id":[],"room_number":[],"present_capacity":[],"hostel_id":[],"validity":[],"room_description":[],"Room_al_status":[],"Vacancy":[] 
			})
		for t in range(len(vac_info)):
			s=pd.Series([vac_info[t][0],vac_info[t][1],vac_info[t][2],vac_info[t][3],vac_info[t][4],vac_info[t][5],vac_info[t][6],vac_info[t][7]],
								index=["Room_id","room_number","present_capacity","hostel_id","validity","room_description","Room_al_status","Vacancy"])
			df1=df1.append(s,ignore_index=True)			
		return df1
	elif flag=="Student_info":	
		# Stu_info=frappe.db.sql(""" select * from `tabRoom Allotment` as RA where RA.student="%s" and RA.docstatus!=2 """%(info))
		Stu_info=frappe.db.sql(""" select name,creation,modified,modified_by,owner,docstatus,
			idx,naming_series,student,student_name,hostel_id,start_date,allotment_type,end_date,room_id,
			room_type,employee,employee_name,room_number from `tabRoom Allotment` where student="%s" and docstatus!=2 and docstatus!=0 """%(info))
		df1=pd.DataFrame({
			'Al_no':[],'creation':[],'modified':[],'modified_by':[],
			'owner':[],'docstatus':[],'parent':[],'parentfield':[],
			'parenttype':[],'idx':[],'naming_series':[],'student':[],
			'student_name':[],'hostel_id':[],'start_date':[],'allotment_type':[],
			'end_date':[],'room_id':[],'room_type':[],'employee':[],'employee_name':[],'Room_No':[]
		})
		for t in range(len(Stu_info)):
			s=pd.Series([Stu_info[t][0],Stu_info[t][1],Stu_info[t][2],Stu_info[t][3],Stu_info[t][4],Stu_info[t][5],
						Stu_info[t][6],Stu_info[t][7],Stu_info[t][8],Stu_info[t][9],Stu_info[t][10],Stu_info[t][11],
						Stu_info[t][12],Stu_info[t][13],Stu_info[t][14],Stu_info[t][15],Stu_info[t][16],Stu_info[t][17],
						Stu_info[t][18]],
								index=['Al_no','creation','modified','modified_by',
										'owner','docstatus','idx','naming_series','student',
										'student_name','hostel_id','start_date','allotment_type',
										'end_date','room_id','room_type','employee','employee_name','Room_No'])
			df1=df1.append(s,ignore_index=True)	
		return df1
	elif flag=="Alloted_student":
		stu_info=frappe.db.sql("""SELECT `name`,`room_id` FROM `tabRoom Allotment` WHERE `room_id`="%s" and (`start_date`<=now() and `end_date`>=now())"""%(info))
		df1=pd.DataFrame({
			"Al_no":[],"room_id":[]
		})		
		for t in range(len(stu_info)):
			s=pd.Series([stu_info[t][0],stu_info[t][1]],
								index=["Al_no","room_id"])
			df1=df1.append(s,ignore_index=True)	
		return df1	




@frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
def hostel_req_query(doctype, txt, searchfield, start, page_len, filters):						
	# return frappe.db.sql(""" SELECT S.name,SA.name,SA.hostel_required,S.student_name
	# 						from `tabStudent Applicant` as SA
	# 						JOIN `tabStudent` S on S.student_applicant=SA.name 
	# 						where SA.hostel_required=1""") ##### Student Applicant
	############################## Search Field Code################# 
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join("S."+field + " like %(txt)s" for field in searchfields)

	data=frappe.db.sql(""" SELECT S.name,SHA.name,S.student_name from `tabStudent Hostel Admission` as SHA 
							JOIN `tabStudent` S on S.name=SHA.student 
							where (SHA.{key} like %(txt)s or {scond})  and 
	       					SHA.allotment_status="Not Reported" and SHA.docstatus=1 """.format(
								**{
									"key": searchfield,
									"scond": searchfields,
								}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})


	# return frappe.db.sql(""" SELECT S.name,SHA.name,S.title from `tabStudent Hostel Admission` as SHA 
	# 						JOIN `tabStudent` S on S.name=SHA.student 
	# 						where SHA.allotment_status="Not Reported" and SHA.docstatus=1 """)
	return data
						

@frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
def allotment(student):
	data=frappe.get_all("Student Hostel Admission",[["student","=",student],["allotment_status","!=","Allotted"],
					["allotment_status","!=","De-Allotted"],["docstatus","=",1]],['name','hostel'])
	if len(data)>0:
		return data[0]
			

@frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
def employee():
	user=frappe.session.user
	name=""
	if user == "Administrator":
		pass
	else:
		employee_name=frappe.get_all("Employee",fields=[["prefered_email","=",user]])
	if user == "Administrator":
		name=""
	else:
		if employee_name:
			name=employee_name[0]['name']
	if len(name)>0:
		return name
	
# Pop-up message Room Allotment Data in Student doctype
@frappe.whitelist()
def get(name=None, filters=None, parent=None):
    '''Returns a document by name or filters

    :param doctype: DocType of the document to be returned
    :param name: return document of this `name`
    :param filters: If name is not set, filter by these values and return the first match'''
    room_allotment_data=frappe.get_all("Room Allotment",filters=[["student","=",name],["start_date","<=",date.today()],["end_date",">=",date.today()]],
                                        fields=['name','hostel_registration_no','hostel_id','room_number','room_id','room_type','start_date','end_date'])
    if len(room_allotment_data)!=0:
       return room_allotment_data[0]
    else:
        return {}
