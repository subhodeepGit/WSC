# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt


from dataclasses import field
import frappe
from frappe import _
import itertools
from datetime import date, timedelta, datetime

def execute(filters=None):
    pe_data, date_list =get_data(filters)
    get_columns_info=get_columns(date_list)
    return  get_columns_info,pe_data


def get_data(filters=None):
    to_date=filters.get('to_date')
    from_date=filters.get('from_date')
    academic_term=filters.get('academic_term')
    semester=filters.get('semester')
    course=filters.get('course')

    try:
        if from_date > to_date:
            frappe.throw("From Date cannot be greater than To Date")
    except TypeError:
        pass

    filt=[]
    if academic_term:
        filt.append(["academic_term","in",tuple(academic_term)])
    if semester:
        filt.append(["program","in",tuple(semester)])
    filt.append(["docstatus","=", 1])

    pe_data = frappe.get_all("Program Enrollment", filters=filt,fields = ["student", "student_name"])
    print("\n\n\n", pe_data)

    def generate_date_range(from_date, to_date):
        date_range = []
        current_date = datetime.strptime(from_date, '%Y-%m-%d')
        end_date = datetime.strptime(to_date, '%Y-%m-%d')
    
        while current_date <= end_date:
            date_range.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
    
        return date_range

    date_list = generate_date_range(from_date, to_date)
    print("\n\n\n\n",date_list)

    att_filt=[]
    if from_date and to_date==None:
        att_filt.append(["date", ">=", from_date])
    elif to_date and from_date==None:
        att_filt.append(["date", "<=", to_date])
    elif from_date and to_date:
        att_filt.append(["date", "between", [from_date,to_date]])

    student_attendance_data = frappe.get_all("Student Attendance", filters=att_filt, fields=['student','course_schedule','status','date'])
    print("\n\n\n", student_attendance_data)

    c_data=[]
    for t in date_list:
        c_data.append(t)

    c_data= list(set(c_data))   

    for t in pe_data:
        for j in c_data:
            t['%s'%(j)]='Attendance not marked'

    # for j in c_data:
    #     for t in pe_data:
    #         for i in student_attendance_data:
    #             if (t['student'] == i['student']) and (i['date'] == j):
    #                  t[j]='Present'

    

    







    return pe_data, date_list

    
def get_columns(head_name=None):
    columns = [
        {
            "label": _("Student No"),
            "fieldname": "student",
            "fieldtype": "Link",
            "options": "Student",
            "width":180
        },
        {
            "label": _("Student Name"),
            "fieldname": "student_name",
            "fieldtype": "Data",
            "width":160
        },
    ]

    if len(head_name) != 0:
        for t in head_name:
            field_name=t
            columns_add={
                "label": _("%s"%(datetime.strptime(field_name, '%Y-%m-%d').strftime('%d-%m-%Y'))),
                "fieldname": "%s"%(field_name),
                "fieldtype": "Data",
                "width":290
            }
            columns.append(columns_add)


    return columns