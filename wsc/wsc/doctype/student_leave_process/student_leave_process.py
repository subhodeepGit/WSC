# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd
import datetime

class StudentLeaveProcess(Document):
	def validate(doc):
		Al_no=doc.allotment_number
		ST_date=pd.to_datetime(doc.start_date).date()
		ED_date=pd.to_datetime(doc.end_date).date()
		workflow_state=doc.workflow_state
		# Leave_process_info=frappe.get_doc("Studnet Leave Process",filters={"allotment_number": "RA-2021-00001"})
		# Leave_process_info[0].name
		St_leave_info=frappe.db.sql(""" SELECT `name`,`allotment_number`,`student`,`student_name`,`hostel`,`room_number`,`room_type`,`start_date`, 
										`end_date`,`status`,`workflow_state` from `tabStudent Leave Process` WHERE `allotment_number`="%s" """%(Al_no))							
		St_leave_df=pd.DataFrame({
			'Leave_doc_no':[],'allotment_number':[],'student':[],'student_name':[],'hostel':[],'room_number':[],'room_type':[],'start_date':[],
			'end_date':[],'status':[],'workflow_state':[]
		})								
		for t in range(len(St_leave_info)):
			s=pd.Series([St_leave_info[t][0],St_leave_info[t][1],St_leave_info[t][2],St_leave_info[t][3],St_leave_info[t][4],St_leave_info[t][5],
						St_leave_info[t][6],St_leave_info[t][7],St_leave_info[t][8],St_leave_info[t][9],St_leave_info[t][10]],
								index=['Leave_doc_no','allotment_number','student','student_name','hostel','room_number','room_type','start_date',
										'end_date','status','workflow_state'])
			St_leave_df=St_leave_df.append(s,ignore_index=True)	
		St_leave_df=St_leave_df[(St_leave_df['workflow_state']!="Approved")|(St_leave_df['workflow_state']!="Withdrawl of Application")|
								(St_leave_df['workflow_state']!="Rejected")|(St_leave_df['workflow_state']!="Approve By Hostel Warden")].reset_index()							
		if workflow_state=="Submit":
			# St_leave_df=St_leave_df[(St_leave_df['status']=="Open")|(St_leave_df['status'].isnull())]
			# if len(St_leave_df)!=0:
			# 		frappe.throw("Document already Present Dco no %s"%(St_leave_df['Leave_doc_no'][0]))
			# else:
				if ST_date<=ED_date and (ST_date>=datetime.date.today()):
					pass
				else:
					frappe.throw("Please check Start Date and End Date of Leave")	

		

	