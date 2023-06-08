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
