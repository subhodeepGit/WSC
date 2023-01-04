# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaterialDistribution(Document):
	# @frappe.whitelist()
	def validate(doc):
		allotment_number=doc.allotment_number
		info=frappe.db.sql("""SELECT `name`,`allotment_number`,`docstatus` FROM `tabMaterial Distribution` WHERE `allotment_number`="%s" and `docstatus`!=2"""%\
							(allotment_number))				
		if len(info)==0:
			pass
		elif len(info)==1 and info[0][2]==0:
			pass
		else:
			frappe.throw("Material already provided to the Student")


