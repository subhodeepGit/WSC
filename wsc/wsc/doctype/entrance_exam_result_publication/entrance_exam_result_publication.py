# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class EntranceExamResultPublication(Document):
	def validate(self):
            if self.is_new():
                dupicate_check(self)
            if self.earned_marks >= self.total_marks:
                frappe.throw('Earned Marks Cannot be Greater than Total Marks')     


def dupicate_check(self):
    if frappe.get_all("Entrance Exam Result Publication",{"entrance_exam_declaration":self.entrance_exam_declaration,
                                                       "docstatus":1,
                                                       "applicant_id":self.applicant_id}):
        frappe.throw("For This Student Entrance Result has been Published")


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):
    
    ############################## Search Field Code#################
    searchfields = frappe.get_meta(doctype).get_search_fields()
    searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)    
    
    # data=frappe.db.sql("""
    #     SELECT `name` FROM `tabEntrance Exam Declaration` WHERE ({key} like %(txt)s or {scond})  and
    #         (`exam_start_date` <= now() AND `exam_end_date` >= now())
    #          and `docstatus`=1 
    # """.format(
    #     **{
    #         "key": searchfield,
    #         "scond": searchfields,
    #         # "info":info
    #     }),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
    
    data=frappe.db.sql("""
        SELECT `name` FROM `tabEntrance Exam Declaration` WHERE ({key} like %(txt)s or {scond}) 
             and `docstatus`=1 
    """.format(
        **{
            "key": searchfield,
            "scond": searchfields,
            # "info":info
        }),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})

    return data

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query3(doctype, txt, searchfield, start, page_len, filters):
    
    ############################## Search Field Code#################
    searchfields = frappe.get_meta(doctype).get_search_fields()
    searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)    
    
    data=frappe.db.sql("""
        SELECT DISTINCT 
            adm.applicant_id,adm.applicant_name,adm.gender,adm.student_category 
    FROM 
        `tabEntrance Exam Admit Card` adm
    INNER JOIN 
        `tabApplicant List` app_list
    ON adm.applicant_id = app_list.applicant_id 
    WHERE 
        adm.docstatus = 1 AND
        adm.entrance_exam = app_list.parent AND
        app_list.parent = '{declartion}'
    """.format(
        **{
            "key": searchfield,
            "scond": searchfields,
            "declartion":filters['entrance_exam_declaration']
            # "info":info
        }),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})

    return data