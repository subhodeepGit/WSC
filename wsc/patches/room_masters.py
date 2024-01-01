import frappe
# bench execute wsc.patches.room_masters.execute
def execute():
    set_status()

def set_status():
    for sg in frappe.get_all("Room Masters",{'status':"Allotted"}):
        print(sg.name)
        doc=frappe.get_doc("Room Masters",sg.name)
        frappe.db.set_value("Room Masters",sg.name,'status','Functional')