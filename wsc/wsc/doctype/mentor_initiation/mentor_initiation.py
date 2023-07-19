# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document


class MentorInitiation(Document):
    def validate(doc):
        pass
     

@frappe.whitelist()
def get_mentor_mentees(user=None):
    # if user != 'Administrator':
        employee = frappe.db.get_all("Employee", {'user_id': user}, ['name'])
        if employee:
            employee = employee[0]['name']
            mentor_employee = frappe.db.get_all("Mentor Allocation", {'mentor':employee}, ['mentor'])
            if mentor_employee:
                mentor_employee = mentor_employee[0]["mentor"]
                get_data = {}
                get_data["mentor"] = frappe.db.get_value("Mentor Allocation", {"mentor":mentor_employee}, ["name"])
                get_data["mentor_name"] = frappe.db.get_value("Mentor Allocation", {"mentor":mentor_employee}, ["mentor_name"])
                get_data["student"] = []
                get_data["student_name"] = []
                get_data["programs"] = []
                for i in range(len(frappe.get_doc("Mentor Allocation", get_data["mentor"]).get("mentee_list"))):
                    get_data["student"].append(frappe.get_doc("Mentor Allocation", get_data["mentor"]).get("mentee_list")[i].student)
                    get_data["student_name"].append(frappe.get_doc("Mentor Allocation", get_data["mentor"]).get("mentee_list")[i].student_name)
                    get_data["programs"].append(frappe.db.get_value("Current Educational Details",{"parent":get_data["student"][i]}, ["programs"]))
                return get_data


def create_mentee_communications(self, doc):
    for mentee_info in self.get("mentee_information"):
        if mentee_info.check:
            communication_doc = frappe.new_doc("Mentor Mentee Communication")
            communication_doc.date = date.today()
            communication_doc.mentor = self.mentor
            communication_doc.mentor_name = self.mentor_name
            communication_doc.student =  mentee_info.student
            communication_doc.student_name = mentee_info.student_name
            communication_doc.programs = mentee_info.programs
            communication_doc.description = self.description
            communication_doc.save()
    frappe.msgprint("Mentor Mentee Communications created successfully!")
































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