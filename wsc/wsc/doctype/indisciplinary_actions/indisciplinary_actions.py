# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import re
from time import process_time
import frappe
from frappe.model.document import Document
import pandas as pd

class IndisciplinaryActions(Document):
	# @frappe.whitelist()
	def on_update(doc):
		#doc status-0
		type_of_decision=doc.type_of_decision
		if type_of_decision=="Warning Letter":
			date_of_letter=doc.date_of_letter
			attachment_of_warnning_letter=doc.attachment_of_warnning_letter

			if date_of_letter!=None and attachment_of_warnning_letter!=None:
				pass
			else:
				frappe.throw("Kindly provide 'Date of Letter Issue' and 'Attach the Warning Letter'")
		elif type_of_decision=="Fine Letter":
			issue_of_letter=doc.issue_of_letter
			attachment_of_fine_letter=doc.attachment_of_fine_letter
			fine_amount=doc.fine_amount
			if issue_of_letter!=None and attachment_of_fine_letter!=None and fine_amount!=None:
				pass
			else:
				frappe.throw("Kindly provide 'Date of Letter Issue' and 'Fine Letter'")		
		elif type_of_decision=="Suspension Letter":
			issue_of_suspension_letter=doc.issue_of_suspension_letter
			attachment_of_suspention_letter=doc.attachment_of_suspention_letter
			type_of_suspension=doc.type_of_suspension
			if type_of_suspension!="":
				if attachment_of_suspention_letter!=None and attachment_of_suspention_letter!=None:
					indisciplinary_complaint_registration_id=doc.indisciplinary_complaint_registration_id
					info=frappe.db.sql("""SELECT `allotment_number` from `tabIndisciplinary Complaint Registration Student` WHERE `parent`="%s" """%\
													(indisciplinary_complaint_registration_id))						
					for t in range(len(info)):
						frappe.db.sql("""UPDATE `tabRoom Allotment` SET `allotment_type`="%s" WHERE `name`="%s" """%(type_of_suspension,info[t][0]))							
					pass
				else:
					frappe.throw("Kindly provide 'Date of Letter Issue' and 'Suspension Letter'")
			else:
				frappe.throw("Suspention Type Not Selected")		
		elif type_of_decision=="Debar Letter":
			issue_of_debar_letter=doc.issue_of_debar_letter
			attachment_of_debar_letter=doc.attachment_of_debar_letter
			if issue_of_debar_letter!=None and attachment_of_debar_letter: 
				indisciplinary_complaint_registration_id=doc.indisciplinary_complaint_registration_id
				info=frappe.db.sql("""SELECT IND.allotment_number, RA.room_id from `tabIndisciplinary Complaint Registration Student` as IND JOIN `tabRoom Allotment` RA on IND.allotment_number=RA.name WHERE IND.parent="%s" """%\
										(indisciplinary_complaint_registration_id))								
				type_of_suspension="Debar"													
				for t in range(len(info)):
					frappe.db.sql("""UPDATE `tabRoom Allotment` SET `allotment_type`="%s",`end_date`="%s" WHERE `name`="%s" """%\
										(type_of_suspension,issue_of_debar_letter,info[t][0]))
					room_id=info[t][1]
					frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(room_id))					
				pass
			else:
				frappe.throw("Kindly provide 'Date of Letter Issue' and 'Debar Letter'")
		elif type_of_decision=="Parents Call Letter":
			Doc_no=doc.name
			issue_of_parents_call_letter=doc.issue_of_parents_call_letter
			attachment_of_parents_call_letter=doc.attachment_of_parents_call_letter
			parents_meeting_date=doc.parents_meeting_date
			parents_undertaking=doc.parents_undertaking
			if (issue_of_parents_call_letter!=None and attachment_of_parents_call_letter!=None) and (parents_meeting_date==None and parents_undertaking==None):
				pass
			elif (parents_meeting_date!=None and parents_undertaking!=None) and (issue_of_parents_call_letter!=None and attachment_of_parents_call_letter!=None):
				pass
			else:
					frappe.throw("1st step Letter has to issue and 2nd step parents reporting has to be issued")		
		elif type_of_decision=="Disciplinary Committee":
			ia_id = doc.name
			in_doc_info=frappe.db.sql("""SELECT * FROM `tabIndisciplinary Actions` where  name="%s" """%(ia_id))
			if len(in_doc_info)!=0:
				ia = frappe.get_doc("Indisciplinary Actions",ia_id)
				emp_df = pd.DataFrame({
					'Emp_no':[]
				})
				for al in ia.dc_member:
					s = pd.Series([al.emp_id],index = ['Emp_no'])
					emp_df = emp_df.append(s,ignore_index = True)
				if 	len(emp_df)!=0:
					duplicate = emp_df[emp_df.duplicated()].reset_index()
					if len(duplicate) == 0:
						issue_of_debar_letter=doc.issue_of_dc_letter
						attachment_of_dc_letter=doc.attachment_of_dc_letter
						if issue_of_debar_letter!=None and attachment_of_dc_letter!=None:
							pass
						else:
							frappe.throw("DC Letter and Date of Issue is not Maintained")
					else:
						b=""
						for t in range(len(duplicate)):
							a="%s  "%(duplicate['Emp_no'][t])
							b=b+a
						frappe.throw("Duplicate value found on Employee ID "+b)
				else:
					frappe.throw("No Disciplinary Committee Maintained")		
			else:
				pass	
		else:
			frappe.throw("No field selected")


	# @frappe.whitelist()
	def on_cancel(doc):
		type_of_decision=doc.type_of_decision
		if type_of_decision=="Suspension Letter":
			indisciplinary_complaint_registration_id=doc.indisciplinary_complaint_registration_id
			info=frappe.db.sql("""SELECT `allotment_number` from `tabIndisciplinary Complaint Registration Student` WHERE `parent`="%s" """%\
													(indisciplinary_complaint_registration_id))						
			for t in range(len(info)):
				frappe.db.sql("""UPDATE `tabRoom Allotment` SET `allotment_type`="%s" WHERE `name`="%s" """%("Allotted",info[t][0]))							
			pass
		elif type_of_decision=="Debar Letter":
			indisciplinary_complaint_registration_id=doc.indisciplinary_complaint_registration_id
			info=frappe.db.sql("""SELECT IND.allotment_number, RA.room_id from `tabIndisciplinary Complaint Registration Student` as IND JOIN `tabRoom Allotment` RA on IND.allotment_number=RA.name WHERE IND.parent="%s" """%\
												(indisciplinary_complaint_registration_id))													
			for t in range(len(info)):
				frappe.db.sql("""UPDATE `tabRoom Allotment` SET `allotment_type`="%s",`end_date`="%s" WHERE `name`="%s" """%\
										("Allotted","9999-12-01",info[t][0]))
				room_id=info[t][1]
				frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`-1 WHERE `name`="%s" """%(room_id))							
			pass
		else:
			pass	

	

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def status_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		SELECT `name` FROM `tabIndisciplinary Complaint Registration` WHERE `status` = "Open"
	"""
	)