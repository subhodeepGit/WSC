# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd


class RoomMasters(Document):
    # @frappe.whitelist()
    def validate(doc):
        hostel_id=doc.hostel_id
        room_number=doc.room_number
        Room_id=doc.name
        validity=doc.validity
        actual_room_type=doc.actual_room_type

        info=''' RM WHERE RM.hostel_id="%s" and RM.room_number="%s" and RM.validity="Functional" '''%(hostel_id,room_number) 
        Type="General"
        Ck_df=Room_master_sql(info,Type, doc) # cheacking for same room no and hostel is present 

        info=''' WHERE `name`="%s" '''%(Room_id)
        Type="General"
        hostel_df=Room_master_sql(info,Type, doc) # checking room id is present or not

        if len(hostel_df)==0 and len(Ck_df)==0:
            previous_room_capacity=doc.previous_room_capacity
            actual_capacity=doc.actual_capacity
            if previous_room_capacity==actual_capacity:
                pass
            else:
                frappe.throw("Vacancy Not Avalable")
        else:
            if len(hostel_df)!=0:
                if hostel_id==hostel_df['hostel_id'][0] and hostel_df['room_number'][0]==room_number:
                    if hostel_df['validity'][0]==validity:
                        if hostel_df['actual_room_type'][0]==actual_room_type:
                            previous_room_capacity=doc.previous_room_capacity
                            actual_capacity=doc.actual_capacity
                            if previous_room_capacity==actual_capacity:
                                pass
                            else:
                                frappe.throw("Vacancy Not Avalable")
                        else:
                            previous_room_capacity=doc.previous_room_capacity
                            actual_capacity=doc.actual_capacity
                            if previous_room_capacity==actual_capacity:
                                frappe.db.sql("""UPDATE `tabRoom Allotment` SET `room_type`="%s" WHERE `room_id`="%s" and (`start_date`<=now() and `end_date`>=now())"""%\
                                    (actual_room_type,Room_id))
                                frappe.msgprint(msg="Student Record is updated", title='Update')
                                pass
                            else:
                                frappe.throw("Vacancy Not Avalable")                    
                    else:
                        info=frappe.db.sql("""SELECT * FROM `tabRoom Allotment` WHERE `room_id`="%s" and (`start_date`<= now() and `end_date`>=now())"""%(Room_id))
                        if len(info)==0:
                            previous_room_capacity=doc.previous_room_capacity
                            actual_capacity=doc.actual_capacity
                            if previous_room_capacity==actual_capacity:
                                pass
                            else:
                                frappe.throw("Vacancy Not Avalable")
                        else:
                            frappe.throw("Already Students are allotted presently")
                elif hostel_id!=hostel_df['hostel_id'][0] or hostel_df['room_number'][0]!=room_number:
                    info=''' RM WHERE RM.hostel_id="%s" and RM.room_number="%s" and RM.validity="Functional" '''%(hostel_id,room_number) 
                    Type="General"
                    Ck_df=Room_master_sql(info,Type, doc) # checking for same room no and hostel is present 
                    if len(Ck_df)==0:
                        if hostel_df['validity'][0]==validity:
                            if hostel_df['actual_room_type'][0]==actual_room_type:
                                previous_room_capacity=doc.previous_room_capacity
                                actual_capacity=doc.actual_capacity
                                if previous_room_capacity==actual_capacity:
                                    pass
                                else:
                                    frappe.throw("Vacancy Not Avalable")
                            else:
                                previous_room_capacity=doc.previous_room_capacity
                                actual_capacity=doc.actual_capacity
                                if previous_room_capacity==actual_capacity:
                                    frappe.db.sql("""UPDATE `tabRoom Allotment` SET `room_type`="%s" WHERE `room_id`="%s" and (`start_date`<=now() and `end_date`>=now())"""%\
                                        (actual_room_type,Room_id))
                                    frappe.msgprint(msg="Student Record is updated", title='Update')
                                    pass
                                else:
                                    frappe.throw("Vacancy Not Avalable")                    
                        else:
                            info=frappe.db.sql("""SELECT * FROM `tabRoom Allotment` WHERE `room_id`="%s" and (`start_date`<= now() and `end_date`>=now())"""%(Room_id))
                            if len(info)==0:
                                previous_room_capacity=doc.previous_room_capacity
                                actual_capacity=doc.actual_capacity
                                if previous_room_capacity==actual_capacity:
                                    pass
                                else:
                                    frappe.throw("Vacancy Not Avalable")
                            else:
                                frappe.throw("Already Students are allotted presently")  
                    else:
                        frappe.throw("Hostel and Room No Exits in the system")                    
                else:
                    frappe.throw("Hostel Name or Room Number can't be changed")
            elif len(hostel_df)==0 and len(Ck_df)!=0:
                frappe.throw("Issue in updating Record")    
            else:
                frappe.throw("Hostel Name or Room Number can't be changed")                     


