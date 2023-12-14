# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime

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
        "width":180
	},
    {
        "label": "Total Time",
        "fieldtype":"Data",
        "fieldname":"total_time",
        # "options":"Room",
        "width":100
    },
    {
        "label": "Class Scheduled",
        "fieldtype":"Data",
        "fieldname":"total_classes",
        # "options":"Room",
        "width":140
    },
    {
        "label": "Class Done",
        "fieldtype":"Data",
        "fieldname":"classes_completed",
        # "options":"Room",
        "width":140
    },
    {
        "label": "Expected Class Dur.(Hrs)",
        "fieldtype":"Data",
        "fieldname":"class_duration",
        # "options":"Student Group",
        "width":180
	},
    {
        "label": "Actual Class Dur.(Hrs)",
        "fieldtype":"Data",
        "fieldname":"class_duration_actual",
        # "options":"Student Group",
        "width":160
	},
    {
        "label": "Expected Class Dur(%)",
        "fieldtype":"Data",
        "fieldname":"class_duration_percent",
        # "options":"Room",
        "width":170
    },
    {
        "label": "Actual Class Dur(%)",
        "fieldtype":"Data",
        "fieldname":"class_duration_percent_actual",
        # "options":"Student Group",
        "width":160
	},
    {
        "label": "ToT Class Scheduled",
        "fieldtype":"Data",
        "fieldname":"total_tot_classes",
        # "options":"Room",
        "width":160
    },
    {
        "label": "ToT Class Done",
        "fieldtype":"Data",
        "fieldname":"tot_classes_completed",
        # "options":"Room",
        "width":140
    },
    {
        "label": "Expected ToT Duration(Hrs)",
        "fieldtype":"Data",
        "fieldname":"tot_duration",
        # "options":"Student Group",
        "width":200
	},
    {
        "label": "Expected ToT Duration(%)",
        "fieldtype":"Data",
        "fieldname":"tot_duration_percent",
        # "options":"Student Group",
        "width":200
	},
    {
        "label": "Actual ToT Duration(Hrs)",
        "fieldtype":"Data",
        "fieldname":"tot_duration_actual",
        # "options":"Student Group",
        "width":200
	},
    {
        "label": "Actual ToT Duration(%)",
        "fieldtype":"Data",
        "fieldname":"tot_duration_percent_actual", ##
        # "options":"Student Group",
        "width":200
	},
    {
        "label": "Expected Total Duration(Hrs)",
        "fieldtype":"Data",
        "fieldname":"total_duration",
        # "options":"Student Group",
        "width":210
	},
    {
        "label": "Actual Total Duration(Hrs)",
        "fieldtype":"Data",
        "fieldname":"total_duration_actual",
        # "options":"Student Group",
        "width":210
	},
    {
        "label": "Expected Duration(%)",
        "fieldtype":"Data",
        "fieldname":"duration_percent",
        # "options":"Student Group",
        "width":180
	},
    {
        "label": "Actual Duration(%)",
        "fieldtype":"Data",
        "fieldname":"duration_percent_actual",
        # "options":"Student Group",
        "width":180
	},
    
]

