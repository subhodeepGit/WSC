# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class EntranceExamCentreAllocation(Document):
    def validate(self):
        date_format = "%Y-%m-%d"
        print("\n\n")

        print(type(self.exam_start_date) , type(self.exam_end_date))
        # exam_start_date = datetime.strptime(self.exam_start_date, date_format).date()

        # exam_end_date = datetime.strptime(self.exam_end_date, date_format).date()

        for i in self.get('exam_slot_timings'):

            slot_date = datetime.strptime(i.slot_date, date_format).date()
            print(type(slot_date))

            if isinstance(self.exam_start_date , str) and isinstance(self.exam_end_date , str):
                exam_start_date = datetime.strptime(self.exam_start_date, date_format).date()
                exam_end_date = datetime.strptime(self.exam_end_date, date_format).date()
                if exam_start_date >= slot_date or exam_end_date <= slot_date:
                    frappe.throw("Slot Date out of Scope")
            else:
                if self.exam_start_date >= slot_date or self.exam_end_date <= slot_date:
                    frappe.throw("Slot Date out of Scope")
            print("\n\n2")
            print(type(self.exam_start_date) , type(self.exam_end_date))

# @frappe.whitelist()
# def get_centers(center_selection):

# 	# center_selection = frappe.get_all('Entrance Exam Centre Selection' , { 'academic_year':academic_year , 'academic_term':academic_term } , ['name'] )

# 	current_centers = frappe.get_all('Current Centers' ,{'parent':center_selection }, ['center'])
# 	print("\n\n\n")
# 	# print(center_selection)
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