import json
import frappe
import json
from frappe import _
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions


def validate(doc, method):
    validate_semester(doc)
    validate_max_credit(doc)
    calculate_total(doc)
    # create_permissions(doc)s
    validate_weightage_percentage(doc)

def create_permissions(doc):
	for instuctor_log in frappe.get_all("Instructor Log",{"course":doc.name},['course','parent']):
		for instr in frappe.get_all("Instructor",{"name":instuctor_log.parent},['department','name','employee']):
			for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id','department']):
				if emp.user_id:
					add_user_permission(doc.doctype,doc.name,emp.user_id,doc)	

def validate_semester(doc):
    if  doc.program and doc.programs:
        if doc.program not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('programs')},['semesters'])]:
            frappe.throw("Semester <b>'{0}'</b> not belongs to program <b>'{1}'</b>".format(doc.get('program'), doc.get('programs')))

def validate_max_credit(doc):
    total_credit = 0
    if doc.total_credit:
        for cd in doc.credit_distribution:
           if cd.passing_marks > cd.total_marks:
               frappe.throw("Passing marks <b>{0}</b> should not be greater than total marks <b>{1}</b>.".format(cd.passing_marks, cd.total_marks))
           if cd.passing_credits > cd.credits:
               frappe.throw("Passing credits <b>{0}</b> should not be greater than total credits <b>{1}</b>.".format(cd.passing_credits, cd.credits))
           total_credit += cd.credits
        doc.total_credit = total_credit
        if doc.total_credit != total_credit:
            frappe.throw("Credit totals <b>{0}</b> should be match with total credit <b>{1}</b>.".format(total_credit, doc.total_credit))



def validate_weightage_percentage(doc):
	total_weightage=0
	for cr in doc.get("credit_distribution"):
		total_weightage+=cr.weightage
	
	if len(doc.get("credit_distribution")) and total_weightage!=100:
		frappe.throw("Total Weightage should be 100%")

@frappe.whitelist()
def get_semesters(doctype, txt, searchfield, start, page_len, filters):
	data = frappe.db.sql("""SELECT semesters from tabSemesters 
		where parent = '{0}'""".format(filters.get("programs")))
	return data 

def validate_credit(doc):
	if doc.total_distribution and doc.maximum_credit:
		if doc.total_distribution > doc.maximum_credit:
			frappe.throw("<b>Total Distribution</b> Must Be Less Than Or Equal To <b>Maximum Credit</b>")

def calculate_total(doc):
	passing_marks=total_credit=passing_credit=weightage_per=0
	for cr in doc.get("credit_distribution"):
		weightage_per+=cr.weightage
		passing_marks+=cr.passing_marks
		total_credit+=cr.credits
		passing_credit+=cr.passing_credits
	# if weightage_per!=100:
	# 	frappe.throw("Please Fill Credit Distribution Below")
	doc.passing_marks=passing_marks
	doc.total_credit=total_credit
	doc.passing_credit=passing_credit
	
	for d in doc.get("topics"):
		print("\n\n\nHELLO",d.practical)
		d.total_hrs = d.theory + d.practical

@frappe.whitelist()
def add_module_to_tot_course(course, programs,is_tot,is_short_term_course):
	semesters = json.loads(programs)
	for entry in semesters:
		programs = frappe.get_doc('Programs',{'is_short_term_course':"Yes",'is_tot':is_tot}, entry)
		programs.append('courses', {
			'course': course,
			'course_name': frappe.db.get_value("Course",{'name':course,'is_short_term_course':"Yes",'is_tot':is_tot},"course_name"),
		})
		program = frappe.get_doc('Program', entry)
		program.append('courses', {
			'course': course,
			'course_name': frappe.db.get_value("Course",{'name':course,'is_tot':is_tot},"course_name"),
		})
		program.flags.ignore_mandatory = True
		program.save()
		programs.flags.ignore_mandatory = True
		programs.save()

	frappe.db.commit()
	frappe.msgprint(frappe._('Module {0} has been added to the selected Course successfully.').format(frappe.bold(course)),
		title=frappe._('Course updated'), indicator='green')

@frappe.whitelist()
def add_course_to_programs(course, programs):
	semesters = json.loads(programs)
	for entry in semesters:
		program = frappe.get_doc('Program', entry)
		program.append('courses', {
			'course': course,
			'course_name': frappe.db.get_value("Course",{'name':course},"course_name"),
		})
		program.flags.ignore_mandatory = True
		program.save()
	frappe.db.commit()
	frappe.msgprint(frappe._('Module {0} has been added to all the selected Course successfully.').format(frappe.bold(course)),
		title=frappe._('Programs updated'), indicator='green')

@frappe.whitelist()
def check_for_semester(course):
	semesters = [p.parent for p in frappe.get_all('Program Course',{'course':course},'parent') ]
	if semesters:
		return semesters

@frappe.whitelist()
def get_semesters_name(course):
	data = []
	for entry in frappe.db.get_all('Program'):
		program = frappe.get_doc('Program', entry.name)
		courses = [c.course for c in program.courses]
		if not courses or course not in courses:
			data.append(program.name)
	return data

@frappe.whitelist()
def get_course_name(course):
	data = []
	for entry in frappe.db.get_all('Program',{'is__tot':1}):
		# ,{'is__tot':0}
		program = frappe.get_doc('Program', entry.name)
		courses = [c.course for c in program.courses]
		if not courses or course not in courses:
			data.append(program.name)
	return data

@frappe.whitelist()
def get_short_term_name(course):
	data = []
	for entry in frappe.db.get_all('Program',{'is__tot':0,'is_short_term_course':"Yes"}):
		# ,{'is__tot':0}
		program = frappe.get_doc('Program', entry.name)
		courses = [c.course for c in program.courses]
		if not courses or course not in courses:
			data.append(program.name)
	return data