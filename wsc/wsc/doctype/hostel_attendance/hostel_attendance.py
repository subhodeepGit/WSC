# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
import pandas as pd
import datetime
from datetime import datetime,date



class HostelAttendance(Document):
    # @frappe.whitelist()
    def before_save(doc):
        allotment_date_validation(doc)
        Al_no=doc.room_allotment_no
        Date_att=doc.attendance_date

        info="""WHERE `room_allotment_no`="%s" and `attendance_date`="%s" and `docstatus`!=2 """%(Al_no,Date_att)
        AT_info=Attendence_info(info,"Genaral")
        try:
            if len(AT_info)==0:
                info=""" WHERE `allotment_number`="%s" and (`start_date`<="%s" and `end_date`>="%s") and (`workflow_state`="Approved" and `docstatus`=1) """%(Al_no,Date_att,Date_att)
                leave_info=Attendence_info(info,"Leave")            

                if len(leave_info)==0:
                    if Date_att <= datetime.now():
                        pass
                    else:
                        frappe.throw("Attendance can not be marked for future dates")
                else:
                    frappe.throw("Studnet is in leave from %s to %s long leave doc No-%s"%(leave_info["start_date"][0],
                                    leave_info["end_date"][0],leave_info["LL_doc_no"][0]))
            else:
                frappe.throw("Attendance is already registered for the %s doc No- %s"%(Date_att,AT_info["AT_doc_no"][0]))
        except:
            Date_att=datetime.strptime(Date_att, '%Y-%m-%d').date() 
            if len(AT_info)==0:
                info=""" WHERE `allotment_number`="%s" and (`start_date`<="%s" and `end_date`>="%s") and (`workflow_state`="Approved" and `docstatus`=1) """%(Al_no,Date_att,Date_att)
                leave_info=Attendence_info(info,"Leave")            

                if len(leave_info)==0:
                    if Date_att <= date.today():
                        pass
                    else:
                        frappe.throw("Attendance can not be marked for future dates")
                else:
                    frappe.throw("Studnet is in leave from %s to %s long leave doc No-%s"%(leave_info["start_date"][0],
                                    leave_info["end_date"][0],leave_info["LL_doc_no"][0]))
            else:
                frappe.throw("Attendance is already registered for the %s doc No- %s"%(Date_att,AT_info["AT_doc_no"][0]))

    # @frappe.whitelist()
    def on_submit(doc):
        Al_no=doc.room_allotment_no
        Date_att=doc.attendance_date
        
        info=""" WHERE `allotment_number`="%s" and (`start_date`<="%s" and `end_date`>="%s") and `workflow_state`="Approved" """%(Al_no,Date_att,Date_att)
        leave_info=Attendence_info(info,"Leave")
        try:
            if len(leave_info)==0:
                if Date_att <= datetime.now():
                    pass
                else:
                    frappe.throw("Attendance can not be marked for future dates")
            else:
                frappe.throw("Studnet is in leave from %s to %s long leave doc No-%s"%(leave_info["start_date"][0],
                                    leave_info["end_date"][0],leave_info["LL_doc_no"][0]))
        except:
            Date_att=datetime.strptime(Date_att, '%Y-%m-%d').date()   
            if len(leave_info)==0:
                if Date_att <= date.today():
                    pass
                else:
                    frappe.throw("Attendance can not be marked for future dates")
            else:
                frappe.throw("Studnet is in leave from %s to %s long leave doc No-%s"%(leave_info["start_date"][0],
                                    leave_info["end_date"][0],leave_info["LL_doc_no"][0]))                        







def Attendence_info(info,flag):
    if flag=="Genaral":
        Att_info=frappe.db.sql("""SELECT `name`,`docstatus`,`status`,`attendance_date`,`room_allotment_no`,`student_name`,`hostel`,
                `room_no`,`room_id` from `tabHostel Attendance`  """+info)
        df1=pd.DataFrame({
			"AT_doc_no":[],"docstatus":[],"status":[],"attendance_date":[],"room_allotment_no":[],"student_name":[],"hostel":[],
			"room_no":[],"room_id":[]
		})
        for t in range(len(Att_info)):
            s=pd.Series([Att_info[t][0],Att_info[t][1],Att_info[t][2],Att_info[t][3],Att_info[t][4],Att_info[t][5],
						Att_info[t][6],Att_info[t][7],Att_info[t][8]],
								index=["AT_doc_no","docstatus","status","attendance_date","room_allotment_no","student_name","hostel",
			                            "room_no","room_id"])
            df1=df1.append(s,ignore_index=True)		
        return df1
    elif flag=="Leave":
        leave_info=frappe.db.sql("""SELECT `name`,`docstatus`,`allotment_number`,`student`,`start_date`,`end_date` from `tabStudent Leave Process`  """+info)
        df1=pd.DataFrame({
			"LL_doc_no":[],"docstatus":[],"allotment_number":[],"student":[],"start_date":[],"end_date":[]
		})
        for t in range(len(leave_info)):
            s=pd.Series([leave_info[t][0],leave_info[t][1],leave_info[t][2],leave_info[t][3],leave_info[t][4],leave_info[t][5]],
								index=["LL_doc_no","docstatus","allotment_number","student","start_date","end_date"])
            df1=df1.append(s,ignore_index=True)		
        return df1    


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):

	if frappe.session.user == "Administrator":
		info=""
	else:
		User=frappe.session.user
		emp_id=frappe.get_all("Employee",{"user_id":User},["name"])
		Emp_al=frappe.db.sql("""
				SELECT `hostel_masters` from `tabEmployee Hostel Allotment` WHERE employees="%s" and
				(`start_date`<=now() and `end_date`>=now())"""%(emp_id[0]['name']))
		if 	Emp_al:	
			if len(Emp_al)==1:
				info="""and hostel_id="%s" """%(Emp_al[0][0])
			else:
				hostel=[]
				for t in range(len(Emp_al)):
					hostel.append(Emp_al[0][t])
				hostel=str(tuple(hostel))	
				info="""and hostel_id in """+hostel
		else:
			frappe.throw("No Employee is allotted to the hostel")				
	return frappe.db.sql("""
		SELECT `name`,`student`,`student_name`,`hostel_id` FROM `tabRoom Allotment` WHERE (`start_date` <= now() AND `end_date` >= now()) 
		and (`allotment_type`!="Hostel suspension" and `allotment_type`!="Suspension" and `allotment_type`!="Debar" and 
		`allotment_type`!="University Suspension" and `allotment_type`!="School Suspension") and `docstatus`=1 
	"""+info
	)	

def allotment_date_validation(doc):
    al_data=frappe.get_all("Room Allotment",filters=[["name","=",doc.room_allotment_no]],fields=["name","start_date","end_date"])                                            
    if al_data:
        Date_att=doc.attendance_date
        if type(Date_att)==str:
            Date_att=datetime.strptime(Date_att,'%Y-%m-%d').date() 
        else:
            Date_att=Date_att.date()    

        if al_data[0]['start_date'] > Date_att:
            frappe.throw("Student is not alloted for this date. Please check room allotment date")
        
        if al_data[0]['end_date'] < Date_att:
            frappe.throw("Student is not alloted for this date. Please check room allotment date")
    
