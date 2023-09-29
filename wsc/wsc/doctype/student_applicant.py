import frappe,json,re
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe import msgprint, _
from wsc.wsc.utils import duplicate_row_validation
from wsc.wsc.validations.student_admission import validate_academic_year
from wsc.wsc.notification.custom_notification import student_applicant_submit,student_applicant_rejected,student_applicant_approved,student_applicant_onhold
import math
from datetime import datetime


class StudentApplicant(Document):
    def on_update_after_submit(doc):
        if not doc.image:
            frappe.throw("Profile Photo is Mandatory")
        if doc.docstatus==1 and doc.application_status=="Approved":
                  if doc.doc_approved==1:
                      frappe.throw("Unable to Edit the form once the application is Approved")
                      doc.doc_approved=1

        if doc.docstatus==1 and doc.application_status=="Approved":
            frappe.db.set_value("Student Applicant",doc.name,'doc_approved',1)
            # frappe.db.set_value("Program Priority",doc.program_priority,'approve',1)
            for t in doc.get("program_priority"):
                if t.approve!=1:
                    t.approve=1
                            
        
        if doc.docstatus==1:
            validate_attachment(doc)
            # validate_student_admission(doc)
        student = frappe.get_list("Student",  filters= {"student_applicant": doc.name})
        # if len(last_result)==0:
		# if student:
        if len(student)==0 and doc.application_status=="Approved" and doc.docstatus==1:
            student = get_mapped_doc("Student Applicant", doc.name,
                {
                "Student Applicant": {
                    "doctype": "Student",
                    "field_map": {
                        "name": "student_applicant"
                    }
                },
                "Education Qualifications Details": {
                    "doctype": "Educational Details"
                },
                # "Education Qualifications Details": {
                #     "doctype": "Education Qualifications Details"
                # },
                # Education Qualifications Details
                "Document List": {
                    "doctype": "Document List"
                }
            }, ignore_permissions=True)
            student.save()
        if doc.account_name and doc.bank and doc.account_type and doc.branch_code and doc.bank_account_no:
            acc_doc = frappe.new_doc('Bank Account')
            acc_doc.account_name = doc.account_name
            acc_doc.bank =  doc.bank
            acc_doc.account_type =  doc.account_type
            acc_doc.branch_code =  doc.branch_code
            acc_doc.bank_account_no =  doc.bank_account_no
            acc_doc.party_type = "Student"
            acc_doc.party = frappe.db.get_value("Student", {'student_applicant': doc.name},'name')
            acc_doc.save()
            frappe.msgprint(_("Bank account created"))
        student = frappe.get_list("Student", filters= {"student_applicant": doc.name})
        if len(student)>1:
            frappe.throw(_("Cannot change status as student {0} is linked with student application {1}").format(student[0].name, doc.name))
    def validate(doc):
        validate_edu_details(doc)
        # doc.title = " ".join(
			# filter(None, [doc.first_name, doc.middle_name, doc.last_name])
		# )
        # doc.title=doc.first_name + doc.middle_name + doc.last_name
        # validate_percentage(doc)
        # check_age(doc)
        validate_duplicate_record(doc)
        # education_details_validation(doc)
        document_list_checkbox(doc)
        # mobile_number_validation(doc)
        validate_pin_code(doc)
        validate_applicant_name(doc)
        # update_education_parameters(doc)
        duplicate_row_validation(doc,"program_priority",["programs"])
        # validate_seat_reservation_type(doc)
        validate_student_name(doc)
        # if len(doc.education_qualifications_details) == 0:
        #     add_eligibility_table_rows(doc)
        if len(doc.document_list ) == 0:
            add_document_list_rows(doc)

        get_admission_fees(doc)
        mobile_number_validation(doc)
        # email_validation(doc)
        isValidPinCode(doc.pin_code)
        get_phone_code(doc)
        # if len(doc.program_priority ) == 0:
        #     set_web_form_fields(doc)

        # validate_counselling_structure(doc)
        validate_academic_year(doc)
        duplicate_row_validation(doc, "guardians", ['guardian', 'guardian_name'])
        duplicate_row_validation(doc, "siblings", ['full_name', 'gender'])
        validate_pincode(doc)

    def on_submit(self):
        from datetime import datetime

# datetime object containing current date and time
        now = datetime.now()
        print("now =", now)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        frappe.db.set_value("Student Applicant",self.name,'date_time',dt_string)
        student_applicant_submit(self)

        for docmnt in self.document_list:
            if docmnt.attach:
                docmnt.is_available = 1
            else:
                docmnt.is_available = 0
        
def on_change(doc,method):
    print("\n\n\nHELLO")
    delete_user_permission(doc)
    if doc.docstatus==1:
        if doc.application_status=="Approved":
            # frappe.throw("Unable to change the any data after approval of the form")
            student_applicant_approved(doc)
        elif doc.applicaiton_status=="Rejected":
            student_applicant_rejected(doc)
        elif doc.application_status=="Waiting":
            student_applicant_onhold(doc)
        else:
            pass
        # update_enrollment_admission_status(doc)

def validate_duplicate_record(self):
		duplicateForm=frappe.get_all("Student Applicant", filters={
			"academic_term":self.academic_term,
			"program_grade": self.program_grade,
			"department": self.department,
            "student_email_id":self.student_email_id,
            "name":("!=",self.name)
		})
		if duplicateForm:
			frappe.throw(("Student Applicant is already Filled the form for this Academic Term."))

