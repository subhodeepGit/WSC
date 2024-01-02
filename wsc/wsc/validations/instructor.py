from queue import Empty
import frappe
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.utils import semester_belongs_to_programs,academic_term,duplicate_row_validation,get_courses_by_semester
# from frappe.utils import validate_email_address

def validate(doc,method):
    validate_email(doc)
    update_user(doc)
    permission(doc)
    validate_instructor_log(doc)
    academic_term(doc)
    validate_float(doc)
    student_group_permission(doc)

    count = 0
    sum = 0
    for t in doc.get('other_activities'):
        count +=1
        sum = sum+(t.duration)
    doc.number_of_other_activities = count

def validate_float(doc):
    for d in doc.get("other_activities"):
        value = float(d.duration)
        min_value =0.0
        max_value = 1000.0
        if min_value <= value <= max_value:
                return True
        else:
            frappe.throw("Duration in other activity table is not a valid input.")

def validate_instructor_log(doc):
    for d in doc.get("instructor_log"):
        validate_semester(d)
        validate_course(d)

def validate_academic_year(doc):
    if doc.academic_term not in [d.name for d in frappe.get_all("Academic Term", {'academic_year':doc.get('academic_year')},['name'])]:
        frappe.throw("Academic Term <b>'{0}'</b> not belongs to academic year <b>'{1}'</b>".format(doc.get('academic_term'), doc.get('academic_year')))

def validate_semester(doc):
    if doc.program not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('programs')},['semesters'])]:
        frappe.throw("Semester <b>'{0}'</b> not belongs to Programs <b>'{1}'</b>".format(doc.get('program'), doc.get('programs')))

def validate_course(doc):
    if doc.course and doc.course not in get_courses_by_semester(doc.program):
        frappe.throw("Module <b>'{0}'</b> not belongs to Semester <b>'{1}'</b>".format(doc.get('course'), doc.get('program')))
              
def permission(doc):
        for d in doc.get("instructor_log"):
            for instr in frappe.get_all("Instructor",{"name":d.parent},['employee']):
                for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id']):
                    # if emp.user_id:
                    #     add_user_permission(doc.doctype,doc.name,emp.user_id,doc)
                        # dept=frappe.get_doc("Department",doc.department)
                        # dept.save()
                        programs=frappe.get_doc("Programs",d.programs)
                        programs.save()
                        # module=frappe.get_doc("Course",d.course)
                        # module.save()
def student_group_permission(doc):
    for j in frappe.get_all("Instructor Log",{"parent":doc.name},['student_group','parent']):
        if j.student_group == None:
            for i in frappe.get_all("Student Group Instructor",{"parent":j.student_group,"instructor":j.parent},['instructor','course','parent']):
                user_id = frappe.db.get_value("Instructor",{"name":i.instructor},'email_id')
                if user_id:
                    frappe.permissions.add_user_permission("Student Group",i.parent, user_id)
   
def on_trash(doc,method):
    if doc.employee:
        user_id=frappe.db.get_value("Employee",doc.employee,'user_id')
        if user_id:
            user=frappe.get_doc("User",user_id)
            user.module_profile=""
            user.save()


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_instructor_by_student_group(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Student Group Instructor",{"parent":filters.get("student_group"),"instructor": ["like", "%{0}%".format(txt)]},['instructor'],as_list=1)

def update_user(doc):
    if doc.employee:
        user_id=frappe.db.get_value("Employee",doc.employee,'user_id')
        if user_id:
            user=frappe.get_doc("User",user_id)
            user.module_profile="Instructor"
            user.role_profile_name="Employee Role"
            user.save()
            for ur_pr in frappe.get_all("User Permission",{'user':user_id,'allow':"Employee",'for_value':doc.employee,"applicable_for":("!=","Employee")}):
                user_permission=frappe.get_doc("User Permission",ur_pr.name)
                user_permission.applicable_for="Employee"
                user_permission.apply_to_all_doctypes=0
                user_permission.applicable_for="Employee"
                # user_permission.reference_doctype=doc.doctype
                # user_permission.reference_docname=doc.name
                if len(frappe.get_all("User Permission",{'user':user_id,'allow':"Employee",'for_value':doc.employee,"applicable_for":"Employee"}))==0:
                    user_permission.save()

            # create_permissions(doc,user_id)
    # set_instructors_read_only_permissions(doc)

# def docshare_permission(user,docname):
#     docshare = frappe.new_doc('DocShare')
#     docshare.user = user
#     docshare.share_doctype = "Instructor"
#     docshare.share_name = docname
#     docshare.read = 1
#     docshare.insert()


@frappe.whitelist()
def create_user(trainer, user=None, email=None):
    emp = frappe.get_doc("Instructor", trainer)

    trainer_name = emp.instructor_name.split(" ")
    middle_name = last_name = ""

    if len(trainer_name) >= 3:
        last_name = " ".join(trainer_name[2:])
        middle_name = trainer_name[1]
    elif len(trainer_name) == 2:
        last_name = trainer_name[1]

    first_name = trainer_name[0]

    if email:
        emp.email_id_for_guest_trainers = email

    user = frappe.new_doc("User")
    user.update(
        {
            "name": emp.instructor_name,
            "email": emp.email_id_for_guest_trainers,
            "enabled": 1,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "gender": emp.gender,
            "role_profile_name":"ToT Trainer",
            "module_profile":"Instructor"
            # "birth_date": emp.date_of_birth,
            # "phone": emp.cell_number,
            # "bio": emp.bio,
        }
    )
    user.insert()
    return user.name
@frappe.whitelist()
def remove_create_user(email):
    for x in frappe.get_all("User",{"name":email},['name']):
        if x.name==email:
            return True

# def validate_email(self):
#     if self.email_id_for_guest_trainers:
#         validate_email_address(self.email_id_for_guest_trainers, True)
        
def validate_email(doc):
    import re
    if doc.email_id_for_guest_trainers:
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', doc.email_id_for_guest_trainers):
            frappe.throw("<b>{0}</b> is an invalid email address. Please enter a valid email address.".format(doc.email_id_for_guest_trainers))