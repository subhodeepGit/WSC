# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    data = get_data(filters)
    columns = get_columns(filters)

    return columns,data

def get_columns(filters=None):
    return [
    {
        "label": "Room",
        "fieldtype":"Link",
        "fieldname":"room",
        "options":"Room",
        "width":200
	},
    {
        "label": "Class Duration In Hours",
        "fieldtype":"Data",
        "fieldname":"class_duration",
        # "options":"Student Group",
        "width":100
	},
    {
        "label": "ToT Duration In Hours",
        "fieldtype":"Data",
        "fieldname":"tot_duration",
        # "options":"Student Group",
        "width":100
	},
    {
        "label": "Total Duration",
        "fieldtype":"Data",
        "fieldname":"total_duration",
        # "options":"Student Group",
        "width":100
	},
    {
        "label": "Duration Percentage",
        "fieldtype":"Data",
        "fieldname":"duration_percent",
        # "options":"Student Group",
        "width":100
	},
    
]

def get_data(filters):
    print("\n\n\n\nreport")
    data = []
    total_time = 24
    total_duration = 0
    duration_percent = 0
    fltr, flt2 = {},[]
    
    if filters.get("schedule_date"):
        fltr.update({'schedule_date':filters.get("schedule_date")})

    room = frappe.db.sql("""
        SELECT 
            name AS room
        FROM `tabRoom`
    """, as_dict=1)

    for i in room:
        info = {}
        tot_duration = 0
        class_duration  = 0
        data_tot = frappe.get_all("ToT Class Schedule" , 
                                    {'room_name' : i['room'] , 
                                     'scheduled_date': filters['schedule_date']},
                                    ['name' , 'participant_group_name', 'room_name' ,
                                     'scheduled_date' ,
                                     'from_time' , 'to_time']  
                                )
        
        for  k in data_tot:
            if i['room'] == k['room_name']:
                duration = 0
                duration = k['to_time'] - k['from_time']
                # print("\ntot" ,duration.total_seconds()/3600 , i['room'])
                tot_duration = tot_duration + duration.total_seconds()/3600
                

        # print("\n" , tot_duration , i['room'])
        data_class = frappe.get_all("Course Schedule",
                                    {'room' : i['room'] , 
                                     'schedule_date' : filters['schedule_date']} ,
                                    ['name' , 'student_group' , 'room' ,
                                    'schedule_date' ,
                                     'from_time' , 'to_time']
                                )
        

        for j in data_class:
            duration = 0
            if i['room'] == j['room']:
                duration = j['to_time'] - j['from_time']
                # print("\nclass" ,duration.total_seconds()/3600 , i['room'])
                class_duration = class_duration + duration.total_seconds()/3600
                # print(class_duration)
        
        
        total_duration = tot_duration + class_duration
        duration_percent = round(((total_duration/total_time) * 100) , 2)

        info['room'] = i['room']
        info['class_duration'] = class_duration
        info['tot_duration'] = tot_duration
        info['total_duration'] = total_duration
        info['duration_percent'] = duration_percent

        data.append(info)
    
    return data

        

	