# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.translate import import_translations
import pandas as pd

class WithdrawalofInwardSuspensionLetter(Document):
	# @frappe.whitelist()
	def before_insert(doc):
		inward_suspension_letter_id=doc.inward_suspension_letter_id
		info=frappe.db.sql("""SELECT * FROM `tabWithdrawal of Inward Suspension Letter` where `inward_suspension_letter_id`="%s" """%(inward_suspension_letter_id))
		if len(info)==0:
			pass
		else:
			frappe.throw("Alredy Document is Closed")

	# @frappe.whitelist()
	def on_submit(doc):
		icr_id = doc.name
		icr = frappe.get_doc("Withdrawal of Inward Suspension Letter",icr_id)
		stu_df = pd.DataFrame({
				'Al_no':[]
			})	
		for al in icr.student_fetch:
			s = pd.Series([al.allotment_number],index = ['Al_no'])
			stu_df = stu_df.append(s,ignore_index = True)
			print(stu_df)
		for t in range(len(stu_df)):	
			frappe.db.sql("""UPDATE `tabRoom Allotment` SET `allotment_type`="Allotted" WHERE `name`="%s" """%(stu_df['Al_no'][t]))
		pass



		
    