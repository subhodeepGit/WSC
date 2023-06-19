# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt


from dataclasses import field
import frappe
from frappe import _
import itertools
from datetime import datetime

def execute(filters=None):
    pe_data , course_schedule_data=get_data(filters)
    get_columns_info=get_columns(course_schedule_data)
    return  get_columns_info,pe_data


def get_data(filters=None):
    to_date=filters.get('to_date')
    from_date=filters.get('from_date')
    academic_term=filters.get('academic_term')
    semester=filters.get('semester')
    
    filt=[]
    if academic_term:
        filt.append(["academic_term","in",tuple(academic_term)])
    if semester:
        filt.append(["program","in",tuple(semester)])
    filt.append(["docstatus","=", 1])


    pe_data = frappe.get_all("Program Enrollment", filters=filt,fields = ["student", "student_name"])

    filter=[]
    if from_date and to_date:
        filter.append(["schedule_date", "between", [from_date,to_date]])
    if semester:
        filt.append(["semester","in",tuple(semester)])

    course_schedule_data = frappe.get_all("Course Schedule", filters=filter, fields=['name','schedule_date'])
    student_attendance_data = frappe.get_all("Student Attendance", ['student','course_schedule','status'])
    print("\n\n\n\n")
    # print(course_schedule_data)
    # print(pe_data)
    c_data=[]
    for t in course_schedule_data:
        c_data.append(t['name'])

    c_data= list(set(c_data))   
    # print(c_data)

    for t in pe_data:
        for j in c_data:
            t['%s'%(j)]=''

    for t in pe_data:
        for d in student_attendance_data:
            if d['student'] in t['student']:
                t['%s'%(d['course_schedule'])]=d['status']


    print(pe_data)
    # head_list = []
    # field_list = []
 
    # for t in course_schedule_data:
    #     head_list.append(t['schedule_date'].strftime("%d-%m-%Y"))
    
    # head_list=list(set(head_list))
    
    # for t in course_schedule_data:
    #     field_list.append(t['name'])

    # field_list=list(set(head_list))

    

    # return pe_data, head_list, field_list
    return pe_data, course_schedule_data

    
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
    # if len(head_name)!=0 and len(head_field_name)!=0:
    #     for (t,d) in zip(head_name, head_field_name):
    #         label=t
    #         field_name=d
    #         columns_add={
    #             "label": _("%s"%(label)),
    #             "fieldname": "%s"%(field_name),
    #             "fieldtype": "Data",
    #             "width":180
    #         }
    #         columns.append(columns_add)

    if len(head_name) != 0:
        for t in head_name:
            field_name=t['name']
            label=t['schedule_date']
            columns_add={
                "label": _("%s"%(label)),
                "fieldname": "%s"%(field_name),
                "fieldtype": "Data",
                "width":180
            }
            columns.append(columns_add)


    return columns