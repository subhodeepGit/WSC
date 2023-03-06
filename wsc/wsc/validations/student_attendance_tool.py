import frappe

@frappe.whitelist()
def get_student_records(building,hostel_room=None):
    student_list=[]
    count=1
    fltr={"building":building, 'docstatus':1}
    fltr2={"building":building, 'docstatus':1}
    if hostel_room:
        fltr.update({"to_room":hostel_room})
        fltr2.update({"room":hostel_room})
    deallotment_list = [s.student for s in frappe.db.get_list("Hostel Deallotment",fltr2, 'student')]
    for st in frappe.get_all("Hostel Allotment",filters=fltr,fields=['student','student_name']):
        is_debarred=False
        for d in frappe.get_all("Disciplinary Complaints",{'student':st.student,'complaint_status':"Action Taken",'action':"Debarred","docstatus":1}):
            is_debarred=True
        if not is_debarred and st.student not in deallotment_list:
            student_list.append(st.update({"group_roll_number":count}))
            count+=1
    return student_list

@frappe.whitelist()
def get_employees(date, department = None, branch = None):
    student_list = []
    count=1
    filters = {"start_date": ["<=", date],"end_date": [">=", date],"allotment_type":"Allotted"}
    for field, value in {'hostel_id': department,'room_id': branch}.items():
        if value:
            filters[field] = value	
    for stu in frappe.get_list("Room Allotment", fields=["student","student_name"],filters=filters,order_by="room_number"):
            roll_no=frappe.get_all("Student",filters={"name":stu['student']},fields=['roll_no'])
            if roll_no:
                stu['roll_no']=roll_no[0]['roll_no']
            else:
               stu['roll_no']=""
            student_list.append(stu.update({"group_roll_number":count}))
            count+=1
    return student_list