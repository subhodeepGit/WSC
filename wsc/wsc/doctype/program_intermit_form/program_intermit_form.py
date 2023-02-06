# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProgramIntermitForm(Document):
	pass

# frappe.whitelist()
# def getdetails(student_id):
# 	data =frappe.get_all("Current Educational Details",{'parent':student_id},["academic_year","academic_term","programs","semesters"])
# 	return data[0]
# 	# if len(data) == 0:
# 	# 	# frappe.throw("Student is not enrolled in Any program")
# 	# 	return 0
# 	# else :
# 	# 	print(data[0])
# 	# 	return data[0]

@frappe.whitelist()
def get_student_details(student_id):
	data = frappe.get_all("Current Educational Details",{'parent':student_id},["academic_year","academic_term","programs","semesters"])
	print()
	if data == None or len(data)==0:
		return 0 
	else :
		return data[0]