def validate_student_name(doc):
    if doc.first_name:
            if not contains_only_characters(doc.first_name):
                frappe.throw("First Name should be only characters")
    if doc.middle_name:
        if not contains_only_characters(doc.middle_name):
            frappe.throw("Middle Name should be only characters")
    if doc.last_name:
        if not contains_only_characters(doc.last_name):
            frappe.throw("Last Name should be only characters")
def contains_only_characters(first_name):
    return all(char.isalpha() or char.isspace() for char in first_name)
def document_list_checkbox(doc):
    for d in doc.get("document_list"):
        if d.attach!=None:
            d.attached=1

        else:
            d.attached=0

            # frappe.db.set_value("Document List",self.name,'attached',1)
def validate_applicant_name(doc):
    if doc.first_name:  
        if not contains_only_characters(doc.first_name):
            frappe.throw("First Name should be only characters")
    if doc.middle_name:
        if not contains_only_characters(doc.middle_name):
            frappe.throw("Middle Name should be only characters")
    if doc.last_name:
        if not contains_only_characters(doc.last_name):
            frappe.throw("Last Name should be only characters")
    if doc.fathers_name:
        if not contains_only_characters(doc.fathers_name):
            frappe.throw("Father's Name should be only characters")
    if doc.mothers_name:
        if not contains_only_characters(doc.mothers_name):
            frappe.throw("Mother's Name should be only characters")
    if doc.local_guardians_name:
        if not contains_only_characters(doc.local_guardians_name):
            frappe.throw("Local Guardian Name should be only characters")
def contains_only_characters(first_name):
    return all(char.isalpha() or char.isspace() or char == '.' for char in first_name)
def delete_user_permission(doc):
    if doc.application_status=="Rejected":
        delete_permissions(doc)
        delete_route_history(doc)
        for user_del in frappe.get_all("User",{"name":doc.student_email_id}):
            frappe.delete_doc("User",user_del.name)
def delete_route_history(doc):
    for route in frappe.get_all("Route History",{"user":doc.student_email_id}):
        frappe.delete_doc("Route History",route.name)
def delete_permissions(doc):
    for usr in frappe.get_all("User Permission",{"allow":doc.doctype,"for_value":doc.name}):
        frappe.delete_doc("User Permission",usr.name)
    for usr in frappe.get_all("User Permission",{"reference_doctype":"Student Applicant","reference_docname":doc.name}):
        frappe.delete_doc("User Permission",usr.name)



# def check_age(doc):
    
#     applicantation_date = frappe.get_all("Student Admission" ,
#                                         {
#                                             'academic_year':doc.academic_year,
#                                             'academic_term':doc.academic_term,
#                                             'department':doc.department
#                                         },
#                                         ['application_start_date' , 'maximum_age_limit']
#                                     )
    
#     date_of_birth = datetime.strptime(doc.date_of_birth , '%Y-%m-%d')
    
#     dob = date_of_birth.date()
    
#     if len(applicantation_date) != 0:
#         age_diff = math.floor(((applicantation_date[0]['application_start_date'] - dob).days)/365)

#         overage = age_diff - applicantation_date[0]['maximum_age_limit']
#         print(age_diff - applicantation_date[0]['maximum_age_limit'])
#         if age_diff > applicantation_date[0]['maximum_age_limit']:
#             frappe.throw("Over Age In-eligible for applications by " + str(overage) + "years")
#     # else:
#     #     frappe.throw(" No Application Start and maximum age limit found ")
    

def mobile_number_validation(doc):
    
    if doc.local_guardian_contact_no:
       
        if not (doc.local_guardian_contact_no).isdigit():
            frappe.throw("Field <b>Local Guardian Contact Number</b> Accept Digits Only")
        if len(doc.local_guardian_contact_no)<10:
            frappe.throw("Field <b>Local Guardian Contact Number</b> must be 10 Digits")
        if len(doc.local_guardian_contact_no)>10:
            frappe.throw("Field <b>Local Guardian Contact Number</b> must be 10 Digits")


    if doc.fathers_contact_number:
        
        if not (doc.fathers_contact_number).isdigit():
            frappe.throw("Field <b>Father's Contact Number</b> Accept Digits Only")
        if len(doc.fathers_contact_number)<10:
            frappe.throw("Field <b>Father's Contact Number</b> must be 10 Digits")
        if len(doc.fathers_contact_number)>10:
            frappe.throw("Field <b>Father's Contact Number</b> must be 10 Digits")

    if doc.fathers_contact_number:
        
        if not (doc.mothers_contact_number).isdigit():
            frappe.throw("Field <b>Mother's Contact Number</b> Accept Digits Only")
        if len(doc.mothers_contact_number)<10:
            frappe.throw("Field <b>Mother's Contact Number</b> must be 10 Digits")
        if len(doc.mothers_contact_number)>10:
            frappe.throw("Field <b>Mother's Contact Number</b> must be 10 Digits")

def validate_pin_code(doc):
    
    # try:
    if doc.pin_code:

        if len(doc.pin_code)<6:
            frappe.throw("Field <b>Pincode</b> must be 6 Digits")
        if len(doc.pin_code)>6:
            frappe.throw("Field <b>Pincode</b> must be 6 Digits")
