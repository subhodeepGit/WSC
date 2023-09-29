# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


import frappe


def execute(filters=None):
    data = get_data(filters)
    columns = get_columns(filters)

    return columns,data

def get_columns(filters=None):
    return [
    {
        "label": "Centre Name",
        "fieldtype":"Link",
        "fieldname":"center_name",
        "options":"Entrance exam select",
        "width":150
	},
    {
        "label": "Centre",
        "fieldtype":"Data",
        "fieldname":"center",
        "options":"Entrance exam select",
        "width":150
	},
    {
        "label": "Number of Prefered Center",
        "fieldtype":"Data",
        "fieldname":"Centers Prefered",
        "width":150
	},
    
]

def get_data(filters):
    data=[]
    fltr, flt2 = {},[]
    
    if filters.get("academic_year"):
        fltr.update({'academic_year':filters.get("academic_year")})
    if filters.get("academic_term"):
        fltr.update({"academic_term":filters.get("academic_term")})
	
    data=frappe.db.sql('''
		SELECT 
            ECP.center_name ,
        	ECP.center ,
            COUNT(ECP.center) AS QWE 
        FROM 
            `tabExam Centre Preference` ECP 
        RIGHT JOIN 
            `tabStudent Applicant` SA 
    	ON 
            ECP.parent = SA.name 
        WHERE 
            SA.docstatus = 1 AND
            SA.application_status = "Applied" AND
            SA.academic_year = "{academic_year}" AND
            SA.academic_term = "{academic_term}" AND
            SA.department = "{department}" AND
            SA.program_grade = "{course_type}" 
        GROUP BY ECP.center
	'''.format(academic_year = filters['academic_year'] , 
            	academic_term = filters['academic_term'],
                department = filters['department'],
                course_type = filters['program_grade']
				))
    print(data)
	
	
    return data
