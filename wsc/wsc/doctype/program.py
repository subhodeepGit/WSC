import frappe
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions

# from wsc.wsc.utils import duplicate_row_validation

def validate(doc,method):
    
	validate_course(doc)
	# create_permissions(doc)
	# create_program_permissions(doc)
    
	# duplicate_row_validation(doc, "courses", ['course', 'course_name'])
	
    

def on_trash(doc,method):
    validate_course_if_exists(doc)

def validate_course(doc):
    pass
#this code is for director
# def create_program_permissions(doc):
# 	for programs_semester in frappe.get_all("Department",{"name":doc.department},['name']):
# 		print("departmentSemester")
# 		print(programs_semester)
# 		for instru_programs in frappe.get_all("Program",{"department":programs_semester.name},['name','department']):
# 			print("\n\ninstru_programs")
# 			print(instru_programs)
# 		for ninstr_program in frappe.get_all("Instructor",{"department":instru_programs.department},['department','employee']):
# 			print("\n\ninstr_program")
# 			print(ninstr_program)
# 			for emp in frappe.get_all("Employee",{"name":ninstr_program.employee},['user_id','department']):
# 				# print("\n\nemployee_program")
# 				# print(emp)
# 				if emp.user_id:
# 					add_user_permission(doc.doctype,doc.name,emp.user_id,doc)
# 	for c in doc.courses:
# 		if c.course:
# 			if c.course not in [d.name for d in frappe.get_all("Course", {"disable":0},['name'])]:
# 				frappe.throw("Course <b>'{0}'</b> not valid".format(c.course))
# this code is for instructor
# def create_permissions(doc):
# 	for instr_log_program in frappe.get_all("Instructor Log",{"program":doc.name},['department','program','parent']):
# 		print("\n\instr_log_program")
# 		print(instr_log_program)
# 		for ninstr_program in frappe.get_all("Instructor",{"name":instr_log_program.parent},['department','name','employee']):
# 			print("\n\ninstr_program")
# 			print(ninstr_program)
# 			for emp in frappe.get_all("Employee",{"name":ninstr_program.employee},['user_id','department']):
# 				print("\n\nemployee_program")
# 				print(emp)
# 				if emp.user_id:
# 					add_user_permission(doc.doctype,doc.name,emp.user_id,doc)
def after_insert(doc,method):
    if doc.get("programs"):
        programs=frappe.get_doc("Programs",doc.get("programs"))
        if doc.program_name not in [d.semesters for d in programs.get("semesters")]:
            programs.append("semesters",{
                "semesters":doc.name,
                "semesters_name":doc.program_name
            })
            programs.no_of_semesters=len(programs.semesters)
            programs.save()

def validate_course_if_exists(doc):
    if len(doc.get("courses"))!=0:
        frappe.throw("Please Delete Courses from Semester")