# def set_web_form_fields(doc):
#     prgram_list = [doc.program_choice_1, doc.program_choice_2,doc.program_choice3, doc.program_choice_4, doc.program_choice_5, doc.program_choice_6 ]
#     if len(prgram_list) > 0:
#         doc.set("program_priority",[])
#         for pro in prgram_list:
#             program_data = get_admission_and_semester_by_program(pro,doc.program_grade,doc.academic_year)
#             doc.append("program_priority",{
#                 "programs":pro,
#                 "semester": program_data.get('semester'),
#                 "student_admission":program_data.get('name')
#             }) 

       
#     for i in doc.education_qualifications_details:
#         i.qualification = i.qualification_ if i.qualification_ else i.qualification
#         i.year_of_completion = i.year_of_completion_ if i.year_of_completion_ else i.year_of_completion
#         i.qualification_ = i.qualification if i.qualification else i.qualification_
#         i.year_of_completion_ = i.year_of_completion if i.year_of_completion else i.year_of_completion_
#     for j in doc.document_list:
#         j.document_name = j.document_name_ if j.document_name_ else j.document_name
#         j.document_name_ = j.document_name if j.document_name else j.document_name_

# def validate_percentage(doc):
#     for eqd in doc.get('education_qualifications_details'):
#         parameter_list = frappe.get_all("Eligibility Parameter List",{"parent":doc.counselling_structure}, ['parameter', 'eligible_score'])
#         for p in parameter_list:
#             if eqd.qualification == p.parameter:
#                 if eqd.score and eqd.score < p.eligible_score:
#                     frappe.throw("You are not eligible for qualification <b>{0}</b>.".format(eqd.qualification))
#         if eqd.percentage_cgpa:
#             for program in doc.program_priority:
#                 percent_cgpa= [ i['percentagecgpa'] for i in frappe.get_all("Eligibility Parameter List",{"parent": .student_admission,"student_category":doc.student_category, "parameter":eqd.qualification},'percentagecgpa' )]
#                 if percent_cgpa and  eqd.percentage_cgpa != percent_cgpa[0]:
#                     frappe.throw("Please correct option for Percentage/CGPA for row no .<b>{0}</b> in Education Qualifications Details.".format(eqd.idx))

def on_update(doc,method):
    delete_user_permission(doc)
    if doc.docstatus==1:
        count = 0
        # print(type(doc.counselling_based_program_priority))
        ## if Approve is selected multiple times
        
        programs = []
        for i in doc.counselling_based_program_priority:
            programs.append(i.programs)

        print(programs)

        programs_set = set(programs)

        if(len(programs) != len(programs_set)):
            frappe.throw("Duplicate Courses in counselling based program priority")

        for d in doc.counselling_based_program_priority:
             
            ## For programs field
            ## For Approve checkbox
            if d.approve == 1: 
                # print(d.approve , count , d.programs)
                count = count + 1

            if d.programs in doc.counselling_based_program_priority:
                print(d.programs)
        
        if count > 1:
            frappe.throw("Please Approve only single course in counselling based program priority")

        validate_attachment(doc)
        # validate_student_admission(doc)
        student = frappe.get_list("Student",  filters= {"student_applicant": doc.name})
        # if len(last_result)==0:
		# if student:
        if len(student)==0 and doc.application_status=="Approved" and doc.docstatus==1:
            student = get_mapped_doc("Student Applicant", doc.name,
                {
                "Student Applicant": {
                    "doctype": "Student",
                    "field_map": {
                        "name": "student_applicant"
                    }
                },
                "Education Qualifications Details": {
                    "doctype": "Educational Details"
                },
                "Document List": {
                    "doctype": "Document List"
                }
            }, ignore_permissions=True)
            # student.save()
        if doc.account_name and doc.bank and doc.account_type and doc.branch_code and doc.bank_account_no:
            acc_doc = frappe.new_doc('Bank Account')
            acc_doc.account_name = doc.account_name
            acc_doc.bank =  doc.bank
            acc_doc.account_type =  doc.account_type
            acc_doc.branch_code =  doc.branch_code
            acc_doc.bank_account_no =  doc.bank_account_no
            acc_doc.party_type = "Student"
            acc_doc.party = frappe.db.get_value("Student", {'student_applicant': doc.name},'name')
            acc_doc.save()
            frappe.msgprint(_("Bank account created"))
    
def education_details_validation(doc):
    if doc.student_category and doc.student_admission:
        for d in get_eligibility_parameter_list_for_category(doc.student_admission,doc.student_category):
            if d.parameter not in [ed.qualification for ed in doc.get("education_qualifications_details")]:
                frappe.throw("Please Add <b>{0}</b> in Education Details Table".format(d.parameter))
           
def mobile_number_validation(doc):
    if doc.student_mobile_number:
        if not (doc.student_mobile_number).isdigit():
            frappe.throw("Field <b>Mobile Number</b> Accept Digits Only")
        if len(doc.student_mobile_number)>10:
            frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")
        if len(doc.student_mobile_number)<10:
            frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")

def email_validation(doc):
    for stu_app in frappe.get_all("Student Applicant",{"student_email_id":doc.student_email_id,"docstatus":("!=",2),"name":("!=",doc.name)}):
        frappe.throw("<b>Email ID</b> already Exist <b><a href='/app/student-applicant/{0}' target='_blank'>{0}</a></b>".format(stu_app.name))

def add_document_list_rows(doc): 
    if doc.student_category and doc.academic_year:
        doc.set("document_list",[])
        for d in get_document_list_by_category(doc):
            doc.append("document_list",{
                "document_name":d.document_name,
                "mandatory":d.mandatory,
                "is_available" :d.is_available,
                "mandatory_during_counselling":d.mandatory_during_counselling
            })

