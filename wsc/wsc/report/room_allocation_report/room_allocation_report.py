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
	print("\n\n\n\n\n\n")
	room_no=filters.get('room_no')
	from_date=filters.get('from_date')
	to_date=filters.get("to_date")
	data=[]
	# print(room_no,from_date,to_date)
	filter_data={}
	room_data=[]
	filter_data['schedule_date']=["between", [from_date, to_date]]
	if room_no!=None :
		filter_data['room']=room_no
		room_data=frappe.get_all("Room",{"name":room_no})
	else:
		room_data=frappe.get_all("Room")	


	date_data=all_date_bwn_from_to_date(from_date,to_date)
	result = frappe.get_all("Course Schedule", filters=filter_data,
						 						fields=['room','student_group','academic_year',"academic_term","program",
				  						"course","course_name","school_house","schedule_date","from_time","to_time"],
										order_by="from_time asc")
	# final_list=[]
	# for t in room_data:
	# 	a={'room':t['name'],'student_group':'','academic_year':'',"academic_term":'',"program":'',
	#  		"course":'',"course_name":'',"school_house":'',"schedule_date":'',"from_time":'',"to_time":''}
	# 	{
    #         "fieldname": "room", "fieldname": "student_group","fieldname": "academic_year","fieldname": "academic_term","fieldname": "course_type","fieldname": "course",
	# 		"fieldname": "program","fieldname": "course", "fieldname": "course_name", "fieldname": "school_house", "fieldname": "schedule_date","fieldname": "from_time",
	# 		"fieldname": "to_time",
    #     },
	# 	{
    #         "label": _("Duration Of Class"),
    #         "fieldname": "duration_of_class",
    #         "fieldtype": "data",
    #         "width":160 
    #     },#
	# 	{
    #         "label": _("TOT Class"),
    #         "fieldname": "tot_class",
    #         "fieldtype": "data",
    #         "width":160 
    #     }
	# 	final_list.append(a)
	# 	for j in result:
	# 		if t['name']==j['room']:
	# 			print(j)

	# data=result
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
		date_data.append(single_date.strftime("%Y-%m-%d"))
	
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
            "fieldtype": "Link",
			"options": "Student Group",
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
            "label": _("Course Name"),
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
            "fieldname": "course",
            "fieldtype": "Link",
			"options":"Course",
            "width":160 
        },
		{
            "label": _("Module Name"),
            "fieldname": "course_name",
            "fieldtype": "data",
			"options":"Programs",
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
            "label": _("Schedule Date"),
            "fieldname": "schedule_date",
            "fieldtype": "data",
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