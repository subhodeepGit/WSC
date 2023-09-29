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
    # {
    #     "label": "Student Group",
    #     "fieldtype":"Link",
    #     "fieldname":"student_group",
    #     "options":"Student Group",
    #     "width":100
	# },
    {
        "label": "Class",
        "fieldtype":"Link",
        "fieldname":"class_schedule",
        "options":"Course Schedule",
        "width":170
	},
    {
        "label": "Course",
        "fieldtype":"Link",
        "fieldname":"course",
        "options":"Course",
        "width":100
	},
    {
        "label": "Course Name",
        "fieldtype":"Data",
        "fieldname":"course_name",
        # "options":"Course",
        "width":180
	},
    {
        "label": "From Time for Class",
        "fieldtype":"Time",
        "fieldname":"from_time",
        # "options":"Course",
        "width":100
	},
    {
        "label": "To Time for Class",
        "fieldtype":"Time",
        "fieldname":"to_time",
        # "options":"Course",
        "width":100
	},
    {
        "label": "ToT Class",
        "fieldtype":"Link",
        "fieldname":"class_tot",
        "options":"ToT Class Schedule",
        "width":100
	},
    {
        "label": "ToT Course",
        "fieldtype":"Link",
        "fieldname":"course_tot",
        "options":"Course",
        "width":100
	},
    {
        "label": "ToT Course Name",
        "fieldtype":"Data",
        "fieldname":"course_name_tot",
        # "options":"Course",
        "width":200
	},
    {
        "label": "From Time for ToT",
        "fieldtype":"Time",
        "fieldname":"from_time_tot",
        # "options":"Course",
        "width":100
	},
    {
        "label": "To Time for ToT",
        "fieldtype":"Time",
        "fieldname":"to_time_tot",
        # "options":"Course",
        "width":100
	},
]

def get_data(filters):
    print("\n\n\n\nreport")
    data = []
    fltr, flt2 = {},[]

    if filters.get("schedule_date"):
        fltr.update({'schedule_date':filters.get("schedule_date")})

    room = frappe.db.sql("""
        SELECT 
            name AS room
        FROM `tabRoom`
    """, as_dict=1)

    for i in room:
        
        data_tot = frappe.get_all("ToT Class Schedule" , 
                                    {'room_name' : i['room'] , 
                                     'scheduled_date': filters['schedule_date']},
                                    ['name' , 'participant_group_name', 'room_name' ,
                                     'module_id' , 'module_name' ,
                                     'scheduled_date' , 'duration' ,
                                     'from_time' , 'to_time']  
                                )
        for j in data_tot:
            info2 = {}
            info2['room'] = j['room_name']
            info2['class_tot'] = j['name']
            info2['course_tot'] = j['module_id']
            info2['course_name_tot'] = j['module_name']
            info2['duration'] = j['duration']
            info2['from_time_tot'] = j['from_time']
            info2['to_time_tot'] = j['to_time']
        
            data.append(info2)

        data_class = frappe.get_all("Course Schedule",
                                    {'room' : i['room'] , 
                                     'schedule_date' : filters['schedule_date']} ,
                                    ['name' , 'student_group' , 'room' ,
                                     'course' , 'course_name' ,
                                     'schedule_date' ,
                                     'from_time' , 'to_time']
                                )
        
        for k in data_class:
            info = {} 
            print("\n\n" ,k['name'])
            info['room'] = k['room']
            info['class_schedule'] = k['name']
            info['course'] = k['course']
            info['course_name'] = k['course_name']
            # duration = k['to_time'] - k['from_time']
            info['duration'] = k['to_time'] - k['from_time']
            info['from_time'] = k['from_time']
            info['to_time'] = k['to_time']
            data.append(info)

    # data_tot = frappe.db.sql("""
	# 	SELECT 
    #         tot.name ,
    # 		tot.room_name ,
    #         tot.participant_group_name ,
    #     	tot.module_id ,
    #         tot.module_name ,
    #         tot.scheduled_date ,
    #         tot.from_time ,
    #         tot.to_time 
    #     FROM `tabRoom` room 
    #     INNER JOIN `tabToT Class Schedule` tot
	# 	ON room.name = tot.room_name 
    #     WHERE 
    #         tot.scheduled_date = '{scheduled_date}'
	# """.format(scheduled_date = filters['schedule_date']) , as_dict=1)
	
    # data_class = frappe.db.sql("""
    #     SELECT 
    #         class.name ,
    #         class.student_group , 
    #         class.room , 
    #         class.course ,
    #         class.course_name ,
    #         class.from_time , 
    #         class.to_time  
    #     FROM `tabRoom` room
    #     INNER JOIN `tabCourse Schedule` class
    #     ON room.name = class.room 
    #     WHERE 
    #         schedule_date = '{scheduled_date}'
    # """.format(scheduled_date = filters['schedule_date']) , as_dict=1)
    # print(data_class)
    # # print("\n\n\n", data_tot)

    # room = frappe.db.sql("""
    #     SELECT 
    #         name AS room
    #     FROM `tabRoom`
    # """, as_dict=1)

    # # for i in room:
    # #     data[i['room']] = []
        
        
    # # print("\n" , room)
    # for i in room:
    #     info = {}
    #     info2 = {}
    #     for j in data_class:
    #         if i['room'] == j['room']:
    #             # print(i , j)
    #             info['room'] = i['room']
    #             info['class_schedule'] = j['name']
    #             info['course'] = j['course']
    #             info['course_name'] = j['course_name']
    #             info['from_time'] = j['from_time']
    #             info['to_time'] = j['to_time']
        
    #     data.append(info)
    #     for k in data_tot:
    #         if i['room'] == k['room_name']:
    #             info2['room'] = i['room']
    #             info2['class_tot'] = k['name']
    #             info2['course_tot'] = k['module_id']
    #             info2['course_name_tot'] = k['module_name']
    #             info2['from_time_tot'] = k['from_time']
    #             info2['to_time_tot'] = k['to_time']
    #     data.append(info2)
    #     # print(i)
    # print("\n\n",data)
    return data
	