def validate_edu_details(doc):
    # doc.set("education_qualifications_details",[])
    if len(doc.education_qualifications_details) == 0:
        for result in frappe.get_all("Eligibility Parameter List",{"parent":doc.student_admission,"parenttype":"Student Admission"},["parameter","percentagecgpa","is_mandatory","eligible_score"] , order_by="parameter",group_by="parameter"):
            doc.append("education_qualifications_details",{
                "qualification":result.parameter,
                "percentage_cgpa":result.percentagecgpa,
                "mandatory":result.is_mandatory,
                "admission_percentage":result.eligible_score
        })
#  var edu_row = frm.add_child("education_qualifications_details");
#                     //                         edu_row.qualification = row.parameter;
#                     //                         edu_row.percentage_cgpa = row.percentagecgpa;
#                     //                         edu_row.mandatory = row.is_mandatory;
#                     //                         edu_row.admission_percentage = row.eligible_score;
# for d in doc.get("document_list"):
#         if d.mandatory and not d.attach:

# def add_eligibility_table_rows(doc): 
#     if doc.student_category and doc.academic_year:
#         doc.set("education_qualifications_details",[])
#         for d in get_eligibility_list_by_category(doc):
#             print("\n\n\n")
#             print(d)
#             doc.append("education_qualifications_details",{
#                 "qualification":d.eligibility,
#                 "mandatory":d.mandatory,
#                 # "is_available" :d.is_available,
#                 # "mandatory_during_counselling":d.mandatory_during_counselling
#             })
def status_validation(doc):
    if doc.student_admission and doc.application_status=="Approved":
        admission_doc=frappe.get_doc("Student Admission",doc.student_admission)
        if admission_doc.counselling_fees=="YES":
            for st in frappe.get_all("Student",{"student_applicant":doc.name}):
                if len(frappe.get_all("Fees",{"student":st.name}))<1:
                    frappe.throw("Please Pay Fess First")
        
def get_year_list(from_year,to_year):
    year_list=[]
    if from_year == to_year:
        year_list.append(from_year)
    else:
        if '-' in from_year and '-' in to_year:
            new_from_year=from_year
            year_list.append(from_year)
            while new_from_year != to_year:
                new_from_year=str(int(new_from_year.split('-')[0])+1)+"-"+str(int(new_from_year.split('-')[1])+1)
                year_list.append(new_from_year)
    return year_list

# def update_education_parameters(doc):
#     if doc.program_priority:
#         main_result = ""
#         for program in doc.program_priority:
#             parameters= frappe.get_all("Eligibility Parameter List",{"parent":program.student_admission,"student_category":doc.student_category},['parameter', 'percentagecgpa', 'total_score', 'eligible_score'],order_by="idx")
#             edu_detail ="<b> * "+ program.student_admission+"</b><br>"
#             str_data = ""
#             for p in parameters[0:]:
#                 str_p = str(parameters.index(p)+1)+"] Parameter:"
#                 if p['parameter']:
#                     str_p = str_p+ p['parameter'] +", "
#                 str_p= str_p+ " Percent/CGPA:"
#                 if p['percentagecgpa']:
#                     str_p = str_p + p['percentagecgpa']+", "
#                 str_p= str_p+" Eligible Score:"
#                 if p['eligible_score']:
#                     str_p = str_p +str(p['eligible_score'])+", "
#                 str_p = str_p+" Total Score:"
#                 if p['total_score']:
#                     str_p = str_p + str(p['total_score'])+"<br>"
#                 str_data = str_data + str_p
#             edu_detail = edu_detail + str_data
#             main_result = main_result+edu_detail+"<br>"
#         doc.education_detail = main_result

