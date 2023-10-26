from queue import Empty
import frappe
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from wsc.wsc.utils import semester_belongs_to_programs,academic_term,duplicate_row_validation,get_courses_by_semester

def validate(doc,method):
    update_user(doc)
    permission(doc)
    # director_permission(doc)
    validate_instructor_log(doc)
    academic_term(doc)
    validate_float(doc)
    # classes_scheduled = doc.get("total_scheduled_classes")
    # classes_taken = doc.get("total_classes_taken")

    # if classes_scheduled==None or classes_scheduled==0:
    #     pass
    # else :
    #     work_load_percent = (classes_taken/classes_scheduled)*100
    #     doc.work_load_percent = "%.2f" % work_load_percent

    # a.s

    count = 0
    sum = 0
    for t in doc.get('other_activities'):
        count +=1
        sum = sum+(t.duration)
    doc.number_of_other_activities = count
    # doc.total_work_load = "%.2f" % sum

def validate_float(doc):
    for d in doc.get("other_activities"):
        value = float(d.duration)
        min_value =0.0
        max_value = 1000.0
        if min_value <= value <= max_value:
                return True
        else:
            frappe.throw("Duration in other activity table is not a valid input.")
#     for d in doc.get("other_activities"):
#          if d.duration:
#             if len(d.duration)<6:
#                     print("\n\n\nHELLO")
#                     frappe.throw("<b>Duration</b> should not be too longer")   
def validate_instructor_log(doc):
    for d in doc.get("instructor_log"):
        # validate_academic_year(d)
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
        frappe.throw("Course <b>'{0}'</b> not belongs to Semester <b>'{1}'</b>".format(doc.get('course'), doc.get('program')))

####################### - FOR VALIDATE CONDITION - #############################################################
    # for director_doc in frappe.get_all("Director",{"department":doc.department},['employee_id']):
    #     print("\n\n\nDirector EMployee ID")
    #     print(director_doc.employee_id)
    #     print(director_doc['employee_id'])
    #     if(director_doc['employee_id']==doc.employee):
    #         print("\n\n In Director")
    #         director_permission(doc)
    #     elif(director_doc['employee_id']!=doc.employee):
    #         print("\n\n In Instructor")
    #         permission(doc)
    #     else:
    #         pass

####################### - FOR Program Enrollment- #############################################################      
# def create_permissions(doc,user):
#     print("IN SAVE")
#     for emp in frappe.get_all("Employee",{"name":doc.employee},['user_id']):
#         print("\n\nHELLO TO")
#         duplicateForm=frappe.get_all("User Permission", filters={
# 			"user":emp.user_id,
# 			"allow": "Instructor",
# 			"for_value":("!=",doc.name)
# 		})
#         if duplicateForm:
#             pass
#         else:
#             print("\n\n\njhello")
#             delete_ref_doctype_permissions(["Programs","Student"],doc)
#             for log in doc.get("instructor_log"):
#                 add_user_permission("Programs",log.programs, user, doc)
#                 for enroll in frappe.get_all("Program Enrollment",{"programs":log.programs,"program":log.program,"academic_year":log.academic_year,"academic_term":log.academic_term},['student']):
#                     add_user_permission("Student",enroll.student, user, doc)

        
        # for  check_perm in frappe.get_all("User Permission",{"user":emp.user_id,"allow":"Instructor","for_value":doc.name},['user','allow','for_value']):
        
########################################## - FOR DIRECTOR - #####################################################
# def director_permission(doc):
#     d = doc.get("department")
#     for dean_department in frappe.get_all("Dean",{"department":d},['director_name','employee_id','department']):
#         for instr in frappe.get_all("Instructor",{"department":dean_department.department,"employee":dean_department.employee_id},['department','employee']):
#             for emp in frappe.get_all("Employee",{"department":instr.department,"name":instr.employee},['user_id']):
#                 if emp.user_id:
#                     add_user_permission(doc.doctype,doc.name,emp.user_id,doc)   
########################################## - FOR INSTRUCTOR - #####################################################                
def permission(doc):
        for d in doc.get("instructor_log"):
            for instr in frappe.get_all("Instructor",{"name":d.parent},['employee']):
                for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id']):
                    # if emp.user_id:
                    #     add_user_permission(doc.doctype,doc.name,emp.user_id,doc)
                        dept=frappe.get_doc("Department",doc.department)
                        dept.save()
                        programs=frappe.get_doc("Programs",d.programs)
                        programs.save()
                        module=frappe.get_doc("Course",d.course)
                        module.save()

   
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
            # "birth_date": emp.date_of_birth,
            # "phone": emp.cell_number,
            # "bio": emp.bio,
        }
    )
    user.insert()
    return user.name
