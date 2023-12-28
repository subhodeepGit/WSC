import frappe
from datetime import datetime, timedelta
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from wsc.wsc.notification.custom_notification import item_expiry
from frappe.utils import today, getdate
import os
import logging
import json
import requests
from Crypto.Cipher import AES
import hashlib
import json
from frappe import _
import os
from datetime import datetime
from frappe.utils import now_datetime, add_days
from wsc.wsc.notification.custom_notification import email_transaction_status
from wsc.wsc.notification.custom_notification import task_delay_reminder

#Notification for 30 days to Warranty period
def warranty_notification():
    item_list = frappe.get_all("Item", filters={}, fields=["item_code","item_name", "creation", "warranty_period"])
    for items in item_list:
        time_data = items['creation']
        creation_date = time_data.date()                                            
        if items['warranty_period'] != None:                                  
            warranty_period = int(items['warranty_period'])
            warranty_over_date = creation_date + timedelta(days=warranty_period)    
            today = date.today()
            date_diff = warranty_over_date - today
            date_diff_int = date_diff.days                                          
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

def send_mail_cc(recipients=None,cc=None,subject=None,message=None,attachments=None):
    if has_default_email_acc(): 
        frappe.sendmail(recipients=recipients or [], cc=cc, expose_recipients="header",subject=subject,message = message,attachments=attachments,with_container=False)

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


def module_exam_group_data():
    today = date.today()
    exam_dic=[]
    student_data=[]
    ed = frappe.get_all("Exam Declaration",filters={'group_email':1,"docstatus":1,"email_status":"Not Sent","to_date": ["<=", today],"exam_start_date": [">=", today],"disabled":0},fields=["name","to_date"])
    if ed:
        for i in ed:
            exam_dic.append(i)

        module_exam_dic=[]
        for j in exam_dic:
            count_exam_declaration_child_data = frappe.db.sql("""SELECT parent,COUNT(courses) as sum_courses FROM `tabExam Courses` WHERE docstatus=1 and parent = '%s'"""%(j["name"]),as_dict=True)
            
            count_module_exam = frappe.db.count('Module Wise Exam Group', {"docstatus":1,"exam_declaration_id":j["name"],"disabled":0})

            if count_exam_declaration_child_data[0]['sum_courses'] == count_module_exam:
                module_exam = frappe.get_all("Module Wise Exam Group",{'docstatus':1,'exam_declaration_id':j["name"]},
                                            ['name','modules_id','modules_name','module_code','exam_declaration_id','module_exam_start_date','module_exam_end_date','marker_name','checker','course_manager_name','exam_name','academic_term'])
                for t in module_exam:
                    module_exam_dic.append(t)
        module_exam_student_dic=[]
        module_exam_scheduling_dic=[]
        for k in module_exam_dic:
            module_exam_student=frappe.get_all("Module Wise Exam Student",{'parent':k['name'],'elegibility_status':'Qualified'},
                                            ['parent','student_no','student_name','group_name'])
            module_exam_scheduling = frappe.get_all("Student Group Exam Scheduling",{'parent':k['name']},
                                                        ['parent','group_name','examination_date','from_time','to_time','total_duration_in_hours'])
            
            for l in module_exam_student:
                module_exam_student_dic.append(l)
            for t in module_exam_scheduling:
                module_exam_scheduling_dic.append(t)
        
        for module_exam in module_exam_dic:
            for student in module_exam_student_dic:
                for exam_schedule in module_exam_scheduling_dic:
                    if student['parent'] == module_exam['name'] and exam_schedule['parent'] == module_exam['name'] and student['group_name'] == exam_schedule['group_name']:
                        student_data.append({
                            'module_exam_group': student['parent'],
                            'exam_declaration_id': module_exam['exam_declaration_id'],
                            'student_no': student['student_no'],
                            'student_name': student['student_name'],
                            'group_name': student['group_name'],
                            'modules_id': module_exam['modules_id'],
                            'modules_name': module_exam['modules_name'],
                            'module_code': module_exam['module_code'],
                            'academic_term': module_exam['academic_term'],
                            'examination_name': module_exam['exam_name'], 
                            'examination_date': exam_schedule['examination_date'],
                            'from_time': exam_schedule['from_time'],
                            'to_time': exam_schedule['to_time'],
                            'total_duration_in_hours': exam_schedule['total_duration_in_hours']
                        })

        student_schedule = {}

        for exam_schedule in student_data:
            student_no = exam_schedule["student_no"]
            if student_no not in student_schedule:
                student_schedule[student_no] = []
            student_schedule[student_no].append(exam_schedule)

        for student_no, schedules in student_schedule.items():
            student_name = schedules[0]["student_name"]
            # roll_no = student_no
            exam_name = schedules[0]["examination_name"]
            academic_term = schedules[0]["academic_term"]
            sub="Student Exam Schedule"
            html_table = """
            <html>
            <body>
                <p>Dear <b>{name}</b>,</p>
                <p>Please find below the schedule for the <b>{exam_name}</b>, for the Academic Term <b>{academic_term}</b>.</p>
                <table style="line-height: 1em;width: 100%;" border="1">
                <thead>
                    <tr style="text-align:center">
                    <th>Module Code</th>
                    <th>Module Name</th>
                    <th>Group Name</th>
                    <th>Examination Date</th>
                    <th>From Time</th>
                    <th>To Time</th>
                    </tr>
                </thead>
                <tbody>
            """.format(name=student_name or '-', exam_name=exam_name or '-', academic_term=academic_term or '-')

            for exam_schedule in schedules:
                html_table += """
                    <tr>
                    <td>{module_code}</td>
                    <td>{module_name}</td>
                    <td>{group_name}</td>
                    <td>{examination_date}</td>
                    <td>{from_time}</td>
                    <td>{to_time}</td>
                    </tr>
                """.format(
                    module_code=exam_schedule["module_code"] or '-',
                    module_name=exam_schedule["modules_name"] or '-',
                    group_name=exam_schedule["group_name"] or '-',
                    examination_date=exam_schedule["examination_date"].strftime("%d-%m-%Y") or '-',
                    from_time=exam_schedule["from_time"] or '-',
                    to_time=exam_schedule["to_time"] or '-'
                )
            html_table += """
                </tbody>
                </table>
            </body>
            </html>
            """
            stu_email = frappe.db.get_value("Student",{'name':student_no, 'enabled':1},"user")
            send_mail(frappe.db.get_value("User",{'name':stu_email, 'enabled':1},"email"),sub,html_table)
            frappe.db.set_value('Exam Declaration', schedules[0]['exam_declaration_id'], 'email_status', 'Sent')
            # exam_declaration_id=[]
            # for t in schedules:
            #     if t['exam_declaration_id'] not in exam_declaration_id:
            #         exam_declaration_id.append(t['exam_declaration_id'])
            # print(exam_declaration_id)