@frappe.whitelist()
def review_student(source_name):
    from wsc.wsc.doctype.student_exchange_applicant.student_exchange_applicant import get_academic_calender_table
    from wsc.wsc.doctype.semesters.semesters import get_courses
    st_applicant=frappe.get_doc("Student Applicant", source_name)
    
    preview_applicant = frappe.new_doc("Preview")
    preview_applicant.first_name = st_applicant.first_name 
    preview_applicant.caste_category = st_applicant.student_category
    preview_applicant.middle_name = st_applicant.middle_name
    preview_applicant.last_name = st_applicant.last_name
    preview_applicant.department = st_applicant.department 
    # program_enrollment.programs = counselling_based_program_priority[0]['programs']
    preview_applicant.date_of_birth = st_applicant.date_of_birth
    preview_applicant.academic_year=st_applicant.academic_year
    preview_applicant.academic_term=st_applicant.academic_term
    preview_applicant.student_category=st_applicant.category
    preview_applicant.seat_reservation_type=st_applicant.category
    preview_applicant.program_grades = st_applicant.program_grade
    preview_applicant.gender = st_applicant.gender
    preview_applicant.religion=st_applicant.religion
    preview_applicant.blood_group=st_applicant.blood_group
    preview_applicant.student_email_address=st_applicant.student_email_id
    preview_applicant.student_mobile_number=st_applicant.student_mobile_number
    preview_applicant.nationality = st_applicant.nationality
    preview_applicant.physically_disabled = st_applicant.physically_disabled
    preview_applicant.award_winner=st_applicant.award_winner
    preview_applicant.states=st_applicant.states
    preview_applicant.districts=st_applicant.districts
    preview_applicant.blocks=st_applicant.blocks
    preview_applicant.post_office = st_applicant.post_office
    preview_applicant.ciity = st_applicant.city
    preview_applicant.address_line_1=st_applicant.address_line_i
    preview_applicant.address_line_2=st_applicant.address_line_ii
    preview_applicant.pincode=st_applicant.pin_code
    preview_applicant.fathers_name=st_applicant.fathers_name
    preview_applicant.fathers_contact_number = st_applicant.fathers_contact_number
    preview_applicant.programs = st_applicant.programs_


    preview_applicant.fathers_qualification = st_applicant.qualification
    preview_applicant.fathers_occupation=st_applicant.fathers_occupation
    preview_applicant.fathers_annual_income=st_applicant.father_annual_income
    preview_applicant.mothers_name=st_applicant.mothers_name
    preview_applicant.mothers_contact_number=st_applicant.mothers_contact_number
    preview_applicant.mothers_qualification = st_applicant.mothers_qualification
    preview_applicant.mothers_occupation = st_applicant.mothers_occupation
    preview_applicant.mothers_annual_income=st_applicant.mother_annual_income
    preview_applicant.local_guardians_name=st_applicant.local_guardians_name
    preview_applicant.local_guardian_contact_no=st_applicant.local_guardian_contact_no
    preview_applicant.relation_with_student=st_applicant.relation_with_student
    preview_applicant.local_guardian_occupation = st_applicant.local_guardian_occupation
    preview_applicant.local_guardian_address = st_applicant.local_guardian_address

    
    for d in st_applicant.get("disable_type"):
        preview_applicant.append("physically_disabled_table",{
            "disability_type":d.disability_type,
            "percentage_of_disability":d.percentage_of_disability,
            "attach_disability_certificate":d.attach_disability_certificate
        })
    
    for d in st_applicant.get("awards_list"):
        preview_applicant.append("awards_winner_list",{
            "awards":d.awards,
            "won_in_year":d.won_in_year
        })
    for d in st_applicant.get("program_priority"):
        preview_applicant.append("course_preferences",{
            "programs":d.programs,
            "approve":d.approve
        })
    # for d in st_applicant.get("program_priority"):
    #     preview_applicant.append("course_preferences",{
    #         "programs":d.programs,
    #     })
    for d in st_applicant.get("education_qualifications_details"):
        preview_applicant.append("education_qualifications_details",{
            "qualification":d.qualification,
            "institute":d.institute,
            "board":d.board,
            "boards":d.boards,
            "percentage_cgpa":d.percentage_cgpa,
            "total_marks":d.total_marks,
            "earned_marks":d.earned_marks,
            "cgpa":d.cgpa,
            "score":d.score,
            "year_of_completion":d.year_of_completion,
            "mandatory":d.mandatory
        })
    for d in st_applicant.get("document_list"):
            preview_applicant.append("document_list",{
                "document_name":d.document_name,
                "attach":d.attach,
                "mandatory":d.mandatory
            })

    # if st_applicant.program:
    #     for crs in get_courses(st_applicant.program):
    #         program_enrollment.append("courses",crs)
    # if st_applicant.student_admission:
    #     st_admission=frappe.get_doc("Student Admission",st_applicant.student_admission)
    #     if st_admission.admission_fees=="YES":
    #         for fs in st_admission.get("admission_fee_structure"):
    #             if fs.student_category==student.student_category:
    #                 program_enrollment.append("fee_structure_item",{
    #                     "student_category":student.student_category,
    #                     "fee_structure":fs.fee_structure,
    #                     "amount":fs.amount,
    #                     "due_date":fs.due_date
    #                 })
                
    #     if st_admission.academic_calendar:
    #         for d in get_academic_calender_table(st_admission.academic_calendar):
    #             program_enrollment.append("academic_events_table",d)
    # print(program_enrollment.program_grade)
    return preview_applicant

def get_admission_fees(doc):
   doc.set("admission_fees",[])
   for admission in doc.get('program_priority'):
       doc.append("admission_fees",{
           "admission":admission.student_admission,
           "programs":admission.programs,
           "fees":get_fees_by_category(doc,admission.student_admission) or 0
       })
def get_fees_by_category(doc,admission):
    student_admission=frappe.get_doc("Student Admission",admission)
    if student_admission.admission_fees=="YES":
        for d in student_admission.get("admission_fee_structure"):
            if d.student_category==doc.student_category:
                return d.amount
@frappe.whitelist()
def get_student_applicant_details(student):
    for st in frappe.get_all("Student",{'name':student},['student_applicant']):
        if st.get('student_applicant'):
            for st_app in frappe.get_all("Student Applicant",{"name":st.get('student_applicant'),"docstatus":1}):
                return frappe.get_doc("Student Applicant",st_app)

@frappe.whitelist()
def get_eligibility_parameter_list_for_category(admission,category):
    parameter_list = frappe.get_all("Eligibility Parameter List",{"parent":admission,"student_category":category},['parameter'],order_by="parameter_name asc")
    return parameter_list

def get_document_list_by_category(doc):
    filters={"student_category":doc.student_category}
    group_by=""
    if doc.counselling_structure:
        filters.update({"parent":doc.counselling_structure,"parenttype":"Counselling Structure"})
    else:
        filters.update({"parent":["IN",[d.student_admission for d in doc.get('program_priority')]],"parenttype":"Student Admission"})
        group_by="document_name"

    doc_list  = frappe.db.sql("""SELECT DL.document_name, DL.mandatory, DL.is_available, DL.mandatory_during_counselling from `tabDocuments Template List` as DL 
    inner join `tabDocuments Template` as D on DL.parent= D.name where D.student_category='{0}' and D.academic_year = '{1}' and D.department = '{2}' ORDER BY document_name ASC""".format(doc.student_category,doc.academic_year,doc.department) ,as_dict=1)
    print("\n\n\nDOCUMENTS",doc_list)
    return doc_list if doc_list else []