def get_data(filters):
    
    data = []
    daily_hrs = float(filters['daily_hrs'])

    total_no_of_hr = ((datetime.strptime(filters['to_date'] , '%Y-%m-%d') - datetime.strptime(filters['from_date'] , '%Y-%m-%d')).days)*daily_hrs
    
    total_time=total_no_of_hr
    print(total_time)
    total_duration = 0
    total_duration_actual = 0
    duration_percent = 0
    duration_percent_actual = 0
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

        total_tot_count = 0
        actual_tot_duration = 0
        tot_duration = 0
        tot_duration_percent = 0
        tot_duration_percent_actual = 0
        tot_count = 0


        total_class_count = 0
        actual_class_duration = 0
        class_duration  = 0
        class_duration_percent = 0
        class_duration_percent_actual = 0
        class_count = 0

        ## Attendance Data fetch class
        attendance_data_class = frappe.db.sql("""
            SELECT 
                class_atten.name, 
                class_atten.date, 
                class_atten.student_name, 
                class_atten.student_group, class_atten.course_schedule, 
                class.room 
            FROM 
                `tabStudent Attendance` class_atten
            INNER JOIN 
                `tabCourse Schedule` class 
            ON 
                class_atten.course_schedule = class.name 
            WHERE 
                class_atten.date BETWEEN '{from_date}' AND '{to_date}' GROUP BY class_atten.date
        """.format(from_date = filters['from_date']  , to_date = filters['to_date']), as_dict=1)

        # print(attendance_data_class , "\n")
        ## Attendance Data fetch tot
        attendance_data_tot = frappe.db.sql("""
            SELECT 
                tot_atten.name ,
                tot_atten.date ,
                tot_atten.select_course ,
                tot_atten.module_name , 
                tot_atten.semester ,
                tot_atten.class_schedule , 
                tot_class.room_name 
            FROM 
                `tabToT Participant Attendance`tot_atten 
            INNER JOIN 
                `tabToT Class Schedule`tot_class 
            ON tot_atten.class_schedule = tot_class.name 
            WHERE tot_atten.date BETWEEN '{from_date}' AND '{to_date}' GROUP BY tot_atten.date;
        """.format(from_date = filters['from_date']  , to_date = filters['to_date']), as_dict=1)

        print(attendance_data_tot , "\n")
        ## data fetch tot
        data_tot = frappe.db.sql("""
            SELECT 
                name ,
                participant_group_name ,
                room_name ,
                scheduled_date ,
                from_time , to_time ,
                semester ,
                course_id , course_type ,
                module_id , module_name 
            FROM `tabToT Class Schedule` 
            WHERE 
                room_name = '{room}' AND
                scheduled_date BETWEEN '{from_date}' AND '{to_date}'
        """.format(room = i['room'] , from_date = filters['from_date']  , to_date = filters['to_date']), as_dict=1)

        tot_count = 0
        for  k in data_tot:
            if i['room'] == k['room_name']:
                
                duration = 0
                duration_actual = 0

                total_tot_count = total_tot_count + 1

                for n in attendance_data_tot:

                    if n['date'] == k['scheduled_date'] and n['class_schedule'] == k['name'] and k['room_name'] == n['room_name']:

                        duration_actual = k['to_time'] - k['from_time']

                        actual_tot_duration = actual_tot_duration + duration_actual.total_seconds()/3600
                        tot_count = tot_count + 1;    

                duration = k['to_time'] - k['from_time']

                tot_duration = tot_duration + duration.total_seconds()/3600
                
        ## data fetch classtotal_classes
        data_class = frappe.db.sql("""
            SELECT 
                class.name ,
                class.student_group ,
                class.room ,
                class.schedule_date ,
                class.program ,
                class.course , class.course_name ,
                class.from_time,
                class.to_time,
                group_alias.program_grade 
            FROM 
                `tabCourse Schedule` class INNER JOIN `tabStudent Group` group_alias 
            ON class.student_group = group_alias.name 
            WHERE 
                class.room = '{room}' AND
                class.schedule_date BETWEEN '{from_date}' AND '{to_date}';
        """.format(room = i['room'] , from_date = filters['from_date']  , to_date = filters['to_date']),as_dict=1)
        
        
        for j in data_class:
        
            if i['room'] == j['room']:

                duration = 0
                duration_actual = 0

                total_class_count = total_class_count + 1
                for m in attendance_data_class:
        
                    if m['date'] == j['schedule_date'] and m['course_schedule'] == j['name'] and m['room'] == j['room']:
        
                        duration_actual = j['to_time'] - j['from_time']
        
                        actual_class_duration = actual_class_duration + duration_actual.total_seconds()/3600
                        class_count = class_count + 1; 
                
                
                
                duration = j['to_time'] - j['from_time']

                class_duration = class_duration + duration.total_seconds()/3600      


        ## Duration percent class        
        class_duration_percent = round(((class_duration/total_time) * 100) , 2)
        class_duration_percent_actual = round(((actual_class_duration/total_time) * 100) , 2)

        ## Duration percent tot
        tot_duration_percent = round(((tot_duration/total_time) * 100) , 2)
        tot_duration_percent_actual = round(((actual_tot_duration/total_time) * 100) , 2)

        ## Duration Expected
        total_duration = tot_duration + class_duration
        duration_percent = round(((total_duration/total_time) * 100) , 2)
        
        ## Duration Actual
        total_duration_actual = actual_class_duration + actual_tot_duration
        duration_percent_actual = round(((total_duration_actual/total_time) * 100) , 2)
        
        info['room'] = i['room']

        ## Scheduled Classes
        info['classes_completed'] = class_count
        info['tot_classes_completed'] = tot_count

        ##Total Time
        info['total_time'] = total_time

        ## Classes Taken
        info['total_classes'] = total_class_count
        info['total_tot_classes'] = total_tot_count

        ## Class Duration
        info['class_duration'] = class_duration
        info['class_duration_actual'] = actual_class_duration

        ## Class Duration Percent
        info['class_duration_percent'] = class_duration_percent
        info['class_duration_percent_actual'] = class_duration_percent_actual

        ## TOT Class Duration
        info['tot_duration'] = tot_duration
        info['tot_duration_actual'] = actual_tot_duration

        ## TOT Class Duration Percent
        info['tot_duration_percent'] = tot_duration_percent
        info['tot_duration_percent_actual'] = tot_duration_percent_actual
        
        ## Total Duration
        info['total_duration'] = total_duration
        info['total_duration_actual'] = total_duration_actual

        ## Duration Percent
        info['duration_percent'] = duration_percent
        info['duration_percent_actual'] = duration_percent_actual

        # print(info, "\n  info")
        data.append(info)
    
    return data

        

	