def student_disable_check():
    today_date=getdate(today())
    student_clearance_list=list(frappe.db.sql("""Select student_id,student_email_address from `tabStudent Clearance Application` where user_disable_date=%s And status= 'Clearance Approved' And docstatus =1""",today_date))
    if len(student_clearance_list)>0:
        for t in student_clearance_list:
            student_id, student_email_address = t[0], t[1]
            frappe.db.sql("""UPDATE `tabStudent` SET `enabled` = 0 WHERE `name` = %s""", student_id)
            frappe.db.sql("""UPDATE `tabUser` SET `enabled` = 0 WHERE `name` = %s""", student_email_address)
            frappe.db.commit()
            delete_user_permission(student_email_address)	
            send_disabled_notification_to_student(student_email_address)

def send_disabled_notification_to_student(student_email_address):
    msg="""<p>Dear Student,Your Student profile and User profile has been disabled successfully.</p><br>"""
    send_mail(student_email_address,'Student Clearance Status',msg)

def delete_user_permission(student_email_address):
    user_permission_list=frappe.db.get_all("User Permission",filters={"user": student_email_address},fields="name")
    if len(user_permission_list)>0:
        for up in user_permission_list:
            
            frappe.db.delete("User Permission",up)
    frappe.db.commit()



def employee_re_engagement_workFlow():
    # bench --site erp.soulunileaders.com execute wsc.task.employee_re_engagement_workFlow
    today_date=getdate(today())
    base_date = str(today_date)
    # months_to_subtract = 9
    # days_to_subtract = 0

    # previous_date = get_previous_date(base_date, months_to_subtract, days_to_subtract)
    # previous_date=previous_date.strftime("%Y-%m-%d")
    # previous_date=datetime.strptime(previous_date, '%Y-%m-%d').date()
    employee_data=frappe.get_all("Employee",['name','present_contract_start_date','present_contract_end_date','date_of_joining','user_id','employee_name'])
    employee_above_ninth_month=[]
    employee_above_six_month=[]
    for t in employee_data:
        if t["present_contract_start_date"] and t["present_contract_end_date"]:
            if  isinstance(t["present_contract_start_date"],str):
                contract_start_date = datetime.strptime(t['present_contract_start_date'], '%Y-%m-%d').date()
            else :
                contract_start_date= t["present_contract_start_date"]
            if isinstance(t["present_contract_end_date"],str):

                contract_end_date = datetime.strptime(t['present_contract_end_date'], '%Y-%m-%d').date()
            else :
                contract_end_date= t["present_contract_end_date"]
            months_difference = frappe.utils.date_diff(contract_end_date,contract_start_date) // 30
            if 6<=months_difference<=9:
                months_to_subtract = 4
                days_to_subtract = 0

                previous_date = get_previous_date(base_date, months_to_subtract, days_to_subtract)
                previous_date=previous_date.strftime("%Y-%m-%d")
                previous_date=datetime.strptime(previous_date, '%Y-%m-%d').date()
                if t['present_contract_start_date'] and t['present_contract_start_date'] == previous_date:
                    employee_above_six_month.append({"name":t['name'],'user_id':t['user_id'],'full_name':['employee_name']})

            if months_difference>9:
                months_to_subtract = 9
                days_to_subtract = 0

                previous_date = get_previous_date(base_date, months_to_subtract, days_to_subtract)
                previous_date=previous_date.strftime("%Y-%m-%d")
                previous_date=datetime.strptime(previous_date, '%Y-%m-%d').date()

                if t['present_contract_start_date'] and t['present_contract_start_date'] == previous_date:
                    employee_above_ninth_month.append({"name":t['name'],'user_id':t['user_id'],'full_name':['employee_name']})

    for t in  employee_above_ninth_month:
        if t['user_id']:
            msg="""<p>Dear %s ,Your Employee Renewal Form is ready. Kindly fill up the form</p><br>"""%(t['full_name'])
            send_mail(t['user_id'],'Employee Renewal Form',msg)

    for t in  employee_above_six_month:
        if t['user_id']:
            msg="""<p>Dear %s ,Your Employee Renewal Form is ready. Kindly fill up the form</p><br>"""%(t['full_name'])
            send_mail(t['user_id'],'Employee Renewal Form',msg)  
  


