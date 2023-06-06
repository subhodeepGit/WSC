# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe


# def execute(filters=None):
#      data = get_data(filters)
#      columns = get_columns(filters)
#      return columns, data

# def get_columns(filters=None):
#     return [
#     {
#         "label": "Subject",
#         "fieldtype": "Data",
#         "fieldname": "subject",
#         'width':180
#     },
# ]
    
# def get_data(filters):
#     filter=[]
    
#     # if filters.get("name_of_school"):
#     #     filter.append(['site',"=",filters.get("name_of_school")])
#     if filters.get("item"):
#         filter.append(['item',"=",filters.get("item")])

#     data=frappe.get_all("Item Price",filters=filter,
#                             fields=['name','site','school_name','udise_code','block','district'])

#     final_data=[]
#     for t in data:
#         child = frappe.get_all("Schoolwise Equipment List childtable",{"parent":t["name"]},['lab','item_name','vendor','serial_number','mac_id'])
#         for i in child:
#             i['name']=t['name']
#             i['site']=t['site']
#             i['school_name']=t['school_name']
#             i['udise_code']=t['udise_code']
#             i['block']=t['block']
#             i['district']=t['district']
#             final_data.append(i)    
#     return final_data