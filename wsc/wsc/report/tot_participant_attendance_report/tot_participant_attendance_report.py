# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt


from dataclasses import field
import frappe
from frappe import _
import itertools
from datetime import datetime

def execute(filters=None):
    result_list , course_schedule_data=get_data(filters)
    get_columns_info=get_columns(course_schedule_data)
    return  get_columns_info,result_list


def get_data(filters=None):
    to_date=filters.get('to_date')
    from_date=filters.get('from_date')
    participant_group=filters.get('participant_group')

    try:
        if from_date > to_date:
            frappe.throw("From Date cannot be greater than To Date")
    except TypeError:
        pass
    
    pg_filt=[]
    result_list = []
    course_schedule_data=[]
    if participant_group:
        pg_filt.append(["parent","in",tuple(participant_group)])
        pg_data = frappe.get_all("Participant Table", filters=pg_filt,fields = ["parent","participant", "participant_name"])

        filt=[]
        if participant_group:
            filt.append(["participant_group_id","in",tuple(participant_group)])
        if from_date and to_date==None:
            filt.append(["scheduled_date", ">=", from_date])
        elif to_date and from_date==None:
            filt.append(["scheduled_date", "<=", to_date])
        elif from_date and to_date:
            filt.append(["scheduled_date", "between", [from_date,to_date]])
        filt.append(["is_canceled", "=", 0])


        course_schedule_data = frappe.get_all("ToT Class Schedule", filters=filt,fields = ["participant_group_id", "scheduled_date", "name", "module_id", "module_name", "from_time", "to_time", "attendance_taken"])

        att_filt=[]
        if participant_group:
            att_filt.append(["participant_group","in",tuple(participant_group)])
        if from_date and to_date==None:
            att_filt.append(["date", ">=", from_date])
        elif to_date and from_date==None:
            att_filt.append(["date", "<=", to_date])
        elif from_date and to_date:
            att_filt.append(["date", "between", [from_date,to_date]])
        filt.append(["docstatus","=", 1])


        participant_attendance_data = frappe.get_all("ToT Participant Attendance", filters=att_filt, fields=["participant_group","participant_id","participant_name","date","status","class_schedule"])        

        for participant_data in pg_data:
            participant_dict = {
                'parent': participant_data['parent'],
                'participant': participant_data['participant'],
                'participant_name': participant_data['participant_name']
            }

            for attendance_data in participant_attendance_data:
                if attendance_data['participant_id'] == participant_data['participant']:
                    status_key = f"{attendance_data['class_schedule']}"
                    participant_dict[status_key] = attendance_data['status']

            result_list.append(participant_dict)

        for t in course_schedule_data:
            flag="No"
            for j in result_list:
                if t['name'] in j:
                    flag="Yes"
                    break
            if flag=="Yes":    
                t['class_conducted']="Yes"
            else:
                t['class_conducted']="No"


        module_names = [entry['name'] for entry in course_schedule_data]

        for entry in result_list:
            for module_name in module_names:
                if module_name not in entry:
                    entry[module_name] = 'Attendance not marked'

        # Iterate through result_list and update the attendance status
        for entry in result_list:
            for key in entry.keys():
                if key.startswith('TCS-') and entry[key] == 'Attendance not marked':
                    # Find the corresponding schedule entry
                    schedule_entry = next((s for s in course_schedule_data if s['name'] == key and s['class_conducted'] == 'Yes'), None)
                    if schedule_entry:
                        entry[key] = 'Absent'

        # Attendance Analysis                

        scheduled_classes = {}
        present_classes = {}

        for record in result_list:
            student_id = record['participant']
            for key, value in record.items():
                if key.startswith('TCS-'):
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
        
        for record in result_list:
            student_id = record['participant']
            num_classes = scheduled_classes.get(student_id, 0)
            if student_id in present_classes:
                percentage = round((present_classes[student_id] / num_classes) * 100, 2)
            else:
                percentage = 0.0
            record['percentage'] = f"{percentage}%"
            record['total_classes_attended'] = present_classes.get(student_id, 0)
            record['total_classes_conducted'] = scheduled_classes.get(student_id, 0)


    return result_list, course_schedule_data

    
def get_columns(head_name=None):
    columns = [
        {
            "label": _("Participant No"),
            "fieldname": "participant",
            "fieldtype": "Link",
            "options": "ToT Participant",
            "width":180
        },
        {
            "label": _("Participant Name"),
            "fieldname": "participant_name",
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
            label='%s|%s[%s(%s to %s)]'%(t['name'],t['module_name'],t['scheduled_date'].strftime("%d-%m-%Y"),rounded_from_time,rounded_to_time)
            columns_add={
                "label": _("%s"%(label)),
                "fieldname": "%s"%(field_name),
                "fieldtype": "Data",
                "width":400
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