# def get_eligibility_list_by_category(doc):
#     filters={"student_category":doc.student_category}
#     group_by=""
#     # if doc.counselling_structure:
#     #     filters.update({"parent":doc.counselling_structure,"parenttype":"Counselling Structure"})
#     # else:
#     #     filters.update({"parent":["IN",[d.student_admission for d in doc.get('program_priority')]],"parenttype":"Student Admission"})
#     #     group_by="document_name"

#     doc_list  = frappe.db.sql("""SELECT DL.eligibility, DL.mandatory from `tabEligibility Table` as DL 
#     inner join `tabEligibility List` as D on DL.parent= D.name where D.academic_year = '{0}' and D.degree = '{1}' ORDER BY eligibility ASC""".format(doc.academic_year,doc.recent_degree) ,as_dict=1)
#     return doc_list if doc_list else []
def on_submit(self):
        student_applicant_submit(self)

@frappe.whitelist()
def enroll_student(source_name):
    from wsc.wsc.doctype.student_exchange_applicant.student_exchange_applicant import get_academic_calender_table
    from wsc.wsc.doctype.semesters.semesters import get_courses
    st_applicant=frappe.get_doc("Student Applicant", source_name)
    
    # counselling_based_program_priority = frappe.get_all("Counseling Based Program Priority" , {'parent' : st_applicant.name , 'approve' : 1} , ['programs'])
    print(st_applicant)
    for student in frappe.get_all("Student",{"student_applicant":source_name},['name','student_category','student_name']):
        program_enrollment = frappe.new_doc("Program Enrollment")
        program_enrollment.student = student.name
        program_enrollment.student_category = student.student_category
        program_enrollment.student_name = student.student_name
        program_enrollment.roll_no = student.roll_no
        program_enrollment.programs = st_applicant.counselling_course 
        # program_enrollment.programs = counselling_based_program_priority[0]['programs']
        program_enrollment.program = st_applicant.counselling_semester
        program_enrollment.academic_year=st_applicant.academic_year
        program_enrollment.academic_term=st_applicant.academic_term
        program_enrollment.category=st_applicant.category
        program_enrollment.seat_reservation_type=st_applicant.category
        program_enrollment.reference_doctype="Student Applicant"
        program_enrollment.reference_name=source_name
        program_enrollment.program_grade = st_applicant.program_grade
        program_enrollment.gender=st_applicant.gender
        program_enrollment.physically_disabled=st_applicant.physically_disabled
        program_enrollment.award_winner=st_applicant.award_winner  
        program_enrollment.boarding_student=st_applicant.hostel_required
        
        for d in st_applicant.get("disable_type"):
            program_enrollment.append("disable_type",{
                "disability_type":d.disability_type,
                "percentage_of_disability":d.percentage_of_disability
            })
        
        for d in st_applicant.get("awards_list"):
            program_enrollment.append("awards_list",{
                "awards":d.awards,
                "won_in_year":d.won_in_year
            })

        if st_applicant.program:
            for crs in get_courses(st_applicant.program):
                program_enrollment.append("courses",crs)
        if st_applicant.student_admission:
            st_admission=frappe.get_doc("Student Admission",st_applicant.student_admission)
            if st_admission.admission_fees=="YES":
                for fs in st_admission.get("admission_fee_structure"):
                    if fs.student_category==student.student_category:
                        program_enrollment.append("fee_structure_item",{
                            "student_category":student.student_category,
                            "fee_structure":fs.fee_structure,
                            "amount":fs.amount,
                            "due_date":fs.due_date
                        })
                    
            if st_admission.academic_calendar:
                for d in get_academic_calender_table(st_admission.academic_calendar):
                    program_enrollment.append("academic_events_table",d)
        print(program_enrollment.program_grade)
        return program_enrollment
        
@frappe.whitelist()
def show_fees_button(student_applicant,student_admission):
    if student_admission:
        admission_doc=frappe.get_doc("Student Admission",student_admission)
        if admission_doc.counselling_fees=="YES":
            for st in frappe.get_all("Student",{"student_applicant":student_applicant}):
                if len(frappe.get_all("Fees",{"student":st.name,"docstatus":1}))>0:
                    return False
        else:
            return False
    return True

# @frappe.whitelist()
# def create_fees(source_name, target_doc=None):
#     from wsc.wsc.validations.program_enrollment import get_program_enrollment
#     from education.education.api import get_fee_components

#     def set_missing_values(source, target):
#         for d in frappe.get_all("Counselling Structure",{"name":source.counselling_structure}):
#             for fsi in frappe.get_all("Fee Structure Item",{"parent":d.name,"parentfield":"counselling_fees","student_category":source.student_category},["fee_structure","due_date"]):
#                 target.fee_structure=fsi.fee_structure
#                 target.due_date=fsi.due_date
#         if target.fee_structure:
#             fee_components = get_fee_components(target.fee_structure)
#             target.update({"components": fee_components})
#         if source.student_email_id:
#             student = frappe.db.get_value("Student", {'student_email_id':source.student_email_id}, 'name')
#             target.student = student

#         target.programs=''
#         target.program=''
#         if get_program_enrollment(target.student):
#             target.program_enrollment=get_program_enrollment(target.student)['name']
#             target.programs=get_program_enrollment(target.student)['programs']
#             target.program=get_program_enrollment(target.student)['program']
#             target.has_program_enrollment=1