# def update_test(hostel_df,AC_room_type,Ac_Room_capacity,Floor_Number,room_description,validity,actual_room_type,actual_capacity,block,hostel_id): 
#   Hostel_room=frappe.get_doc("Room Masters",hostel_df)
#   if Hostel_room.hostel_id==hostel_id:
#       Hostel_room.room_type_id=AC_room_type
#       Hostel_room.room_capacity=Ac_Room_capacity
#       Hostel_room.floor_number=Floor_Number
#       Hostel_room.room_description=room_description
#       Hostel_room.validity=validity
#       Hostel_room.actual_room_type=actual_room_type
#       Hostel_room.actual_capacity=actual_capacity
#       Hostel_room.block=block
#       Hostel_room.save(    ignore_permissions=True, # ignore write permissions during insert
#                           ignore_version=True # do not create a version record    
#                       )                           
#       frappe.db.commit()  
#   else:
#       frappe.throw("Issue in updating")           

def Room_master_sql(info,Type, doc):
        if Type=="General":
            # Hostel=frappe.db.sql(""" SELECT `name`,`hostel_id`,`room_type_id`,`room_number`,`room_capacity`,`floor_number`,`room_description`,
            #                                 `validity`,`actual_room_type`,`actual_capacity`,`block`  from `tabRoom Masters` """ + info)  

            # SELECT `name`,`hostel_id`,`room_type_id`,`room_number`,`room_capacity`,`floor_number`,`room_description`,`validity`,`actual_room_type`,`actual_capacity`,`block`  from `tabRoom Masters` RM WHERE RM.hostel_id="Kings Palace I" and RM.room_number="1B-02" and RM.validity="Functional"              
            
            hostel_df=pd.DataFrame({
                'Room_doc_id':[],'hostel_id':[],'Acc_room_type':[],'room_number':[],
                'Acc_room_capacity':[],'floor_number':[],'room_description':[],'validity':[],
                'actual_room_type':[],'actual_capacity':[],'block':[]
            })
            s = pd.Series({'Room_doc_id':doc.name,'hostel_id':doc.hostel_id,'Acc_room_type':doc.room_type_id,'room_number':doc.room_number,
                'Acc_room_capacity':doc.room_capacity,'floor_number':doc.floor_number,'room_description':doc.room_description,'validity':doc.validity,
                'actual_room_type':doc.actual_room_type,'actual_capacity':doc.actual_capacity,'block':doc.block})
            for i in s.index:
                hostel_df[i] = s[i]
            # for t in range(len(Hostel)):
            #     s=pd.Series([Hostel[t][0],Hostel[t][1],Hostel[t][2],Hostel[t][3],Hostel[t][4],Hostel[t][5],
            #                 Hostel[t][6],Hostel[t][7],Hostel[t][8],Hostel[t][9],Hostel[t][10]],
            #                         index=['Room_doc_id','hostel_id','Acc_room_type','room_number',
            #                                 'Acc_room_capacity','floor_number','room_description','validity',
            #                                 'actual_room_type','actual_capacity','block'])
            #     hostel_df=hostel_df.append(s,ignore_index=True) 
            return hostel_df



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def room_type_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""SELECT `name` from `tabRoom Type` WHERE `start_date`<=now() and `end_date`>=now()""")



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def room_description_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""SELECT `name` from `tabRoom Description` WHERE `start_date`<=now() and `end_date`>=now()""")
	