def appraisal_reminder():
    #notify_employee_after
    today = frappe.utils.today()
    employee_data = frappe.get_all("Employee",['name','date_of_joining','user_id','employee_name'])
    appraisal_cycle_date = frappe.get_all("Employee Appraisal Cycle",{'notify_employee_after': today},["notify_employee_after"])
    if appraisal_cycle_date:
        for t in employee_data:
            if t["user_id"]:
                msg="""<p>Dear %s ,Your Appraisal  form is ready. Kindly fill up the form</p><br>"""%(t['employee_name'])
                send_mail(t['user_id'],'Employee Appraisal',msg)




def get_previous_date(base_date, months_to_subtract, days_to_subtract):
    # Convert the base date to a datetime object
    base_date = datetime.strptime(base_date, "%Y-%m-%d")

    # Calculate the start date by subtracting months and days
    start_date = base_date - relativedelta(months=months_to_subtract) - timedelta(days=days_to_subtract)

    return start_date


def check_and_delete_exit_employee_permissions():
    employee_status = frappe.db.get_all("Employee",{'status':"Left"},['employee','user_id'])
    # if employee_status in ["Left", "Inactive"]:
    if employee_status:
        for employee in employee_status:
            user_email = employee.get('user_id')


            if user_email:
                user_permission_list = frappe.get_all("User Permission", filters={"user": user_email}, fields="name")
                if user_permission_list:
                    for up in user_permission_list:
                        frappe.delete_doc("User Permission", up["name"])
                
        frappe.db.commit() 

###Online payment scheduler start
def find_file_path(filename):
    for dirpath, dirnames, filenames in os.walk('/'):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None
# file_name_transaction_log = 'payment_scheduler.log'
# file_path_transaction_log = find_file_path(file_name_transaction_log)
# logging.basicConfig(filename=file_path_transaction_log, level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_name_transaction_log = 'payment_scheduler.log'
file_path_transaction_log = find_file_path(file_name_transaction_log)
hdfc_file_logger = logging.getLogger('hdfc_file_logger')
file_handler = logging.FileHandler(file_path_transaction_log)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
hdfc_file_logger.addHandler(file_handler)
hdfc_file_logger.setLevel(logging.INFO)

def pad(data):
    length = 16 - (len(data) % 16)
    data += chr(length)*length
    return data
def encrypt(plainText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText)
    encDigest = hashlib.md5()
    encDigest.update(workingKey.encode())
    enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
    encryptedText = enc_cipher.encrypt(plainText.encode()).hex()
    return encryptedText
