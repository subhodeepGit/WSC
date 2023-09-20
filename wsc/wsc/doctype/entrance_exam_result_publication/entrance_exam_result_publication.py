# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EntranceExamResultPublication(Document):
	pass

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):
    
    ############################## Search Field Code#################
    searchfields = frappe.get_meta(doctype).get_search_fields()
    searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)    
    
    data=frappe.db.sql("""
        SELECT `name` FROM `tabEntrance Exam Declaration` WHERE ({key} like %(txt)s or {scond})  and
            (`exam_start_date` <= now() AND `exam_end_date` >= now())
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
            adm.applicant_id 
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