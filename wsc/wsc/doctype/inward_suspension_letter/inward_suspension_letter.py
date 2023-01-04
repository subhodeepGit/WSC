# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd
from datetime import date 

class InwardSuspensionLetter(Document):
    # @frappe.whitelist()
    def on_update(self):
        icr_id = self.name
        suspension_type=self.suspension_type
        in_doc_info=frappe.db.sql("""select * from `tabInward Suspension Letter` where  name="%s" """%(icr_id))
        if len(in_doc_info)!=0:
            icr = frappe.get_doc("Inward Suspension Letter",icr_id)
            stu_df = pd.DataFrame({
                'Al_no':[]
            })
            for al in icr.student:
                s = pd.Series([al.allotment_number],index = ['Al_no'])
                stu_df = stu_df.append(s,ignore_index = True)
            if len(stu_df)!=0:    
                duplicate = stu_df[stu_df.duplicated()].reset_index()
                if len(duplicate) == 0:
                    pass
                else:
                    b=""
                    for t in range(len(duplicate)):
                        a="%s  "%(duplicate['Al_no'][t])
                        b=b+a
                    frappe.throw("Duplicate value found on allotment number "+b)
            else:
                frappe.throw("No Studnet Entered")        

    # @frappe.whitelist()
    def on_submit(self):
        icr_id = self.name
        suspension_type=self.suspension_type
        in_doc_info=frappe.db.sql("""select * from `tabInward Suspension Letter` where  name="%s" """%(icr_id))
        if len(in_doc_info)!=0:
            icr = frappe.get_doc("Inward Suspension Letter",icr_id)
            stu_df = pd.DataFrame({
                'Al_no':[],"Room_id":[]
            })
            for al in icr.student:
                s = pd.Series([al.allotment_number,al.room_id],index = ['Al_no',"Room_id"])
                stu_df = stu_df.append(s,ignore_index = True)
            if len(stu_df)!=0:    
                duplicate = stu_df[stu_df.duplicated()].reset_index()
                if len(duplicate) == 0:
                    if in_doc_info[0][5]==1:
                        if suspension_type=="University Debar":
                            for t in range(len(stu_df)):
                                frappe.db.sql("""UPDATE `tabRoom Allotment` SET `allotment_type`="%s",`end_date`="%s" WHERE `name`="%s" """%(suspension_type,date.today(),stu_df['Al_no'][t]))
                                room_info=frappe.db.sql("""SELECT `name` FROM `tabRoom Masters` where `name` ="%s" """%(stu_df['Room_id'][t]))
                                frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`-1 WHERE `name`="%s" """%(room_info[0][0]))
                            pass
                        else:
                            for t in range(len(stu_df)):
                                frappe.db.sql("""UPDATE `tabRoom Allotment` SET `allotment_type`="%s" WHERE `name`="%s" """%(suspension_type,stu_df['Al_no'][t]))
                        
                            pass
                    else:
                        pass
                else:
                    b=""
                    for t in range(len(duplicate)):
                        a="%s  "%(duplicate['Al_no'][t])
                        b=b+a
                    frappe.throw("Duplicate value found on allotment number "+b)
            else:
                frappe.throw("No Studnet Entered")  



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT `name`,`student`,`student_name`,`hostel_id` FROM `tabRoom Allotment` WHERE 
        (`start_date` <= now() AND `end_date` >= now()) and 
        (`allotment_type`!="Debar" and `allotment_type`!="University Debar" 
            and `allotment_type`!="University Suspension" and `allotment_type`!="School Suspension") 
    """
    )   

