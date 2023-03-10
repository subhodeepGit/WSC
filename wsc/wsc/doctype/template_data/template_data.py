# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd
from pandas import DataFrame
import json
import os
from glob import glob

class TemplateData(Document):
	def on_submit(self):
		# print("\n\n\n\n")
		# for t in self.get("data_import_child"):
		# 	print(t.table)
		get_data(self)

def get_data(self):
	# rawData=[]
	# rawData=frappe.get_all("DocField",['parent','label','reqd','unique'])
	# allData=json.loads(rawData)
	data=[]
	for t in self.get("data_import_child"):
		data_out =frappe.get_all("DocField",{"parent":t.table},['parent','label','reqd','unique'])
		for j in data_out:
			if j['label']:
				data.append(j)
	
	df = pd.DataFrame.from_records(data)
	# print (df)
	# print (data)
	df.to_excel("/home/erpnext/Downloads/data.xlsx", index=False)


	List_trans=["/home/erpnext/frappe-bench/apps/wsc/wsc/fixtures/translation.json"]
	cus_json=['/home/erpnext/frappe-bench/apps/wsc/wsc/wsc/custom/']
	Trans_df=trans_of_doc(List_trans)
	data_custom_json=custom_json(Trans_df,cus_json)
	print("\n\n\n\n")
	print(data_custom_json)    

def trans_of_doc(path_of_translation):
    # /opt/bench/frappe-bench/apps/ed_tec/ed_tec/fixtures/translation.json
    # This is for Translation of Doc type
    Trans_list=[]
    for t in range(len(path_of_translation)):
        with open(path_of_translation[t]) as json_file:
            data = json.load(json_file)
        for t in range(len(data)):
            Trans_list.append(["source_text",data[t]["source_text"],"translated_text",data[t]["translated_text"]])
    Trans_df = pd.DataFrame(Trans_list, columns = ["source_text","source_text_info","translated_text","translated_text_info"])
    return Trans_df

def custom_json(Trans_df,cus_json):
    # for custom doc type of ed_tec
    data_return=[]
    for i in range(len(cus_json)):
        path=cus_json[i]
        dir_list = os.listdir(path)
        for t in range(len(dir_list)):
            split_tup = os.path.splitext(dir_list[t])
            file_extension = split_tup[1]
            file_name=str(split_tup[0])
            if file_extension==".json":
                file_name=path+dir_list[t]
                with open(file_name) as json_file:
                    data = json.load(json_file)
                if len(data["custom_fields"])!=0:
                    df = pd.DataFrame(data["custom_fields"])
                    df['Doctype_name']=data["doctype"]
                    # df=df[(df.fieldtype=='Link') | (df.fieldtype=='Table')]

                    # df.reset_index(inplace = True)
                    for r in range(len(Trans_df)):
                        df=df.replace(to_replace =Trans_df["source_text_info"][r],value =Trans_df["translated_text_info"][r])
                    # print(df)    
                    for z in range(len(df)):
                        # a='''{"source": "%s", "target_type": null, "target": "%s", "source_type": null},'''%(df["Doctype_name"][z],df["options"][z])
                        a={"parent": df["Doctype_name"][z], "label": df["label"][z], "reqd": df["reqd"][z], "unique": df["unique"][z]}
                        data_return.append(a)
    df = pd.DataFrame.from_records(data_return)
    print(df)
    return  data_return
	