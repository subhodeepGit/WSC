import frappe

def validate(doc, method):
	validate_student_group(doc)
	validate_course_schedule(doc)

def validate_student_group(doc):
	if doc.student_group:
		stud_grp_list = frappe.db.sql("""SELECT SG.name from `tabStudent Group Student` as SGS 
			inner join `tabStudent Group` as SG on SGS.parent=SG.name 
			where '{0}' = SGS.student""".format(doc.student), as_dict=1)
		if doc.student_group not in [d.name for d in stud_grp_list]:
			frappe.throw("Student group <b>'{0}'</b> not belongs to student <b>'{1}'</b>".format(doc.student_group, doc.student))

def validate_course_schedule(doc):
	fltr = {}
	lst = []
	for i in frappe.get_all("Student Group Student",{'student':doc.get("student")},['parent']):
		if i.parent not in lst:
			lst.append(i.parent)
	
	if doc.course_schedule and  not frappe.db.get_value("Course Schedule",{"student_group":["IN",lst],"name":doc.course_schedule},["name"]):
		frappe.throw("Course schedule <b>'{0}'</b> not belongs to student <b>'{1}'</b>".format(doc.course_schedule, doc.student))

# @frappe.whitelist()
# def get_group(doctype, txt, searchfield, start, page_len, filters):
#     fltr = {}
#     lst = []
#     if txt:
#         fltr.update({"parent":txt})
#     for i in frappe.get_all("Student Group Student",{'student':filters.get("student")},['parent']):
#         if i.parent not in lst:
#                 lst.append(i.parent)
#     return [(d,) for d in lst]

@frappe.whitelist()
def get_group(doctype, txt, searchfield, start, page_len, filters):
    fltr = {'student':filters.get("student")}
    lst = []
    if txt:
        fltr.update({"parent":['like', '%{}%'.format(txt)]})
    for i in frappe.get_all("Student Group Student",fltr,['parent']):
        if i.parent not in lst:
            lst.append(i.parent)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_course_schedule(doctype, txt, searchfield, start, page_len, filters):
    fltr = {'student':filters.get("student")}
    lst = []
    if txt:
        fltr.update({"parent":['like', '%{}%'.format(txt)]})
    for i in frappe.get_all("Student Group Student",fltr,['parent']):
        if i.parent not in lst:
            lst.append(i.parent)
    
    return frappe.get_all("Course Schedule",{"student_group":["IN",lst]},["name"],as_list=1)