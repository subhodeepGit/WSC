# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AutoRollNoGenerator(Document):
	def validate(self):
		mylist=[]
		for t in self.get('student_list'):
			mylist.append(t.roll_no)

		myset = set(mylist)
		if len(mylist) != len(myset):
			frappe.throw("<b>Duplicates Roll No </b> found in the list")

	def on_submit(self):
		for t in self.get('student_list'):
			doc=frappe.get_doc("Program Enrollment",t.course_enrollment)
			doc.roll_no=t.roll_no
			doc.save()

	def on_cancel(self):
		for t in self.get('student_list'):
			doc=frappe.get_doc("Program Enrollment",t.course_enrollment)
			doc.roll_no=""
			doc.save()

@frappe.whitelist()
def get_student(course_type=None,programs=None,semester=None,academic_year=None,
		academic_term=None,course_code=None,year_code=None,branch_code=None):
	if course_type!=None and programs!=None and semester!=None and academic_year!=None and \
		academic_term!=None and course_code!=None and year_code!=None and branch_code!=None:
		program_enrollment_data=frappe.get_all("Program Enrollment",{"program_grade":course_type,"programs":programs,"program":semester,
							       				"academic_year":academic_year,"academic_term":academic_term,"admission_status":"Admitted","docstatus":1},
												['name','student','student_name'])
		flag=1
		for t in program_enrollment_data:
			id_no=str(flag)
			if len(id_no)==1:
				id_no="000"+id_no
			elif len(id_no)==2:
				id_no="00"+id_no
			elif len(id_no)==3:
				id_no="0"+id_no		
			else:
				id_no=id_no
			roll_no=course_code+year_code+branch_code+id_no
			t.update({"roll_no":roll_no})	
			flag+=1
		return program_enrollment_data
	
	# a=[1,2,3,4,5,6,7,8,100,10,1200]
	# branch_code="01"
	# year="21"
	# batch="05"
	# for t in a:
	# 	id_no=t
	# 	id_no=str(id_no)
	# 	if len(id_no)==1:
	# 		id_no="000"+id_no
	# 	elif len(id_no)==2:
	# 		id_no="00"+id_no
	# 	elif len(id_no)==3:
	# 		id_no="0"+id_no
	# 	else:
	# 		id_no=id_no
	# 	roll_no=branch_code+year+batch+id_no		
