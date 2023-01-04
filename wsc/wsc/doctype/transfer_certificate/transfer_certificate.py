# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TransferCertificate(Document):
    @frappe.whitelist()
    def get_missing_fields(self):
        data={}
        data["enrollment_dte"]=frappe.db.get_value("Program Enrollment",{"student":self.student,"docstatus":1},"enrollment_date")
        data["prn"]=frappe.db.get_value("Program Enrollment",{"student":self.student,"docstatus":1},"permanant_registration_number","enrollment_date")
        data["class"]=frappe.db.get_value("Current Educational Details",{"parent":self.student},"programs")
        return data

    def validate(doc):
        sten=frappe.db.get_all("Student", {'name':doc.student},['name','enabled'])
        status=sten[0]['enabled']
        stu_name = sten[0]['name']
        if(status == 1):
            update_doc = frappe.get_doc("Student",stu_name)
            update_doc.enabled=0
            update_doc.save()