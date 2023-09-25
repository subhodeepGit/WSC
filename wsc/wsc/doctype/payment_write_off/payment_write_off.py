# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from six import iteritems, string_types
from frappe import _

class PaymentWriteOff(Document):
	def validate(doc):
		if int(doc.payment_write_off_amount) > doc.total_allocated_amount:
			frappe.throw("Payment Write Off Amount can not be greater than total allocated amount.")


@frappe.whitelist()
def get_student_details(args,self):
	# fees_info=frappe.db.get_all("Fees",filter,['name','posting_date'])
	semesters=[]
	for result in frappe.get_all("Fees",{"student":self.student},['name','program']):
		self.append("references",{
			"semesters":result.program
		})
	semesters.append(result.program)


@frappe.whitelist()
def get_outstanding_fees(args):
	print("Hello World")
	if isinstance(args, string_types):
		args = json.loads(args)
	filter=[]

	filter.append(["Student","=",args.get('student')])
	filter.append(['posting_date', 'between',[args.get('from_posting_date'),args.get('to_posting_date')]])
	filter.append(["outstanding_amount",">",0])	
	filter.append(["docstatus","=",1])

	if args.get('outstanding_amt_greater_than') > 0:
		filter.append(["outstanding_amount",">",args.get('outstanding_amt_greater_than')])
	if args.get('outstanding_amt_less_than') >0:
		filter.append(["outstanding_amount","<",args.get('outstanding_amt_less_than')])	
	if args.get('cost_center'):
		filter.append(['cost_center',"=",args.get('cost_center')])	
	
	if args.get('from_due_date') and args.get('to_due_date'):
		filter.append(['valid From','between',[args.get('from_due_date'),args.get('to_due_date')]])
		filter.append(['valid_to','between',[args.get('from_due_date'),args.get('to_due_date')]])
	fees_info=frappe.db.get_all("Fees",filter,['name','posting_date','program','fee_structure','hostel_fee_structure'],order_by="posting_date asc")
	fee_component_info=[]

	for t in fees_info:
		if t['fee_structure']!=None and t['hostel_fee_structure']==None:
			fee_component=frappe.db.get_all("Fee Component", {"parent":t['name']},
									["name","fees_category","outstanding_fees","receivable_account","income_account","outstanding_fees","amount","idx"],order_by="idx asc")					
			for j in fee_component:
				if j["outstanding_fees"]>0:	
					j['posting_date']=t['posting_date']
					j['Type']='Fees'
					j['program']=t['program']
					j['reference_name']=t['name']
					j['exchange_rate']=1
					fee_component_info.append(j)

	for t in fees_info:
		# if (t['fee_structure']==None or t['fee_structure']=="") and (t['hostel_fee_structure']!=None or t['hostel_fee_structure']!=""):
		if t['fee_structure']==None and t['hostel_fee_structure']!=None:
			fee_component=frappe.db.get_all("Fee Component", {"parent":t['name']},
									["name","fees_category","outstanding_fees","receivable_account","income_account","outstanding_fees","amount","idx"],order_by="idx asc")
			for j in fee_component:
				if j["outstanding_fees"]>0:	
					j['posting_date']=t['posting_date']
					j['Type']='Fees'
					j['program']=t['program']
					j['reference_name']=t['name']
					j['exchange_rate']=1
					fee_component_info.append(j)
	for t in fees_info:
		# if (t['fee_structure']==None or t['fee_structure']=="") and (t['hostel_fee_structure']==None or t['hostel_fee_structure']==""):
		if t['fee_structure']==None and t['hostel_fee_structure']==None:
			fee_component=frappe.db.get_all("Fee Component", {"parent":t['name']},
									["name","fees_category","outstanding_fees","receivable_account","income_account","outstanding_fees","amount","idx"],order_by="idx asc")
			for j in fee_component:
				if j["outstanding_fees"]>0:	
					j['posting_date']=t['posting_date']
					j['Type']='Fees'
					j['program']=t['program']
					j['reference_name']=t['name']
					j['exchange_rate']=1
					fee_component_info.append(j)

	data=fee_component_info	
	if not data:
		frappe.msgprint(_("No outstanding invoices found for the {0} {1} which qualify the filters you have specified.")
			.format(_(args.get("party_type")).lower(), frappe.bold(args.get("party"))))

	return data


