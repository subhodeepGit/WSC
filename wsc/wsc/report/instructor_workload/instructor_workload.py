# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	data,label = get_data(filters)
	columns = get_columns(label)
	return columns, data

def get_data(filters):

	fltr = {}
	if filters.get("academic_year"):
		fltr.update({"academic_year":filters.get("academic_year")})
	if filters.get("instructor"):
		fltr.update({"instructor":filters.get("instructor")})

	#labels will be Total Classes Scheduled , Total Classes Taken, Academic Year

	label = list(fltr.keys())
	main_data=[]
	#getting the student group from course schedule for the instructor
	st_group = frappe.get_all("Course Schedule",{"instructor":filters.get("instructor")},['student_group'])
	#get the employee joining date from instructor name

	emp_id = frappe.get_all("Instructor",{"name":filters.get("instructor")},["employee"])
	if len(emp_id)>0:
		emp_id = emp_id[0].employee
		emp_joining_date = frappe.get_all("Employee",{"name":emp_id},["date_of_joining"])
		if len(emp_joining_date)>0:
			emp_joining_date=emp_joining_date[0]["date_of_joining"]

			academic_years = frappe.db.sql("""Select name from `tabAcademic Year` where year_start_date>%s or year_end_date>%s""",(emp_joining_date,emp_joining_date))
			print("\n\n\n\n\nAcademic Year")
			if len(academic_years)>0:
				
				#for total classes scheduled
				for item in academic_years:
					final_data = {}
					print("\n\n\n\nitems")
					print(item)
					final_data.update({"academic_year":item[0]})
					stg = frappe.get_all("Student Group",{"academic_year":item[0]},["name"])
					print("\n\n\n\nstg")
					print(stg)
					if stg :
						count = 0
						for i in stg :

							classes = frappe.db.sql("""Select count(*) from `tabCourse Schedule` where instructor = %s and student_group = %s""",(filters.get("instructor"),i["name"]))
							print("\n\n\n\n\nClasses")
							print(classes)
							classes = classes[0][0]
							count = count+classes
						print("\n\n\n\nCounts")
						print(count)
						final_data.update({"total_scheduled_classes":count})
						date_ranges = frappe.get_all("Academic Year",{"name":item[0]},["year_start_date","year_end_date"])

						if len(date_ranges)>0 :
						
							start_date = date_ranges[0].year_start_date
							end_date = date_ranges[0].year_end_date
							total_classes_taken = list(frappe.db.sql("""Select count(distinct date) from `tabStudent Attendance` where instructor=%s and  date between %s and %s""",(filters.get("instructor"),start_date,end_date)))
							if len(total_classes_taken)>0:
								total_classes_taken=total_classes_taken[0][0]
								final_data.update({"total_classes_taken":total_classes_taken})
						if count>0:
							workload_percentage = (final_data["total_classes_taken"]/final_data["total_scheduled_classes"])*100
							workload_percentage= str("%.2f" % workload_percentage)+"%"
							final_data.update({"workload_percentage":workload_percentage})
					main_data.append(final_data)
					print("\n\n\n\n\nFinalData")
					print(final_data)



	return main_data,label

def get_columns(label):
	columns=[
		{
			"label": _("Academic Year"),
			"fieldname": "academic_year",
			"fieldtype": "Data",
			"width": 350
		},
		# {
		# 	"label": _("Instructor"),
		# 	"fieldname": "instructor",
		# 	"fieldtype": "Data",
		# 	"width": 350
		# },

		{
			"label": _("Total Scheduled Classes"),
			"fieldname": "total_scheduled_classes",
			"fieldtype": "data",
			"width": 350
		},
		{
			"label": _("Total Classes Taken"),
			"fieldname": "total_classes_taken",
			"fieldtype": "data",
			"width": 300
		},
		
		{			
			"label": _("Workload Percentage"),
			"fieldname": "workload_percentage",
			"fieldtype": "data",
			"width": 400
		},
		
	]

	print("\n\n\n\n\ncolumns")
	print(columns)
	return columns