# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import re
import frappe
from frappe.model.document import Document
import pandas as pd
from datetime import datetime

class HostelClearance(Document):
	# @frappe.whitelist()
	def before_save(doc):
		#doc status-0
		allotment_number=doc.allotment_number
		due_status=doc.due_status
		due_amount=doc.due_amount
		reason_of_due=doc.reason_of_due
		info=""" WHERE `allotment_number`="%s" and (`docstatus`!=1 and `docstatus`!=2) """%(allotment_number)
		HC_info=hostel_cle_df("Genaral",info)
		print("\n\n\n")
		print(HC_info)
		if len(HC_info)==0:
			if due_status=="Dues":
				if due_amount!=None and reason_of_due!=None:
					pass
				else:
					frappe.throw("Due amount or Reason of Due")
			else:
				pass
		else:
			frappe.throw("Document is already present in Doc no %s"%(HC_info["HC_doc_no"][0]))	


			
	# @frappe.whitelist()	
	def on_submit(doc):
		#doc status-1
		Hol_cle_doc_no=doc.name
		allotment_number=doc.allotment_number
		due_status=doc.due_status
		type_of_clearance=doc.type_of_clearance
		end_date=doc.end_date
		end_date=datetime.strptime(end_date,"%Y-%m-%d").date()
		due_amount=doc.due_amount
		reason_of_due=doc.reason_of_due
		if due_status=="Dues":
			if due_amount!=None and reason_of_due!=None:
				info=""" where `name`="%s" """%(allotment_number)
				Al_df=hostel_cle_df("Room_al_genaral",info)
				if end_date<=Al_df['end_date'][0]:
					frappe.db.sql(""" UPDATE `tabRoom Allotment` SET `end_date`="%s",`allotment_type`="%s" WHERE `name`="%s" """%\
								(end_date,type_of_clearance,allotment_number))
					room_id=doc.room_number			
					frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(room_id))
					status=frappe.get_all("Room Allotment",{"name":doc.student},['hostel_registration_no'])
					frappe.db.set_value("Student Hostel Admission",status[0]['hostel_registration_no'], "allotment_status", "Deallotted") 				
					pass
				else:
					frappe.throw("Kindly check the End Date")
			else:
				frappe.throw("Due amount or Reason of Due")
		else:
			info=""" where `name`="%s" """%(allotment_number)
			Al_df=hostel_cle_df("Room_al_genaral",info)
			if end_date<=Al_df['end_date'][0]:
				frappe.db.sql(""" UPDATE `tabRoom Allotment` SET `end_date`="%s",`allotment_type`="%s" WHERE `name`="%s" """%\
								(end_date,type_of_clearance,allotment_number))
				room_id=doc.room_number			
				frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(room_id))
				status=frappe.get_all("Room Allotment",{"name":doc.allotment_number},['hostel_registration_no'])
				frappe.db.set_value("Student Hostel Admission",status[0]['hostel_registration_no'], "allotment_status", "Deallotted") 						
				pass
			else:
				frappe.throw("Kindly check the End Date")




	# @frappe.whitelist()		
	def on_cancel(doc):
		#doc status-2
		allotment_number=doc.allotment_number
		frappe.db.sql(""" UPDATE `tabRoom Allotment` SET `end_date`="9999-12-01",`allotment_type`="Allotted" WHERE `name`="%s" """%\
								(allotment_number))
		room_id=doc.room_number			
		frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`-1 WHERE `name`="%s" """%(room_id))
		status=frappe.get_all("Room Allotment",{"name":doc.allotment_number},['hostel_registration_no'])
		frappe.db.set_value("Student Hostel Admission",status[0]['hostel_registration_no'], "allotment_status", "Deallotted") 							
		pass









def hostel_cle_df(flag,info):
	if flag=="Genaral":
		HC_info=frappe.db.sql("""SELECT `name`,`allotment_number`,`student`,`student_name`,`hostel`,`room_number`,`end_date`,
		`type_of_clearance`,`due_status`,`due_amount`,`reason_of_due`,`docstatus` from `tabHostel Clearance`  """+info)
		df1=pd.DataFrame({
			"HC_doc_no":[],"allotment_number":[],"student":[],"student_name":[],"hostel":[],"room_number":[],"end_date":[],
			"type_of_clearance":[],"due_status":[],"due_amount":[],"reason_of_due":[],"docstatus":[]
	
		})
		for t in range(len(HC_info)):
			s=pd.Series([HC_info[t][0],HC_info[t][1],HC_info[t][2],HC_info[t][3],HC_info[t][4],HC_info[t][5],
						HC_info[t][6],HC_info[t][7],HC_info[t][8],HC_info[t][9],HC_info[t][10],HC_info[t][11]],
								index=["HC_doc_no","allotment_number","student","student_name","hostel","room_number","end_date",
										"type_of_clearance","due_status","due_amount","reason_of_due","docstatus"])
			df1=df1.append(s,ignore_index=True)		
		return df1
	elif flag=="Room_al_genaral":
		RA_info=frappe.db.sql("""SELECT `name`,`student`,`start_date`,`end_date` FROM `tabRoom Allotment` """+info)
		df1=pd.DataFrame({
			"Al_no":[],"student":[],"start_date":[],"end_date":[]
		})
		for t in range(len(RA_info)):
			s=pd.Series([RA_info[t][0],RA_info[t][1],RA_info[t][2],RA_info[t][3]],index=["Al_no","student","start_date","end_date"])
			df1=df1.append(s,ignore_index=True)
		return df1	