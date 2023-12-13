# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document

class MentorInitiation(Document):
    def validate(self):
        create_mentee_communications(self)   
    
    def after_insert(self):
        user_per(self)

    def on_trash(self):
        delete_user_permission(self)

@frappe.whitelist()
def get_mentor_mentees(mentor=None):
    mentors = frappe.get_all("Mentor Allocation", {'name':mentor}, ['program'])
    child = frappe.get_all("Mentee List", {'parent':mentor}, ['student','student_name'])
    data=[]
    if mentors:
        for t in child:
            if t:
                a={}
                a["student"]=t.student
                a["student_name"]= t.student_name
                a["program"]=mentors[0]["program"]
                data.append(a)
        return data

def create_mentee_communications(self):
    for mentee_info in self.get("mentee_information"):
        if mentee_info.check:
            mentor_in = frappe.get_doc(
                {
                    "doctype": "Mentor Mentee Communication",
                    "date": date.today(),
                    "mentor": self.mentor,
                    "mentor_name": self.mentor_name,
                    "student": mentee_info.student,
                    "student_name": mentee_info.student_name,
                    "programs": mentee_info.programs,
                    "description":self.description,
                }
            )
            mentor_in.save()
    frappe.msgprint("Mentor Mentee Communications created successfully!")
    
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def filter_mentor(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(""" SELECT `name`,`mentor_name` FROM `tabMentor Allocation` where docstatus=1 """)	

def user_per(self):
    mentor_allo = frappe.get_all("Mentor Allocation", {'name':self.mentor}, ['mentor'])
    emp = frappe.get_all("Employee", {'name':mentor_allo[0]["mentor"]}, ['user_id'])
    if emp:
        user_trainer = frappe.get_doc(
                    {
                        "doctype": "User Permission",
                        "user": emp[0]["user_id"],
                        "allow": "Mentor Initiation",
                        "for_value": self.name,
                        "apply_to_all_doctypes": 0,
                        "applicable_for": "Mentor Initiation",
                    }
                )
        user_trainer.save()

def delete_user_permission(self):
        for t in frappe.get_all("User Permission",{"for_value":self.doctype,"for_value":self.name}):
            frappe.delete_doc("User Permission",t.name)























# @frappe.whitelist()
# def get_mentor_mentees(user=None):
#     if user != 'Administrator':
#         employee = frappe.db.get_all("Employee", {'user_id': user}, ['name'])
#         student = frappe.db.get_all("Student", {"user": user}, ['name'])
#         if employee:
#             employee = employee[0]['name']
#             mentor_employee = frappe.db.get_all("Mentor Allocation", {'mentor':employee}, ['mentor'])
#             if mentor_employee:
#                 mentor_employee = mentor_employee[0]["mentor"]
#                 get_data = {}
#                 get_data["mentor"] = frappe.db.get_value("Mentor Allocation", {"mentor":mentor_employee}, ["name"])
#                 get_data["mentor_name"] = frappe.db.get_value("Mentor Allocation", {"mentor":mentor_employee}, ["mentor_name"])
#                 get_data["student"] = []
#                 get_data["student_name"] = []
#                 get_data["programs"] = []
#                 for i in range(len(frappe.get_doc("Mentor Allocation", get_data["mentor"]).get("mentee_list"))):
#                     get_data["student"].append(frappe.get_doc("Mentor Allocation", get_data["mentor"]).get("mentee_list")[i].student)
#                     get_data["student_name"].append(frappe.get_doc("Mentor Allocation", get_data["mentor"]).get("mentee_list")[i].student_name)
#                     get_data["programs"].append(frappe.db.get_value("Current Educational Details",{"parent":get_data["student"][i]}, ["programs"]))
#                 # print("\n\n\n\n\n\n\n\n\n\n\n\n\n", get_data, "\n\n\n\n\n\n\n\n\n\n\n\n\n")
#                 return get_data
#         if student:
#             student = student[0]['name']
#             mentee_student = frappe.db.get_all("Mentee List", {"student":student}, ['student'])
#             if mentee_student:
#                 mentee_student = mentee_student[0]["student"]
#                 get_data = {}
#                 get_data["mentor"] = frappe.db.get_value("Mentee List", {"student":mentee_student}, ["parent"])
#                 get_data["mentor_name"] = frappe.db.get_value("Mentor Allocation", {"name": get_data["mentor"]}, ["mentor_name"])
#                 get_data["student"] = []
#                 get_data["student_name"] = []
#                 get_data["programs"] = []
#                 get_data["student"].append(frappe.db.get_all('Mentee List', {'student':mentee_student}, ["student"])[0]["student"])
#                 get_data["student_name"].append(frappe.db.get_all('Mentee List', {'student':mentee_student}, ["student_name"])[0]["student_name"])
#                 get_data["programs"].append(frappe.db.get_value("Current Educational Details",{"parent":get_data["student"][0]}, ["programs"]))
#                 # print("\n\n\n\n\n\n\n\n\n\n\n\n\n", get_data, "\n\n\n\n\n\n\n\n\n\n\n\n\n")
#                 return get_data