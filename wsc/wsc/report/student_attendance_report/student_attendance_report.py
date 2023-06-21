# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt


from dataclasses import field
import frappe
from frappe import _
import itertools
from datetime import datetime
import copy

def execute(filters=None):
    pe_data , course_schedule_data=get_data(filters)
    get_columns_info=get_columns(course_schedule_data)
    return  get_columns_info,pe_data


def get_data(filters=None):
    to_date=filters.get('to_date')
    from_date=filters.get('from_date')
    academic_term=filters.get('academic_term')
    semester=filters.get('semester')
    course=filters.get('course')
    filt=[]
    if academic_term:
        filt.append(["academic_term","in",tuple(academic_term)])
    if semester:
        filt.append(["program","in",tuple(semester)])
    filt.append(["docstatus","=", 1])


    pe_data = frappe.get_all("Program Enrollment", filters=filt,fields = ["student", "student_name"])

    filter=[]
    if from_date and to_date==None:
        filter.append(["schedule_date", ">=", from_date])
    elif to_date and from_date==None:
        filter.append(["schedule_date", "<=", to_date])
    elif from_date and to_date:
        filter.append(["schedule_date", "between", [from_date,to_date]])
    if course:
        filter.append(["course","in",tuple(course)])

    course_schedule_data = frappe.get_all("Course Schedule", filters=filter, fields=['name','schedule_date','from_time','to_time'])
    student_attendance_data = frappe.get_all("Student Attendance", ['student','course_schedule','status'])
    print(course_schedule_data)
    # print(pe_data)
    c_data=[]
    for t in course_schedule_data:
        c_data.append(t['name'])

    c_data= list(set(c_data))   
    # print(c_data)

    for t in pe_data:
        for j in c_data:
            t['%s'%(j)]='Attendance not marked'

    for t in pe_data:
        for d in student_attendance_data:
            if d['student'] in t['student']:
                t['%s'%(d['course_schedule'])]=d['status']



    scheduled_classes = {}
    present_classes = {}

    for record in pe_data:
        student_id = record['student']
        for key, value in record.items():
            if key.startswith('EDU-CSH-'):
                if value != 'Attendance not marked':
                    if student_id in scheduled_classes:
                        scheduled_classes[student_id] += 1
                    else:
                        scheduled_classes[student_id] = 1
                    if value == 'Present':
                        if student_id in present_classes:
                            present_classes[student_id] += 1
                        else:
                            present_classes[student_id] = 1
    print("\n\n\n\n")
    print(scheduled_classes)
    print("\n\n\n\n")
    print(present_classes)
    
    for record in pe_data:
        student_id = record['student']
        num_classes = scheduled_classes.get(student_id, 0)
        if student_id in present_classes:
            percentage = round((present_classes[student_id] / num_classes) * 100, 2)
        else:
            percentage = 0.0
        record['percentage'] = percentage
        record['total_classes_attended'] = present_classes[student_id]
        record['total_classes_conducted'] = scheduled_classes[student_id]



    print("\n\n\n\n")
    print(pe_data)
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

    if len(head_name) != 0:
        for t in head_name:
            field_name=t['name']
            from_time_string = "%s"%t['from_time']
            to_time_string = "%s"%t['to_time']
            try:
                from_time_object = datetime.strptime(from_time_string, '%H:%M:%S.%f')
            except ValueError:
                from_time_object = datetime.strptime(from_time_string, '%H:%M:%S')
            try:
                to_time_object = datetime.strptime(to_time_string, '%H:%M:%S.%f')
            except ValueError:
                to_time_object = datetime.strptime(to_time_string, '%H:%M:%S')
            rounded_from_time = from_time_object.strftime("%H:%M")
            rounded_to_time = to_time_object.strftime("%H:%M")
            label='%s(%s to %s)'%(t['schedule_date'].strftime("%d-%m-%Y"),rounded_from_time,rounded_to_time)
            columns_add={
                "label": _("%s"%(label)),
                "fieldname": "%s"%(field_name),
                "fieldtype": "Data",
                "width":250
            }
            columns.append(columns_add)

    total_classes_attended={
        "label": _("Total Classes Attended"),
        "fieldname": "total_classes_attended",
        "fieldtype": "Data",
        "width":180
    }
    total_classes_conducted={
        "label": _("Total Classes Conducted"),
        "fieldname": "total_classes_conducted",
        "fieldtype": "Data",
        "width":180
    }
    percentage={
        "label": _("Attendance Percentage"),
        "fieldname": "percentage",
        "fieldtype": "Data",
        "width":180
    }
    columns.append(total_classes_conducted)
    columns.append(total_classes_attended)
    columns.append(percentage)

    return columns