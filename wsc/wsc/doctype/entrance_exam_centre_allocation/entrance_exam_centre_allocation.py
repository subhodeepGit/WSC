# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class EntranceExamCentreAllocation(Document):
    def validate(self):
        if self.is_new():
            dupicate_check(self)
        time_validation(self)    
        date_format = "%Y-%m-%d"
        for i in self.get('exam_slot_timings'):
            
            slot_date = datetime.strptime(i.slot_date, date_format).date()

            if isinstance(self.exam_start_date , str) and isinstance(self.exam_end_date , str):
                exam_start_date = datetime.strptime(self.exam_start_date, date_format).date()
                exam_end_date = datetime.strptime(self.exam_end_date, date_format).date()
                
                if exam_start_date > slot_date or exam_end_date < slot_date:
                    # frappe.throw("Slot Date out of Scope")
                    frappe.throw("Row <b>{0}</b> Slot Date out of Scope".format(i.idx))
            else:
                if self.exam_start_date > slot_date or self.exam_end_date < slot_date:
            
                    frappe.throw("Row <b>{0}</b> Slot Date out of Scope".format(i.idx))

def dupicate_check(self):
    if frappe.get_all("Entrance Exam Centre Allocation",{"docstatus":1,
                                                      "entrance_exam_declaration":self.entrance_exam_declaration,
                                                      "centre":self.centre}):
        frappe.throw("</b> For This Center Entrance Exam Centre Allocation Has Already Scheduled </b> ")

def time_validation(self):
    for t in self.get("exam_slot_timings"):
        
        if t.slot_starting_time and t.slot_ending_time:
            from_time= datetime.strptime(t.slot_starting_time, '%H:%M:%S').time()
            to_time= datetime.strptime(t.slot_ending_time, '%H:%M:%S').time()
            if from_time>to_time:
                frappe.throw("Row <b>{0}</b> Slot Starting Time cannot be greater than Slot Ending Time".format(t.idx))
        pass
# @frappe.whitelist()
# def get_centers(center_selection):

# 	# center_selection = frappe.get_all('Entrance Exam Centre Selection' , { 'academic_year':academic_year , 'academic_term':academic_term } , ['name'] )

# 	current_centers = frappe.get_all('Current Centers' ,{'parent':center_selection }, ['center'])
# 	return current_centers

# @frappe.whitelist()
# def get_centers_data(center):
	
# 	current_centers = frappe.get_all("Current Centers" , {'center':center , 'docstatus':1} , ['center_name' ,'center_name' , 'address' , 'district' , 'state' , 'pincode'])

# 	return current_centers

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