import frappe
import datetime
from datetime import datetime
from datetime import date, timedelta
from wsc.wsc.notification.custom_notification import item_expiry


#Notification for 30 days to Warranty period
def warranty_notification():
    item_list = frappe.get_all("Item", filters={}, fields=["item_code","item_name", "creation", "warranty_period"])
    for items in item_list:
        time_data = items['creation']
        creation_date = time_data.date()                                            #converting date_time to date()
        if items['warranty_period'] != None:                                  
            warranty_period = int(items['warranty_period'])
            warranty_over_date = creation_date + timedelta(days=warranty_period)    #adding date of creation with number of days to get warranty_end_date
            today = date.today()
            date_diff = warranty_over_date - today
            date_diff_int = date_diff.days                                          #difference between warranty expires and creation in days
            if date_diff_int == 30 or (date_diff_int <= 30 and date_diff_int > 0):
                item_expiry(items)
        
# Notification for Safety stock reach
def safety_stock_reach():
    item_list = frappe.get_all("Item", filters={}, fields=["item_code","safety_stock"])
    for items in item_list:
        item_code = items['item_code']
        remaining_stock_list = frappe.get_all("Stock Ledger Entry", filters={"item_code": item_code}, fields=["sum(actual_qty) as remaining_stock"])
        remaining_stock_dict = remaining_stock_list[0]
        remaining_stock_value = remaining_stock_dict['remaining_stock']
        if remaining_stock_value != None:
            remaining_stock = remaining_stock_value
            # print(items)
            # print(remaining_stock)
            if remaining_stock <= items['safety_stock']:
            #     print(items)
                safety_stock_reach_notification(items)

def safety_stock_reach_notification(doc):
    msg="""<b>---------------------Safety Stock for Item {0} reached---------------------</b><br>""".format(doc.get('item_name'))
    recipients_list = list(frappe.db.sql("select department_email_id from `tabDepartment Email ID`"))
    recipients = recipients_list[0]
    attachments = None
    send_mail(recipients,'Payment Details',msg,attachments)


def has_default_email_acc():
    for d in frappe.get_all("Email Account", {"default_outgoing":1}):
       return "true"
    return ""

def send_mail(recipients=None,subject=None,message=None,attachments=None):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients or [],expose_recipients="header",subject=subject,message = message,attachments=attachments,with_container=True)        


# Notification to students and invigilators 7 days prior exam date
# bench --site erp.soulunileaders.com execute wsc.task.exam_reminder_notification
def exam_reminder_notification():
    get_students = frappe.get_all("Module Wise Exam Student", fields=["parent","student_no","student_name","group_name"])
    get_exam_date_based_group = frappe.get_all("Student Group Exam Scheduling", fields=["parent", "group_name", "examination_date", "from_time", "to_time"])
    get_invigilators = frappe.get_all("Invigilator Details", fields=["parent","trainer","trainer_name"])
    for t in get_students:
        for d in get_exam_date_based_group:
            if t["parent"] == d["parent"] and t["group_name"] == d["group_name"]:
                exam_detail = frappe.get_all("Module Wise Exam Group",filters={"name":t["parent"], "disabled": 0, "docstatus":1}, fields=["name","exam_name","modules_name","module_code"])
                email=frappe.get_all("Student", filters={"name":t["student_no"]}, fields=["student_email_id"])[0]["student_email_id"]
                msg="""Dear {0},<br>""".format(t["student_name"])
                msg+="""This is a reminder that your {0} for {1}({2}) will be held on <b>{3}</b> from <b>{4}</b> to <b>{5}</b>.""".format(exam_detail[0]["exam_name"],exam_detail[0]["modules_name"],exam_detail[0]["module_code"],d["examination_date"].strftime("%d-%m-%Y"),d["from_time"],d["to_time"])
                if date.today() == d["examination_date"] - timedelta(days=7):
                    send_mail_without_container(email,'Examination Reminder Notification',msg)
    for j in get_invigilators:
        for k in get_exam_date_based_group:
            if j["parent"] == k["parent"]:
                exam_detail = frappe.get_all("Module Wise Exam Group",filters={"name":j["parent"], "disabled": 0, "docstatus":1}, fields=["name","exam_name","modules_name","module_code"])
                email = frappe.get_all("Employee",filters={"name":j["trainer_name"]}, fields=["user_id"])[0]["user_id"]
                msg="""Dear {0},<br>""".format(j["trainer"])
                msg+="""This is a reminder that <b>{0}</b> for <b>{1}</b>({2}) will be held on the following date(s):""".format(exam_detail[0]["exam_name"],exam_detail[0]["modules_name"],exam_detail[0]["module_code"])
                msg_table=frappe.get_all("Student Group Exam Scheduling", filters={"parent":j["parent"]}, fields=["parent", "group_name", "examination_date", "from_time", "to_time","total_duration_in_hours"])
                msg+="""
                <table style="line-height: 1em;width: 100%;" border="1" cellpadding="2" cellspacing="2">
                <thead>
                    <tr><th colspan="5"><b>Examination Details</b></th></tr>
                    <tr>
                        <th class="text-center" style="width:20%; font-size:14px;">Group Name</th>
                        <th class="text-center" style="width:20%; font-size:14px;">Examination Date</th>
                        <th class="text-center" style="width:20%; font-size:14px;">From Time</th>
                        <th class="text-center" style="width:20%; font-size:14px;">To Time</th>
                        <th class="text-center" style="width:20%; font-size:14px;">Total Duration (in Hours)</th>
                    </tr>
                </thead>
                <tbody>"""
                for i in msg_table:
                    msg+="""<tr><td class="text-center">{0}</td>""".format(i["group_name"])
                    msg+="""<td class="text-center">{0}</td>""".format(i["examination_date"].strftime("%d-%m-%Y"))
                    msg+="""<td class="text-center">{0}</td>""".format(i["from_time"])
                    msg+="""<td class="text-center">{0}</td>""".format(i["to_time"])
                    msg+="""<td class="text-center">{0}</td>""".format(i["total_duration_in_hours"])
                    msg+="""</tr>"""
                msg+="""
                </tbody>
                </table>"""
                if date.today() == k["examination_date"] - timedelta(days=7):
                    send_mail_without_container(email,'Examination Reminder Notification',msg)


def send_mail_without_container(recipients=None,subject=None,message=None,attachments=None):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients or [],expose_recipients="header",subject=subject,message = message,attachments=attachments,with_container=False)    