def decrypt(cipherText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    decDigest = hashlib.md5()
    decDigest.update(workingKey.encode())
    encryptedText = bytes.fromhex(cipherText)
    dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
    decryptedText = dec_cipher.decrypt(encryptedText)
    return str(decryptedText)
def getFinalTransactionStatus(doc):    
    try:                                
        getDoc = frappe.get_doc("HDFCSetting")       
        is_prod = getDoc.get("is_production")     
        hdfc_file_logger.info("Scheduler gt is_prod: %s", is_prod)  

            
        if is_prod is 1:          
            myDoc = frappe.get_doc("HDFCSetting")                    
            access_code = myDoc.get("access_code")
            working_key = myDoc.get("working_key")
            orderNo = doc.name
            hdfc_file_logger.info("Scheduler orderNo: %s", orderNo)    
            # referenceNo = doc.transaction_id
            if doc.transaction_status=="Success" or doc.transaction_status=="Shipped":
                merchant_json_data = {
                    # 'order_no': orderNo,
                    "reference_no" : doc.transaction_id
                }
            else:
                merchant_json_data = {
                    'order_no': orderNo
                }     
            merchant_data = json.dumps(merchant_json_data)
            encrypted_data = encrypt(merchant_data, working_key)

            final_data = 'enc_request='+encrypted_data+'&'+'access_code='+access_code + \
                            '&'+'command=orderStatusTracker&request_type=JSON&response_type=JSON'
            # hdfc_file_logger.info("Scheduler Final API final_data: %s", final_data)
            # r = requests.post('https://apitest.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
            # r = requests.post('https://api.ccavenue.com/apis/servlet/DoWebTran', params=final_data)
            r = requests.post('https://login.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
            t = r.text
            # hdfc_file_logger.info("Scheduler Final API Req: %s", r)
            key_value_pairs = t.split("&")
          

            enc_response_value = None
            for pair in key_value_pairs:
                if pair.startswith("enc_response="):
                    enc_response_value = pair[len("enc_response="):]                   
                    break

            decryptData = decrypt(enc_response_value, working_key)
            # hdfc_file_logger.info("Scheduler final_status_info decryptData: %s",decryptData)
            start_idx = decryptData.find('{')
            end_idx = decryptData.rfind('}}') + 2
            json_string = decryptData[start_idx:end_idx]
            data_dict = json.loads(json_string)
            hdfc_file_logger.info("Scheduler Final Data :%s",data_dict)
            return data_dict
            
        else:
            frappe.throw("Error: is_prod value is None")  

    except Exception as e:	
        return str(e)
    
def await_transaction_update_status():             # bench execute wsc.task.await_transaction_update_status
     
    
    # doc=frappe.get_doc("OnlinePayment","PAYM-2023-0720")        
    # data_dict= getFinalTransactionStatus(doc)
    # print(data_dict)

    current_datetime = now_datetime()
    current_datetime = current_datetime.replace(microsecond=0)  
    five_days_ago = add_days(current_datetime, -5)
           

    awaited_status_transactions_1=frappe.get_all("OnlinePayment",filters=[["date_time_of_transaction", ">=", five_days_ago],["date_time_of_transaction", "<=", current_datetime],["transaction_status" ,"IN",["Awaited","Failure","Initiated","Rejected","Aborted","Unsuccessful"]],['gateway_name','=','HDFC']],fields=['name'])  
    hdfc_file_logger.info("awaited_status_transactions_1:%s",awaited_status_transactions_1)

    awaited_status_transactions_2=frappe.get_all("OnlinePayment",filters=[["date_time_of_transaction", ">=", five_days_ago],["date_time_of_transaction", "<=", current_datetime],["transaction_status" ,"IN",["Success","Shipped"]],['gateway_name','=','HDFC']],fields=['name',"transaction_id"])  
    hdfc_file_logger.info("awaited_status_transactions_2:%s",awaited_status_transactions_2)

    awaited_status_transactions_0=frappe.get_all("OnlinePayment",filters=[["docstatus" ,"=",0],["posting_date", ">=", five_days_ago],["posting_date", "<=", current_datetime],['gateway_name','=','HDFC']])
    hdfc_file_logger.info("awaited_status_transactions_0 in draft:%s",awaited_status_transactions_0)


    # awaited_status_transactions_3=frappe.get_all("OnlinePayment",filters=[["posting_date", ">=", five_days_ago],["posting_date", "<=", current_datetime],['gateway_name','=','HDFC']])
    # hdfc_file_logger.info("awaited_status_transactions_0 in draft:%s",awaited_status_transactions_3)
    # print("awaited_status_transactions_3----->",awaited_status_transactions_3)       #To update submitted transaction status

           
    for t0 in awaited_status_transactions_0:
        try:
            doc=frappe.get_doc("OnlinePayment",t0["name"])  
            hdfc_file_logger.info("t0 doc: %s", doc)      
            data_dict= getFinalTransactionStatus(doc)
            # print("t0",data_dict)

            if doc.docstatus==0:
                print(data_dict["Order_Status_Result"])
                if "order_no" in data_dict["Order_Status_Result"].keys():
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    hdfc_file_logger.info("t0 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status"]!='Initiated':
                        if data_dict["Order_Status_Result"]["order_bank_response"]:
                            doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"]
                   
                    paying_amount=str(data_dict['Order_Status_Result']['order_amt'])
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        # hdfc_file_logger.info("t0 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                hdfc_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            # hdfc_file_logger.info("t0 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            # hdfc_file_logger.info("t0 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        hdfc_file_logger.info("Missing order_status_date_time in data_dict")     
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper() 
                    order_no=data_dict['Order_Status_Result']['order_no'] 
                    order_status=data_dict['Order_Status_Result']['order_status'] 
                    payer_name=data_dict['Order_Status_Result']['order_bill_name'] 
                                 
                    # transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nPaying Amount: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    transaction_info = f"Order ID: {order_no}\nStatus Message: {order_status}\nPaying Amount: {paying_amount}\nBilling Name: {payer_name}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    
                    try:
                        hdfc_file_logger.info("t0 scheduler inside try.....................")
                        doc.save(ignore_permissions=True)                        
                        doc.submit()
                        hdfc_file_logger.info("t0 scheduler inside submit.....................")
                        # doc.submit()
                        hdfc_file_logger.info("t0 Scheduler SUCESSFULLY COMPLETED")    
                    except Exception as save_exception:                        
                        hdfc_file_logger.info(f"Error saving document: {repr(save_exception)}")
        except Exception as e:
           hdfc_file_logger.info(f"Error in awaited_status_transactions_0: {repr(e)}")

    for t1 in awaited_status_transactions_1:
        try:
            doc=frappe.get_doc("OnlinePayment",t1["name"])  
            data_dict= getFinalTransactionStatus(doc)

            # print("t1",data_dict)
            if doc.docstatus==1:  
                if data_dict["Order_Status_Result"]["order_status"]!=doc.transaction_status:
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    hdfc_file_logger.info("t1 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    hdfc_file_logger.info("t1 order_status: %s", order_status)
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        hdfc_file_logger.info("t0 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                hdfc_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            hdfc_file_logger.info("t0 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            hdfc_file_logger.info("t0 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        hdfc_file_logger.info("Missing order_status_date_time in data_dict")                     
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper() 
                    hdfc_file_logger.info("t1 gateway_name: %s", data_dict["Order_Status_Result"]["order_ship_name"].upper() )
                    paying_amount=str(data_dict['Order_Status_Result']['order_amt'])
                    hdfc_file_logger.info("t1 paying_amount: %s", paying_amount)
                    if "order_bank_response" in data_dict["Order_Status_Result"].keys(): 
                        doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"]                    
                                      
                    transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nAmount Paid: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    doc.save(ignore_permissions=True)  
                    doc.submit()
                    hdfc_file_logger.info("t1 Scheduler SUCESSFULLY COMPLETED")     
                if data_dict["Order_Status_Result"]["order_status"]=="Shipped" and doc.transaction_status!="Success":
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    hdfc_file_logger.info("t1 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        hdfc_file_logger.info("t0 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                hdfc_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            hdfc_file_logger.info("t0 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            hdfc_file_logger.info("t0 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        hdfc_file_logger.info("Missing order_status_date_time in data_dict")   
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper()   
                    if "order_bank_response" in data_dict["Order_Status_Result"].keys():
                       doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"] 
                                   
                    transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nAmount Paid: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    if doc.transaction_status=="Success":
                        doc.email_status=1
                        email_transaction_status(doc)
                    doc.save(ignore_permissions=True)  
                    # doc.submit()

                    hdfc_file_logger.info("t1 Scheduler SUCESSFULLY COMPLETED")  
                # if data_dict["Order_Status_Result"]["order_status"]=="Shipped" and doc.transaction_status=="Shipped":
                #     doc.transaction_status = "Success"
                #     doc.save()
                #     doc.submit()
                #     hdfc_file_logger.info("t1 Successfully submitted") 
        except Exception as e:	
            hdfc_file_logger.info(f"Error in awaited_status_transactions_1: {repr(e)}")

    for t2 in awaited_status_transactions_2:
        try:
            doc=frappe.get_doc("OnlinePayment",t2["name"])  
            data_dict= getFinalTransactionStatus(doc)

            # print("t1",data_dict)
            if doc.docstatus==1:  
                if data_dict["Order_Status_Result"]["order_status"]!=doc.transaction_status:
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    hdfc_file_logger.info("t2 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    hdfc_file_logger.info("t2 order_status: %s", order_status)
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        hdfc_file_logger.info("t2 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                hdfc_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            hdfc_file_logger.info("t0 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            hdfc_file_logger.info("t0 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        hdfc_file_logger.info("Missing order_status_date_time in data_dict")                     
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper() 
                    hdfc_file_logger.info("t2 gateway_name: %s", data_dict["Order_Status_Result"]["order_ship_name"].upper() )
                    paying_amount=str(data_dict['Order_Status_Result']['order_amt'])
                    hdfc_file_logger.info("t2 paying_amount: %s", paying_amount)
                    if "order_bank_response" in data_dict["Order_Status_Result"].keys(): 
                        doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"]                    
                                      
                    transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nAmount Paid: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    doc.save(ignore_permissions=True)  
                    doc.submit()
                    hdfc_file_logger.info("t1 Scheduler SUCESSFULLY COMPLETED")     
                if data_dict["Order_Status_Result"]["order_status"]=="Shipped" and doc.transaction_status!="Success":
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    hdfc_file_logger.info("t2 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        hdfc_file_logger.info("t2 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                hdfc_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            hdfc_file_logger.info("t1 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            hdfc_file_logger.info("t1 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        hdfc_file_logger.info("Missing order_status_date_time in data_dict")   
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper()   
                    if "order_bank_response" in data_dict["Order_Status_Result"].keys():
                       doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"] 
                                   
                    transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nAmount Paid: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    doc.save(ignore_permissions=True)  
                    # doc.submit()
                    hdfc_file_logger.info("t2 Scheduler SUCESSFULLY COMPLETED")  
                # if data_dict["Order_Status_Result"]["order_status"]=="Shipped" and doc.transaction_status=="Shipped":
                #     doc.transaction_status = "Success"
                #     doc.save()
                #     doc.submit()
                #     hdfc_file_logger.info("t1 Successfully submitted") 
        except Exception as e:	
            hdfc_file_logger.info(f"Error in awaited_status_transactions_2: {repr(e)}")


##Online payment scheduler end
##########################################################################Online Payment AXIS Scheduler Start###############################################################################

axis_file_name_transaction_log = 'axis_payment_scheduler.log'
axis_file_path_transaction_log = find_file_path(axis_file_name_transaction_log)
axis_file_logger = logging.getLogger('axis_file_logger')
axis_file_handler = logging.FileHandler(axis_file_path_transaction_log)
axis_file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
axis_file_handler.setFormatter(axis_file_formatter)
axis_file_logger.addHandler(axis_file_handler)
axis_file_logger.setLevel(logging.INFO)


def axis_getFinalTransactionStatus(doc):   
    try:                                
        getDoc = frappe.get_doc("AXIS Settings")       
        is_prod = getDoc.get("is_production")     
        axis_file_logger.info("Scheduler gt is_prod: %s", is_prod)  

            
        if is_prod is 1:          
            myDoc = frappe.get_doc("AXIS Settings")                    
            access_code = myDoc.get("access_code")
            working_key = myDoc.get("working_key")
            orderNo = doc.name
            axis_file_logger.info("Scheduler orderNo: %s", orderNo)    
            # referenceNo = doc.transaction_id
            if doc.transaction_status=="Success" or doc.transaction_status=="Shipped":
                merchant_json_data = {
                    # 'order_no': orderNo,
                    "reference_no" : doc.transaction_id
                }
            else:
                merchant_json_data = {
                    'order_no': orderNo
                }     
            merchant_data = json.dumps(merchant_json_data)
            encrypted_data = encrypt(merchant_data, working_key)

            final_data = 'enc_request='+encrypted_data+'&'+'access_code='+access_code + \
                            '&'+'command=orderStatusTracker&request_type=JSON&response_type=JSON'
            
            r = requests.post('https://apitest.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)        #Staging
            # r = requests.post('https://api.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)              #Production
            # r = requests.post('https://login.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
            t = r.text

            # axis_file_logger.info("Scheduler Final API Req: %s", r)
            key_value_pairs = t.split("&")
          

            enc_response_value = None
            for pair in key_value_pairs:
                if pair.startswith("enc_response="):
                    enc_response_value = pair[len("enc_response="):]                   
                    break

            decryptData = decrypt(enc_response_value, working_key)
            axis_file_logger.info("Scheduler final_status_info decryptData: %s",decryptData)
            start_idx = decryptData.find('{')
            end_idx = decryptData.rfind('}}') + 2
            json_string = decryptData[start_idx:end_idx]
            data_dict = json.loads(json_string)
            axis_file_logger.info("Scheduler Final Data :%s",data_dict)
            return data_dict
            
        else:
            frappe.throw("Error: is_prod value is None")  

    except Exception as e:	
        return str(e)


def axis_transaction_update_status():             # bench execute wsc.task.axis_transaction_update_status

    # doc=frappe.get_doc("OnlinePayment","PAYM-2023-0736")        
    # data_dict= axis_getFinalTransactionStatus(doc)
    # print(data_dict) 
    current_datetime = now_datetime()
    current_datetime = current_datetime.replace(microsecond=0)  
    five_days_ago = add_days(current_datetime, -5)
           

    awaited_status_transactions_1=frappe.get_all("OnlinePayment",filters=[["date_time_of_transaction", ">=", five_days_ago],["date_time_of_transaction", "<=", current_datetime],["transaction_status" ,"IN",["Awaited","Failure","Initiated","Rejected","Aborted","Unsuccessful"]],['gateway_name','=','AXIS']],fields=['name'])  
    axis_file_logger.info("awaited_status_transactions_1:%s",awaited_status_transactions_1)

    awaited_status_transactions_2=frappe.get_all("OnlinePayment",filters=[["date_time_of_transaction", ">=", five_days_ago],["date_time_of_transaction", "<=", current_datetime],["transaction_status" ,"IN",["Success","Shipped","Successful"]],['gateway_name','=','AXIS']],fields=['name',"transaction_id"])  
    axis_file_logger.info("awaited_status_transactions_2:%s",awaited_status_transactions_2)

    awaited_status_transactions_0=frappe.get_all("OnlinePayment",filters=[["docstatus" ,"=",0],["posting_date", ">=", five_days_ago],["posting_date", "<=", current_datetime],['gateway_name','=','AXIS']],fields=['name'])
    axis_file_logger.info("awaited_status_transactions_0 in draft:%s",awaited_status_transactions_0)

    for t0 in awaited_status_transactions_0:
        try:
            doc=frappe.get_doc("OnlinePayment",t0["name"])  
            axis_file_logger.info("t0 doc: %s", doc)      
            data_dict= axis_getFinalTransactionStatus(doc)

            if doc.docstatus==0:
                # print(data_dict["Order_Status_Result"])
                if "order_no" in data_dict["Order_Status_Result"].keys():
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    axis_file_logger.info("t0 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status"]!='Initiated':
                        if data_dict["Order_Status_Result"]["order_bank_response"]:
                            doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"]
                   
                    paying_amount=str(data_dict['Order_Status_Result']['order_amt'])
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        # axis_file_logger.info("t0 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                axis_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            # axis_file_logger.info("t0 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            # axis_file_logger.info("t0 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        axis_file_logger.info("Missing order_status_date_time in data_dict")     
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper() 
                    order_no=data_dict['Order_Status_Result']['order_no'] 
                    order_status=data_dict['Order_Status_Result']['order_status'] 
                    payer_name=data_dict['Order_Status_Result']['order_bill_name'] 
                                 
                    # transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nPaying Amount: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    transaction_info = f"Order ID: {order_no}\nStatus Message: {order_status}\nPaying Amount: {paying_amount}\nBilling Name: {payer_name}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    
                    try:
                        axis_file_logger.info("t0 scheduler inside try.....................")
                        doc.save(ignore_permissions=True)                        
                        doc.submit()
                        axis_file_logger.info("t0 scheduler inside submit.....................")
                        # doc.submit()
                        axis_file_logger.info("t0 Scheduler SUCESSFULLY COMPLETED")    
                    except Exception as save_exception:                        
                        axis_file_logger.info(f"Error saving document: {repr(save_exception)}")
        except Exception as e:
           axis_file_logger.info(f"Error in awaited_status_transactions_0: {repr(e)}")

    for t1 in awaited_status_transactions_1:
        try:
            doc=frappe.get_doc("OnlinePayment",t1["name"])  
            data_dict= axis_getFinalTransactionStatus(doc)

            # print("t1",data_dict)
            if doc.docstatus==1:  
                if data_dict["Order_Status_Result"]["order_status"]!=doc.transaction_status:
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    axis_file_logger.info("t1 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    axis_file_logger.info("t1 order_status: %s", order_status)
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        axis_file_logger.info("t0 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                axis_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            axis_file_logger.info("t0 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            axis_file_logger.info("t0 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        axis_file_logger.info("Missing order_status_date_time in data_dict")                     
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper() 
                    axis_file_logger.info("t1 gateway_name: %s", data_dict["Order_Status_Result"]["order_ship_name"].upper() )
                    paying_amount=str(data_dict['Order_Status_Result']['order_amt'])
                    axis_file_logger.info("t1 paying_amount: %s", paying_amount)
                    if "order_bank_response" in data_dict["Order_Status_Result"].keys(): 
                        doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"]                    
                                      
                    transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nAmount Paid: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    doc.save(ignore_permissions=True)  
                    doc.submit()
                    axis_file_logger.info("t1 Scheduler SUCESSFULLY COMPLETED")     
                if data_dict["Order_Status_Result"]["order_status"]=="Shipped" and doc.transaction_status!="Success":
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    axis_file_logger.info("t1 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        axis_file_logger.info("t0 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                axis_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            axis_file_logger.info("t0 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            axis_file_logger.info("t0 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        axis_file_logger.info("Missing order_status_date_time in data_dict")   
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper()   
                    if "order_bank_response" in data_dict["Order_Status_Result"].keys():
                       doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"] 
                                   
                    transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nAmount Paid: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    if doc.transaction_status=="Success":
                        doc.email_status=1
                        email_transaction_status(doc)
                    doc.save(ignore_permissions=True) 

                    # doc.submit()
                    axis_file_logger.info("t1 Scheduler SUCESSFULLY COMPLETED")  
                # if data_dict["Order_Status_Result"]["order_status"]=="Shipped" and doc.transaction_status=="Shipped":
                #     doc.transaction_status = "Success"
                #     doc.save()
                #     doc.submit()
                #     axis_file_logger.info("t1 Successfully submitted") 
        except Exception as e:	
            axis_file_logger.info(f"Error in awaited_status_transactions_1: {repr(e)}")

    for t2 in awaited_status_transactions_2:
        try:
            doc=frappe.get_doc("OnlinePayment",t2["name"])  
            data_dict= axis_getFinalTransactionStatus(doc)

            # print("t1",data_dict)
            if doc.docstatus==1:  
                if data_dict["Order_Status_Result"]["order_status"]!=doc.transaction_status:
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    axis_file_logger.info("t2 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    axis_file_logger.info("t2 order_status: %s", order_status)
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        axis_file_logger.info("t2 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                axis_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            axis_file_logger.info("t0 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            axis_file_logger.info("t0 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        axis_file_logger.info("Missing order_status_date_time in data_dict")                     
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper() 
                    axis_file_logger.info("t2 gateway_name: %s", data_dict["Order_Status_Result"]["order_ship_name"].upper() )
                    paying_amount=str(data_dict['Order_Status_Result']['order_amt'])
                    axis_file_logger.info("t2 paying_amount: %s", paying_amount)
                    if "order_bank_response" in data_dict["Order_Status_Result"].keys(): 
                        doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"]                    
                                      
                    transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nAmount Paid: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    doc.save(ignore_permissions=True)  
                    doc.submit()
                    axis_file_logger.info("t1 Scheduler SUCESSFULLY COMPLETED")     
                if data_dict["Order_Status_Result"]["order_status"]=="Shipped" and doc.transaction_status!="Success":
                    doc.transaction_id = data_dict["Order_Status_Result"]["reference_no"]
                    axis_file_logger.info("t2 Final API transaction_id: %s", data_dict["Order_Status_Result"]["reference_no"])
                    order_status= data_dict["Order_Status_Result"]["order_status"]
                    if order_status=="Shipped":
                        doc.transaction_status = "Success"
                    else:
                        doc.transaction_status = order_status
                    if data_dict["Order_Status_Result"]["order_status_date_time"]:
                        transaction_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                        axis_file_logger.info("t2 scheduler server transaction_time %s", transaction_time)

                        try:                          
                            date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
                        except ValueError:
                            try:                                
                                date_obj = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                axis_file_logger.info("Invalid date format: %s", transaction_time)
                                date_obj = None

                        if date_obj:
                            axis_file_logger.info("t1 date_obj: %s", date_obj)
                            doc.date_time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                            axis_file_logger.info("t1 updated date_obj: %s", date_obj.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                       
                        axis_file_logger.info("Missing order_status_date_time in data_dict")   
                    doc.gateway_name=data_dict["Order_Status_Result"]["order_ship_name"].upper()   
                    if "order_bank_response" in data_dict["Order_Status_Result"].keys():
                       doc.transaction_status_description = data_dict["Order_Status_Result"]["order_bank_response"] 
                                   
                    transaction_info = f"Order ID: {data_dict['Order_Status_Result']['order_no']}\nStatus Message: {data_dict['Order_Status_Result']['order_status']}\nAmount Paid: {paying_amount}\nBilling Name: {data_dict['Order_Status_Result']['order_bill_name']}"
                    doc.transaction_status_description=transaction_info
                    doc.transaction_progress="Completed"
                    doc.save(ignore_permissions=True)  
                    # doc.submit()
                    axis_file_logger.info("t2 Scheduler SUCESSFULLY COMPLETED")  
                # if data_dict["Order_Status_Result"]["order_status"]=="Shipped" and doc.transaction_status=="Shipped":
                #     doc.transaction_status = "Success"
                #     doc.save()
                #     doc.submit()
                #     axis_file_logger.info("t1 Successfully submitted") 
        except Exception as e:	
            axis_file_logger.info(f"Error in awaited_status_transactions_2: {repr(e)}")

#################################################### Project Management Scheduler Start #####################################################################

##########  Email for Task Overdue  ##########
def overdue_task():
    today_date = datetime.today().date()
    task_data = frappe.get_all("Task",['name','exp_end_date','project_manager'])
    for t in task_data:
        if t["exp_end_date"]:
            end_date = datetime.strptime(t['exp_end_date'], "%Y-%m-%d").date()
            if today_date > end_date:
                sub = "Reg:Task Delay"
                msg="""<b>Task {0} with Subject {1} has exceeded its expected end date</b><br>"""%(t['name'],['subject'])
                msg += """Thank You<br>"""
                recipients_list = frappe.get_all("Task Assign", {'parent':t['name']},['assign_to'])
                recipient_emails = [recipient['assign_to'] for recipient in recipients_list]
                cc_emails = t['project_manager']
                send_mail_cc(recipient_emails,cc_emails,sub,msg)

##########  Status Update for Task Overdue  ##########
def status_update():
    today_date = datetime.today().date()
    task_data = frappe.get_all("Task",['name','exp_end_date','project_manager'])
    for t in task_data:
        if t['exp_end_date']:
            exp_date = datetime.strptime(t['exp_end_date'], "%Y-%m-%d").date()
            if today_date > exp_date:
                frappe.db.set_value('Task', t['name'], t['status'], 'Overdue')
            else:
                pass
#################################################### Project Management Scheduler Ends #####################################################################