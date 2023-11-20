# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)  
	return columns, data

def get_data(filters=None):
	room_no=filters.get('room_no')
	from_date=filters.get('from_date')
	to_date=filters.get("to_date")
	data=[]

	filter_data_tot={}
	filter_data=""
	room_data=[]
	filter_data_tot['scheduled_date']=["between", [from_date, to_date]]
	if room_no!=None :
		filter_data="And cs.room='%s' "%(room_no)
		filter_data_tot['room_name']=room_no
		room_data=frappe.get_all("Room",{"name":room_no})
	else:
		room_data=frappe.get_all("Room")	


	date_data=all_date_bwn_from_to_date(from_date,to_date)



	result=frappe.db.sql(""" Select 
							cs.room,cs.student_group,cs.academic_year,cs.academic_term,cs.program,cs.course,
							cs.course_name,cs.school_house,cs.schedule_date,cs.from_time,cs.to_time,sg.programs,sg.program_grade
							from `tabCourse Schedule` as cs
							Join `tabStudent Group` as sg	on sg.name=cs.student_group
					  		WHERE (cs.schedule_date BETWEEN '{from_date}' AND '{to_date}') {filter_data}
							""".format(**{
								"from_date":from_date,
								"to_date":to_date,
								"filter_data":filter_data
							}),as_dict=True)
	

	result_tot=frappe.get_all("ToT Class Schedule",filters=filter_data_tot,fields=['room_name as room','participant_group_name as student_group',"academic_year",
																				'academic_term','course_type as program_grade',"course_id as programs","semester as program",
																				'module_id as course','module_name as course_name','from_time','to_time','scheduled_date as schedule_date'])


	final_list=[]
	for rooms in room_data:
		a=	{
		"room":'%s'%(rooms['name']), "student_group":"","academic_year":"","academic_term":"","course_type":"","course":"",
		"program":"","course":"", "course_name":"", "school_house":"", "schedule_date":"","from_time":"",
		"duration_of_class":"","to_time":"","tot_class":"",
		}
		final_list.append(a)
		for date in date_data:
			for course_schedule in result:
				if course_schedule['room']==rooms['name'] and course_schedule['schedule_date']==date:					
					a=	{
					"room":'', "student_group":"%s"%(course_schedule['student_group']),"academic_year":"%s"%(course_schedule['academic_year']),"academic_term":"%s"%(course_schedule['academic_term']),
					"course_type":"%s"%(course_schedule["program_grade"]),"course":"%s"%(course_schedule["programs"]),"program":"%s"%(course_schedule['program']),
					"module_id":"%s"%(course_schedule['course']), "module_name":"%s"%(course_schedule['course_name']), "school_house":"%s"%(course_schedule['school_house']), 
					"schedule_date":date,"from_time":"%s"%(course_schedule['from_time']),
					"duration_of_class":"%s"%(course_schedule['to_time']-course_schedule['from_time']),"to_time":"%s"%(course_schedule['to_time']),"tot_class":"No",
					}
					final_list.append(a)
			for course_schedule in result_tot:
				if course_schedule['room']==rooms['name'] and course_schedule['schedule_date']==date:					
					a=	{
					"room":'', "student_group":"%s"%(course_schedule['student_group']),"academic_year":"%s"%(course_schedule['academic_year']),"academic_term":"%s"%(course_schedule['academic_term']),
					"course_type":"%s"%(course_schedule["program_grade"]),"course":"%s"%(course_schedule["programs"]),"program":"%s"%(course_schedule['program']),
					"module_id":"%s"%(course_schedule['course']), "module_name":"%s"%(course_schedule['course_name']), "school_house":"", 
					"schedule_date":date,"from_time":"%s"%(course_schedule['from_time']),
					"duration_of_class":"%s"%(course_schedule['to_time']-course_schedule['from_time']),"to_time":"%s"%(course_schedule['to_time']),"tot_class":"Yes",
					}
					final_list.append(a)		


	data=final_list
	return data


def all_date_bwn_from_to_date(from_date,to_date):
	from datetime import timedelta, date,datetime
	from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
	to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
	start_date = from_date
	end_date = to_date
	def daterange(start_date, end_date):
		for n in range(int ((end_date - start_date).days) + 1):
			yield start_date + timedelta(n)
	
	
	date_data=[]
	for single_date in daterange(start_date, end_date):
		# date_data.append(single_date.strftime("%Y-%m-%d"))
		date_data.append(single_date)
	
	return date_data		






def get_columns(filters=None):
    columns = [
        {
            "label": _("Room No"),
            "fieldname": "room",
            "fieldtype": "Link",
            "options": "Room",
            "width":180
        },
        {
            "label": _("Student Group"),
            "fieldname": "student_group",
			"fieldtype": "Data",
            # "fieldtype": "Link",
			# "options": "Student Group",
            "width":160
        },
		{
            "label": _("Schedule Date"),
            "fieldname": "schedule_date",
            "fieldtype": "data",
            "width":160 
        },
        {
            "label": _("Academic Year"),
            "fieldname": "academic_year",
            "fieldtype": "Link",
			"options": "Academic Year",
            "width":160 
        },
		{
            "label": _("Academic Term"),
            "fieldname": "academic_term",
            "fieldtype": "Link",
			"options": "Academic Term",
            "width":160 
        },
        {
            "label": _("Course Type"),
            "fieldname": "course_type",
            "fieldtype": "Link",
			"options":"Program Grades",
            "width":160 
        },
        {
            "label": _("Course ID"),
            "fieldname": "course",
            "fieldtype": "Link",
			"options":"Programs",
            "width":160 
        },
		{
            "label": _("Semester"),
            "fieldname": "program",
            "fieldtype": "Link",
			"options":"Program",
            "width":160 
        },
		{
            "label": _("Module ID"),
            "fieldname": "module_id",
            "fieldtype": "Link",
			"options":"Course",
            "width":160 
        },
		{
            "label": _("Module Name"),
            "fieldname": "module_name",
            "fieldtype": "data",
            "width":160 
        }, 	   
		{
            "label": _("Class"),
            "fieldname": "school_house",
            "fieldtype": "Link",
			"options":"School House",
            "width":160 
        },

		{
            "label": _("From Time"),
            "fieldname": "from_time",
            "fieldtype": "data",
            "width":160 
        },        
		{
            "label": _("To Time"),
            "fieldname": "to_time",
            "fieldtype": "data",
            "width":160 
        },
		{
            "label": _("Duration Of Class"),
            "fieldname": "duration_of_class",
            "fieldtype": "data",
            "width":160 
        },#
		{
            "label": _("TOT Class"),
            "fieldname": "tot_class",
            "fieldtype": "data",
            "width":160 
        }#
    ]
    return columns