#     doclist = get_mapped_doc("Student Applicant", source_name,  {
#         "Student Applicant": {
#             "doctype": "Fees",
#             "validation": {
#                 "docstatus": ["=", 1]
#             },
#             "field_map":{
#                 "doctype":"reference_doctype",
#                 "name":"reference_docname"
#             }
#         },
#     }, target_doc,set_missing_values)
#     return doclist


def validate_attachment(doc):
    for d in doc.get("document_list"):
        if d.mandatory and not d.attach:
            frappe.throw("Please Attach Document <b>{0}</b>".format(d.document_name))
    for d in doc.get("education_qualifications_details"):
        if d.mandatory==1 and not d.board and not d.score and d.year_of_completion:
            frappe.throw("Please enter the details of <b>{0}</b>".format(d.document_name))


def validate_student_admission(doc):
    for i in doc.program_priority:
        stud_admi_data = frappe.db.sql("""SELECT CA.student_admission, CS.name from `tabProgram Priority` as CA inner join `tabStudent Applicant`  as CS on CA.parent = CS.name where CS.academic_year = '{0}' and CS.docstatus=1""".format(doc.academic_year), as_dict=1)
        if i.student_admission in [d.student_admission for d in stud_admi_data]:
            exist_data = ', '.join(map(str, [d.name for d in stud_admi_data]))
            frappe.throw("Student admission <b>'{0}'</b> already exists in Counselling Structure <b>'{1}'</b> ".format(i.student_admission, exist_data))

@frappe.whitelist()
def get_document_list(student_category):
    doc_list  = frappe.db.sql("""SELECT DL.document_name, DL.mandatory, DL.is_available from `tabDocuments Template List` as DL 
    inner join `tabDocuments Template` as D on DL.parent= D.name where D.student_category='{0}'""".format(student_category), order_by="document_name asc", as_dict=1)
    return doc_list

@frappe.whitelist()
def get_sharing_type():
    capacity=""
    for room in frappe.get_all("Room Type",order_by="capacity",group_by="capacity",fields=["capacity"]):
        capacity+=("\n"+str(room.capacity))

    if not capacity:
        capacity="\n1\n2\n3\n4"

    return capacity

# def validate_seat_reservation_type(doc):
#     seat_reservation_type_list = [s.seat_reservation_type for s in frappe.get_all("Reservations List",{"parent":["IN",[d.student_admission for d in doc.get("program_priority")]]}, 'seat_reservation_type')]
#     if seat_reservation_type_list:
#         if doc.physically_disabled:
#             physically_disabled_list = [r.name for r in frappe.get_all("Seat Reservation Type",{"name":["IN",seat_reservation_type_list], 'physically_disabled':1}, 'name')]
#             if len(physically_disabled_list) == 0 :
#                 frappe.throw("Seat Reservation Type <b>Physically Disabled</b> Not Exists in Student Admissions List")
#         if doc.award_winner:
#             award_winner_list = [r.name for r in frappe.get_all("Seat Reservation Type",{"name":["IN",seat_reservation_type_list], 'award_winner':1}, 'name')]
#             if len(award_winner_list) == 0 :
#                 frappe.throw("Seat Reservation Type <b>Award Winner</b> Not Exists in Student Admissions List")

@ frappe.whitelist()
def get_admission_and_semester_by_program(programs,program_grade,academic_year):
    for d in frappe.get_all("Student Admission",{"admission_program":programs,"program_grade":program_grade,"academic_year":academic_year},['name','admission_program','semester','counselling_required','counselling_structure']):
        return d
    return {"no_record_found":1}

@frappe.whitelist()
def get_counselling_structure(program_grade,department,academic_year):
    for d in frappe.get_all("Counselling Structure",{"program_grade":program_grade,"department":department,"academic_year":academic_year}):
        return d

# @frappe.whitelist() for future student applicant in wsc (Tousiff)
# def get_education_qualifications_details_by_admissions(student_category,admission):
#     return frappe.get_all("Eligibility Parameter List",{"parent":["IN",[d.get("student_admission") for d in json.loads(admission)]],"parenttype":"Student Admission"},["parameter","percentagecgpa","is_mandatory","eligible_score"] , order_by="parameter",group_by="parameter")

