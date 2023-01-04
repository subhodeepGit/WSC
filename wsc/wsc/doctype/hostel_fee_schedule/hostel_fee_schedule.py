# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, money_in_words
from frappe.utils.background_jobs import enqueue

import erpnext


class HostelFeeSchedule(Document):
	global length
	
	def validate(self):
		self.calculate()
	def calculate(self):
		a=frappe.db.sql(""" Select RA.*,CED.*,RA.name as room_allotment  from `tabRoom Allotment` as RA
				Join `tabCurrent Educational Details` as CED on CED.parent=RA.Student
				where CED.programs="%s" and CED.semesters="%s" and CED.academic_term="%s" and CED.academic_year="%s" and (RA.room_type="%s" and RA.docstatus=1 and (RA.start_date <=now() and RA.end_date>=now()))
				"""%(self.programs,self.program,self.academic_term,self.academic_year,self.room_type),as_dict = True)
		length=len(a)  
		self.grand_total=self.total_amount*length
		self.grand_total_in_words = money_in_words(self.grand_total)

		
	def on_submit(self):
		pass	
	def onload(self):
		info = self.get_dashboard_info()
		self.set_onload('dashboard_info', info)

	def get_dashboard_info(self):
		info = {
			"total_paid": 0,
			"total_unpaid": 0,
			"currency": erpnext.get_company_currency(self.company)
		}

		fees_amount = frappe.db.sql("""select sum(grand_total), sum(outstanding_amount) from `tabHostel Fees`
			where hostel_fee_schedule=%s and docstatus=1""", (self.name))

		if fees_amount:
			info["total_paid"] = flt(fees_amount[0][0]) - flt(fees_amount[0][1])
			info["total_unpaid"] = flt(fees_amount[0][1])

		return info

	@frappe.whitelist()
	def create_fees(self):
		self.db_set("fee_creation_status", "In Process")
		frappe.publish_realtime("fee_schedule_progress",
			{"progress": "0", "reload": 1}, user=frappe.session.user)

		total_records = sum([int(d.idx) for d in self.student_room_alloted])
		if total_records > 100:
			frappe.msgprint('''Fee records will be created in the background.
				In case of any error the error message will be updated in the Schedule.''')
			enqueue(generate_fee, queue='default', timeout=6000, event='generate_fee',
				hostel_fee_schedule=self.name)
		else:
			generate_fee(self.name)

# Student fetch after clicking on Get Student button
@frappe.whitelist()
def get_students(self=None,academic_term=None, programs=None,program=None,academic_year=None,room_type=None,fee_structure=None):
	stud_info=frappe.db.sql(""" Select RA.*,CED.*,RA.name as room_allotment  from `tabRoom Allotment` as RA
	Join `tabCurrent Educational Details` as CED on CED.parent=RA.Student
	where CED.programs="%s" and CED.semesters="%s" and CED.academic_term="%s" and CED.academic_year="%s" and 
	(RA.room_type="%s" and RA.docstatus=1 and (RA.start_date <=now() and RA.end_date>=now()))
	"""%(programs,program,academic_term,academic_year,room_type),as_dict=True)


	alrdy_chrg = frappe.get_all("Fees",{"hostel_fee_structure":fee_structure,"docstatus":1},{"name","student"})
	stu_list=[]
	for t in alrdy_chrg:
		stu_list.append(t['student'])
	stu_list=list(set(stu_list))

	final_list_student=[]
	for t in stud_info:
		flag=0
		for j in stu_list:
			if t['parent']==j:
				flag=1
		if flag==0:
			final_list_student.append(t)
	print(final_list_student)
	if len(final_list_student)!=0:
		return final_list_student
	else:
		frappe.msgprint("No Student Found in Room Allotment")
		stud_info = []
		return stud_info

def generate_fee(hostel_fee_schedule):
	doc = frappe.get_doc("Hostel Fee Schedule", hostel_fee_schedule)
	error = False
	total_records = sum([int(d.idx) for d in doc.student_room_alloted])
	created_records = 0

	if not total_records:
		frappe.throw("Please click get student button")

	for d in doc.get("student_room_alloted"):
			try:
				fees = frappe.new_doc("Hostel Fees")
				fees.posting_date = doc.posting_date
				fees.due_date = doc.due_date
				fees.programs = doc.programs
				fees.program = doc.program
				fees.academic_year = doc.academic_year
				fees.academic_term = doc.academic_term
				fees.hostel_fee_structure = doc.fee_structure
				fees.cost_center = doc.cost_center
				fees.student = d.student
				fees.student_name = d.student_name
				fees.hostel_admission = d.hostel_registration_no
				fees.allotment_number = d.room_allotment_id
				fees.room_number = d.room_number
				fees.room_type = d.room_type
				fees.hostel = d.hostel_id
				fees.hostel_fee_schedule = hostel_fee_schedule
				ref_details = frappe.get_all("Fee Component",{"parent":doc.fee_structure},['fees_category','amount','receivable_account','income_account','company','grand_fee_amount','outstanding_fees'])
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
				created_records += 1
				frappe.publish_realtime("fee_schedule_progress", {"progress": str(int(created_records * 100/total_records))}, user=frappe.session.user)

			except Exception as e:
				error = True
				err_msg = frappe.local.message_log and "\n\n".join(frappe.local.message_log) or cstr(e)
	
	if error:
		frappe.db.rollback()
		frappe.db.set_value("Hostel Fee Schedule", hostel_fee_schedule, "fee_creation_status", "Failed")
		frappe.db.set_value("Hostel Fee Schedule", hostel_fee_schedule, "error_log", err_msg)

	else:
		frappe.db.set_value("Hostel Fee Schedule", hostel_fee_schedule, "fee_creation_status", "Successful")
		frappe.db.set_value("Hostel Fee Schedule", hostel_fee_schedule, "error_log", None)

	frappe.publish_realtime("fee_schedule_progress",
		{"progress": "100", "reload": 1}, user=frappe.session.user)