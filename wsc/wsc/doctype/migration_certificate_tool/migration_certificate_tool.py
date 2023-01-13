# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from pytz import all_timezones, country_names
from frappe.utils.data import nowtime
from frappe.utils.background_jobs import enqueue
from frappe.utils import cint, flt, cstr
from frappe import _

class MigrationCertificateTool(Document):
	pass
	@frappe.whitelist()
	def make_exam_assessment_result(self):
		print("\n\n\n\nmake_exam_assessment_result")
		self.db_set("certificate_creation_status", "In Process")
		frappe.publish_realtime("migration_certificate_tool_progress",
			{"progress": "0", "reload": 1}, user=frappe.session.user)

		total_records = len(self.get("migration_certificate_student"))
		if total_records > 10:
			frappe.msgprint(_(''' Records will be created in the background.
				In case of any error the error message will be updated in the Schedule.'''))
			enqueue(create_migration_certificate, queue='default', timeout=6000, event='create_migration_certificate',
				migration_certificate_tool=self.name)

		else:
			create_migration_certificate(self.name)
def create_migration_certificate(migration_certificate_tool):
	print("migration_certificate_tool",migration_certificate_tool)
	doc = frappe.get_doc("Migration Certificate Tool", migration_certificate_tool)
	error = False
	total_records = len(doc.get("migration_certificate_student"))
	created_records = 0
	if not total_records:
		frappe.throw(_("Please setup Students under Student Groups"))
	# result=frappe.new_doc("Provisional Certificate")
	
	# for d in doc.get("provisional_certificate_student"):
	# 	if d.completion_status=="Pending":
	# 		frappe.throw("#Row {0} Completion Status Should be <b>Completed</b>".format(d.idx))
	for d in doc.get("migration_certificate_student"):
		# try:
		result=frappe.new_doc("Migration Certificate")
		result.student=d.student
		result.student_name=d.student_name
		result.roll_no=d.roll_no
		result.permanant_registration_number=d.registration_number
		
		for enroll in frappe.get_all("Program Enrollment",{"student":d.student,"docstatus":1,"academic_term":doc.academic_term},['programs','academic_term','academic_year'],order_by="creation desc",limit=1):
			result.programs=enroll.programs
			result.academic_term=enroll.academic_term
			result.academic_year=enroll.academic_year
		for enroll in frappe.get_all("Program Enrollment",{"student":d.student,"docstatus":1,"academic_term":doc.academic_term},['programs','academic_term','academic_year'],order_by="creation desc",limit=1):
			result.programs=enroll.programs
			result.academic_term=enroll.academic_term
			result.academic_year=enroll.academic_year
		result.resistrar_signature=doc.resistrar_signature
		result.acadmic_session=doc.academic_session 
		# result.place=d.place 
		result.place=doc.place
		# result.academic_year=doc.academic_year
		result.save()
		created_records += 1
	frappe.msgprint("Record Created")
	frappe.publish_realtime("migration_certificate_tool_progress", {"progress": str(int(created_records * 100/total_records)),"current":str(created_records),"total":str(total_records)}, user=frappe.session.user)
	frappe.db.set_value("Migration Certificate Tool", migration_certificate_tool, "certificate_creation_status", "Successful")
	frappe.publish_realtime("migration_certificate_tool_progress",
	{"progress": "100", "reload": 1}, user=frappe.session.user)
@frappe.whitelist()
def get_students(academic_term=None, programs=None):
    enrolled_students = get_program_enrollment(academic_term,programs)
    if enrolled_students:
        student_list = []
        for s in enrolled_students:
            if frappe.db.get_value("Student", s.student, "enabled"):
                s.update({"active": 1})
            else:
                s.update({"active": 0})
            student_list.append(s)
        return student_list
    else:
        frappe.msgprint("No students found")
        return []
def get_program_enrollment(academic_term,programs=None):
    condition1 = " "
    condition2 = " "
    if programs:
        condition1 += " and pe.programs = %(programs)s"
    
    return frappe.db.sql('''
        select
            pe.student, pe.student_name
        from
            `tabProgram Enrollment` pe {condition2}
        where
            pe.academic_term = %(academic_term)s  {condition1}
        order by
            pe.student_name asc
        '''.format(condition1=condition1, condition2=condition2),
                ({"academic_term": academic_term,"programs": programs}), as_dict=1)
