import frappe
from frappe.model.document import Document

def validate(self, method):
    if self.party_type=="Student":
        student_info=frappe.db.get_list("Student",filters={"name":self.party},fields=["roll_no"])
        self.roll_no=student_info[0]["roll_no"]
       

    self.letter_head=""

def on_submit(self,method):    
    for d in self.get("references"):
        hostel_fee_info=frappe.get_all("Hostel Fees",filters=[["fees_id","=",d.reference_name]],fields=['name','outstanding_amount'])
        if len(hostel_fee_info)>0:
            hostel_fee_comp=frappe.get_all("Fee Component",{"parent":hostel_fee_info[0]['name'],'fees_category':d.fees_category},
            ["name","outstanding_fees"])
            if len(hostel_fee_comp)>0:
                frappe.db.set_value("Fee Component",hostel_fee_comp[0]['name'], "outstanding_fees",d.outstanding_amount)
                frappe.db.set_value("Hostel Fees",hostel_fee_info[0]['name'], "outstanding_amount",hostel_fee_info[0]['outstanding_amount']-d.allocated_amount)

def on_cancel(self,method):
    for d in self.get("references"):
        hostel_fee_info=frappe.get_all("Hostel Fees",filters=[["fees_id","=",d.reference_name]],fields=['name','outstanding_amount'])
        if len(hostel_fee_info)>0:
            hostel_fee_comp=frappe.get_all("Fee Component",{"parent":hostel_fee_info[0]['name'],'fees_category':d.fees_category},
            ["name","outstanding_fees"])
            if len(hostel_fee_comp)>0:
                frappe.db.set_value("Fee Component",hostel_fee_comp[0]['name'], "outstanding_fees",d.outstanding_amount)
                frappe.db.set_value("Hostel Fees",hostel_fee_info[0]['name'], "outstanding_amount",hostel_fee_info[0]['outstanding_amount']+d.allocated_amount)