@frappe.whitelist()
def filter_programs_by_department(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Programs",{"name":['like', '%{}%'.format(txt)],"department":["IN",[d.name for d in frappe.get_all("Department",{"name":filters.get("department")})]],"program_grade":["IN",[d.name for d in frappe.get_all("Program Grades",{"grade":filters.get("program_grade")})]]},order_by="name asc",as_list=1)
##NEW Code by Tousiff##
@frappe.whitelist()
def filter_programs_by_department_counselling(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Programs",{"name":['like', '%{}%'.format(txt)],"department":["IN",[d.name for d in frappe.get_all("Department",{"name":filters.get("department")})]],"program_grade":["IN",[d.name for d in frappe.get_all("Program Grades",{"grade":filters.get("program_grade")})]]},order_by="name asc",as_list=1)
#End
@frappe.whitelist()
def get_qualification_list():
    quali_list =  [q.name for q in frappe.db.get_list("Eligibility Parameters", "name", order_by="parameter_name asc")]
    academic_yr_list =  [q.name for q in frappe.db.get_list("Academic Year", "name", order_by="name")]
    return {'qual':quali_list, 'acadmic':academic_yr_list}

def isValidPinCode(pinCode):
    if pinCode:
        regex = "^[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}$"
        p = re.compile(regex)
        if (pinCode == ''):
            return False
            
        m = re.match(p, pinCode)
        if m is None:
            return False
        else:
            return True

def get_phone_code(doc):
    if doc.country_code:
        for st in frappe.get_all("State",{"name":doc.states},['country']):
            for cnt in frappe.get_all("Country",{"name":st.country},['country_phone_code']):
                doc.country_code=cnt.country_phone_code

# def update_available_seats(doc):
#     if doc.reference_doctype=="Student Applicant":
#         student_admission = frappe.db.get_value("Student Applicant",{"name":doc.reference_name, 'docstatus':1}, 'student_admission')
#         for sa in frappe.get_all("Student Admission",{"name":student_admission}):
#             sa_doc=frappe.get_doc("Student Admission",sa.name)
#             if len(sa_doc.get('seat_balances')) == 0:
#                 for seat_rd in sa_doc.get("reservations_distribution"):
#                     row = sa_doc.append('seat_balances', {})
#                     row.seat_reservation_type = seat_rd.seat_reservation_type
#                     row.seat = seat_rd.seat
#             sa_doc.save()
#             for seats in sa_doc.get("seat_balances"):
#                 if seats.seat_reservation_type == doc.seat_reservation_type:
#                     seats.seat -= 1
#                 if seats.seat_reservation_type==doc.seat_reservation_type:
#                     if seats.seat==0:
#                         frappe.throw("Seats Not Available For This Student Category <b>{0}</b> in Admission <b>{1}</b>".format(seats.student_category,sa.name))
#             sa_doc.save()
#         #physicaly handicapped
#         # frappe.db.get_value("Student Applicant",{"name":doc.reference_name, 'docstatus':1, 'physically_disabled':1}, 'student_admission')

def validate_pincode(doc):
    if doc.pin_code:
        if not check_int(doc.pin_code):
            frappe.throw("Pincode must be the integer.")

def check_int(pin_code):
    import re
    return re.match(r"[-+]?\d+(\.0*)?$", pin_code) is not None

# def validate_counselling_structure(doc):
#     if doc.counselling_structure:
#         if doc.counselling_structure not in [d['name'] for d in frappe.get_all("Counselling Structure",{"program_grade":doc.program_grade,"department":doc.department,"academic_year":doc.academic_year},['name'])]:
#             frappe.throw("Counselling structure <b>'{0}'</b> not belongs to program grade,academic year and department".format(doc.counselling_structure))
            
        # program_list = [d.programs for d in frappe.get_all("Counselling Programs",{"parent":doc.counselling_structure},"programs")]
        # for p in doc.program_priority:
        #     if program_list and p.programs:
        #         if p.programs not in program_list:
        #             frappe.throw("Programs <b>'{0}'</b> not belongs to Counselling Structure <b>'{1}'</b>".format(p.programs, doc.counselling_structure))
        # # parameter_list = frappe.db.get_value("Eligibility Parameter List",{"parent":doc.counselling_structure, 'student_category':doc.student_category},"parameter")
        # parameter_total_list = frappe.db.get_all("Eligibility Parameter List",{"parent":doc.counselling_structure, 'student_category':doc.student_category},["parameter", "total_score"])
        # for p in doc.education_qualifications_details:
        #     if p.qualification:
        #         if p.qualification not in [p['parameter'] for p in parameter_total_list]:
        #             frappe.throw("Qualification of education qualifications details <b>'{0}'</b> not belongs to Counselling Structure <b>'{1}'</b>".format(p.qualification, doc.counselling_structure))
        #         else:
        #             for pt in parameter_total_list:
        #                 if pt.parameter == p.qualification:
        #                     if p.score > pt.total_score:
        #                         frappe.throw("Score <b>'{0}'</b> of education qualifications details should not be greater than the total score <b>'{1}'</b>".format(p.score, pt.total_score))
    # else:
    #     if doc.department and doc.program_grade:
    #         for p in doc.program_priority:
    #             if p.programs:
    #                 if p.programs not in [d['name'] for d in frappe.get_all("Programs",{"program_grade":doc.program_grade,"department":doc.department},['name'])]:
    #                     frappe.throw("Programs <b>'{0}'</b> not belongs to program grade <b>'{1}'</b> and department <b>'{2}'</b>".format(p.programs, doc.program_grade, doc.department))
        # for p in doc.program_priority:
        #     if p.student_admission and doc.student_category:
        #         # parameter_list = [i['parameter'] for i in frappe.db.get_all("Eligibility Parameter List",{"parent":p.student_admission, 'student_category':doc.student_category},["parameter"])]
        #         parameter_total_list = frappe.db.get_all("Eligibility Parameter List",{"parent":p.student_admission, 'student_category':doc.student_category},["parameter", "total_score"])
        #         for e in doc.education_qualifications_details:
        #             if e.qualification not in [p.parameter for p in parameter_total_list]:
        #                 frappe.throw("Qualification of education qualifications details <b>'{0}'</b> not belongs to Student Admission <b>'{1}'</b>".format(e.qualification, p.student_admission))
        #             else:
        #                 for pt in parameter_total_list:
        #                     if pt.parameter == e.qualification:
        #                         if e.score > pt.total_score:
        #                             frappe.throw("Score <b>'{0}'</b> of education qualifications details should not be greater than the total score <b>'{1}'</b>".format(e.score, pt.total_score))


