# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	columns, data = [], []
	data,room_type_data,get_room_description_data=get_data(filters)
	columns=get_columns(room_type_data,get_room_description_data)
	return columns, data


def get_data(filters):
	hostel=filters.get("hostel")
	fil={}
	if hostel:
		fil['name']=hostel
	data=frappe.get_all("Hostel Masters",filters=fil,fields=['name',"hostel_short_name","hostel_type"])
	room_type_data=get_room_type()
	get_room_description_data=get_room_description()
	final_list=[]
	if data:
		for t in data:
			a={}
			a['hostel']=t['name']
			a['hostel_short_name']=t['hostel_short_name']
			a['hostel_type']=t['hostel_type']
			output=frappe.db.count("Room Masters",{"hostel_id":t['name'],"validity":"Functional"})
			a['total_no_of_rooms']=output
			output=frappe.db.sql(""" select sum(actual_capacity)
				 			from `tabRoom Masters` 
				 			where hostel_id = '{hostel}' and validity="Functional" """.format(**{
								"hostel":t['name']
							}),as_dict=True)
			a['total_capacity_of_the_hostel']=output[0]['sum(actual_capacity)']
			output=frappe.db.sql(""" select sum(vacancy)
				 			from `tabRoom Masters` 
				 			where hostel_id = '{hostel}' and validity="Functional" """.format(**{
								"hostel":t['name']
							}),as_dict=True)
			a['total_valency_of_the_hostel']=output[0]['sum(vacancy)']
			if a['total_capacity_of_the_hostel']!=0:
				a["hostel_utilization_report"]=(a['total_valency_of_the_hostel']/a['total_capacity_of_the_hostel'])*100
			else:
				a["hostel_utilization_report"]=0

			for j in room_type_data:
				output=frappe.db.count("Room Masters",{"hostel_id":t['name'],"actual_room_type":j['name']})
				label=j['name']
				label="Total no. of Room "+label
				fieldname=label.replace(" ", "")
				a['%s'%(fieldname)]=output

			for j in get_room_description_data:
				output=frappe.db.count("Room Masters",{"hostel_id":t['name'],"room_description":j['name']})
				label=j['name']
				label=label
				fieldname=label.replace(" ", "")
				a['%s'%(fieldname)]=output

			output=frappe.db.count("Room Allotment",{"hostel_id":t['name'],"allotment_type":"Allotted"})	
			a['total_no_of_students_allotted']=output

			final_list.append(a)


	return final_list,room_type_data,get_room_description_data

def get_room_type():
	data=frappe.db.sql(""" select name from `tabRoom Type`
			   		where  start_date<=now() and  end_date>=now() """,as_dict=True)
	return data

def get_room_description():
	data=frappe.db.sql(""" select name from `tabRoom Description`
			   		where  start_date<=now() and  end_date>=now() """,as_dict=True)
	return data




def get_columns(room_type_data,get_room_description_data):
	columns = [
		{
			"label": _("Hostel"),
			"fieldname": "hostel",
			"fieldtype": "Link",
			"options":"Hostel Masters",
			"width":200
		},
		{
			"label": _("Hostel Short Name"),
			"fieldname": "hostel_short_name",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Hostel Type"),
			"fieldname": "hostel_type",
			"fieldtype": "Link",
			"options":"Hostel Type",
			"width":200
		},
		{
			"label": _("Total No of Rooms"),
			"fieldname": "total_no_of_rooms",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Total Capacity Of The Hostel"),
			"fieldname": "total_capacity_of_the_hostel",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Total No of Students Allotted"),
			"fieldname": "total_no_of_students_allotted",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Total Vacancy Of The Hostel"),
			"fieldname": "total_valency_of_the_hostel",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Hostel Utilization Report"),
			"fieldname": "hostel_utilization_report",
			"fieldtype": "Data",
			"width":200
		},
	]

	if room_type_data:
		for t in room_type_data:
			label=t['name']
			label="Total no. of Room "+label
			fieldname=label.replace(" ", "")
			columns_add={
				"label": _("%s"%(label)),
				"fieldname": "%s"%(fieldname),
				"fieldtype": "Data",
				"width":250
			}
			columns.append(columns_add)


	if get_room_description_data:
		for t in get_room_description_data:
			label=t['name']
			label=label
			fieldname=label.replace(" ", "")
			columns_add={
				"label": _("%s"%(label)),
				"fieldname": "%s"%(fieldname),
				"fieldtype": "Data",
				"width":250
			}
			columns.append(columns_add)	
	return columns
