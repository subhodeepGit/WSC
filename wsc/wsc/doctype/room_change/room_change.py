# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd

class RoomChange(Document):
	# @frappe.whitelist()
	def validate(doc):
		Al_no=doc.allotment_number
		preferred_hostel=doc.preferred_hostel
		preferred_room=doc.preferred_room
		preferred_room_type=doc.preferred_room_type
		workflow_state=doc.workflow_state
		Room_change_info=frappe.db.sql("""SELECT `name`,`allotment_number`,`student`,`student_name`,`hostel`,`room_number`,`room_type`,
		`preferred_hostel`,`preferred_room`,`preferred_room_type`,`workflow_state`,`application_status` 
		FROM `tabRoom Change` WHERE `allotment_number`="%s" """%(Al_no))
		
		Room_change_df=pd.DataFrame({
			'Room_doc_no':[],'allotment_number':[],'student':[],'student_name':[],
			'Pre_hostel':[],'Pre_room_no':[],'Pre_room_type':[],'preferred_hostel':[],
			'preferred_room':[],'preferred_room_type':[],'workflow_state':[],'application_status':[]
		})
		for t in range(len(Room_change_info)):
			s=pd.Series([Room_change_info[t][0],Room_change_info[t][1],Room_change_info[t][2],Room_change_info[t][3],Room_change_info[t][4],Room_change_info[t][5],
						Room_change_info[t][6],Room_change_info[t][7],Room_change_info[t][8],Room_change_info[t][9],Room_change_info[t][10],Room_change_info[t][11]],
								index=['Room_doc_no','allotment_number','student','student_name',
										'Pre_hostel','Pre_room_no','Pre_room_type','preferred_hostel',
										'preferred_room','preferred_room_type','workflow_state','application_status'])
			Room_change_df=Room_change_df.append(s,ignore_index=True)	

		chk_df=Room_change_df[(Room_change_df['workflow_state']!="Withdrawl")|(Room_change_df['workflow_state']!="Reject")|(Room_change_df['workflow_state']!="Reported")].reset_index()
		if workflow_state=="Submit":
			chk_df=chk_df[(chk_df['application_status'].isnull())|(chk_df['application_status']=="Open")].reset_index()
			if len(chk_df)!=0:
				frappe.throw("Document already present Doc no %s"%(chk_df['Room_doc_no'][0]))

		elif workflow_state=="Reported":
			if preferred_hostel == None or  preferred_room == None:
				frappe.throw("Please provide Hostel and Room number")
			else:
				if preferred_room != chk_df["Pre_room_no"][0]:
					Room_no_info=frappe.db.sql("""Select `room_number` from `tabRoom Masters` WHERE `name`="%s" """%(preferred_room))
					Room_no_info=Room_no_info[0][0]
					frappe.db.sql("""UPDATE `tabRoom Allotment` SET `hostel_id`="%s",`room_id`="%s",
						`room_type`="%s",`room_number`="%s" WHERE `name`="%s" """%(preferred_hostel,preferred_room,preferred_room_type,Room_no_info,Al_no))
					room_id=preferred_room
					frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`-1 WHERE `name`="%s" """%(room_id))
					room_id=doc.room_number
					frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(room_id))

				else:
					frappe.throw("Preferred room number and Present room number are same")


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):
	Emp_al=""
	if frappe.session.user == "Administrator":
		info=""
	else:
		User=frappe.session.user
		emp_id=frappe.get_all("Employee",{"user_id":User},["name"])
		if emp_id:
			Emp_al=frappe.db.sql("""
					SELECT `hostel_masters` from `tabEmployee Hostel Allotment` WHERE employees="%s" and
					(`start_date`<=now() and `end_date`>=now())"""%(emp_id[0]['name']))
		if Emp_al:	
			if len(Emp_al)==1:			
				info="""and hostel_id="%s" """%(Emp_al[0][0])
			else:
				hostel=[]
				for t in Emp_al:
					for i in t:
						hostel.append(i)
				hostel=str(tuple(hostel))	
				info="""and hostel_id in """+hostel
		else:
			frappe.throw("No Employee is allotted to the hostel")				
	############################## Search Field Code################# 	
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)	

	data=frappe.db.sql("""
		SELECT `name`,`student`,`student_name`,`hostel_id` FROM `tabRoom Allotment` WHERE ({key} like %(txt)s or {scond})  and
		    (`start_date` <= now() AND `end_date` >= now()) 
		and (`allotment_type`!="Hostel suspension" and `allotment_type`!="Suspension" and `allotment_type`!="Debar" and 
		`allotment_type`!="University Suspension" and `allotment_type`!="School Suspension" and `allotment_type`!="Death" and `allotment_type`!="De-Allotted") and `docstatus`=1 {info}
	""".format(
		**{
			"key": searchfield,
			"scond": searchfields,
			"info":info
		}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return data	

@frappe.whitelist()
def get_allotment_data(allotment_number):
	if allotment_number:
		for d in frappe.get_all("Room Allotment",{'name':allotment_number},['student','student_name','roll_no','registration_number','hostel_id','room_id','room_type','room_number']):
			return d

