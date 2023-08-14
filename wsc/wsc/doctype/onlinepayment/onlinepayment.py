# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
from Crypto.Cipher import AES
import hashlib
import json
from frappe import _
import secrets
import pymysql
from urllib.parse import urlparse
import os
import sys
import logging
from .database_operations import fetch_and_process_data



# username = os.getenv('USER')
username ='wsc'

module_path = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "onlinepayment")
sys.path.append(module_path)


# Configure logging for getTransactionDetails()
logfile_transaction_name = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "onlinepayment", "transaction_log.log")
logging.basicConfig(filename=logfile_transaction_name, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger_transaction = logging.getLogger(__name__)

# Configure logging for login()
logfile_login_name = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "onlinepayment", "login_log.log")
logging.basicConfig(filename=logfile_login_name, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger_login = logging.getLogger(__name__)


class OnlinePayment(Document):
    def validate(self):
        if self.paying_amount>self.total_outstanding_amout:
            frappe.throw("Paying Amount can't be more then Total Outstanding Amount")

    def on_cancel(doc):
        frappe.throw("Once form is submitted it can't be cancelled")

    def on_submit(doc):
        get_url= frappe.utils.get_url()       
        # getTransactionDetails(doc, 'http://erp.soulunileaders.com:8000/app/onlinepayment')
        getTransactionDetails(doc, get_url)
        frappe.msgprint("Your Transaction is completed. Your Transaction Id is " +
                doc.transaction_id + "."  " Status is " + frappe.bold(doc.transaction_status))



currency = 'INR'
language = 'EN'

def check_url(p_url):
    parsed_url = urlparse(p_url)
    
    if parsed_url.scheme == "http":
        return "test"
    else:
        return "production"
    

@frappe.whitelist()
def get_outstanding_amount(student):
	fee_voucher_list=frappe.get_all("Fees",filters=[["student","=",student],["outstanding_amount","!=",0],["docstatus","=",1]],
															fields=['outstanding_amount'],
															order_by="due_date asc")
	outstanding_amount=0
	for t in fee_voucher_list:
		outstanding_amount=t['outstanding_amount']+outstanding_amount
		# print("outstanding_amount",outstanding_amount)
	return outstanding_amount

@frappe.whitelist()
def login(party_name, roll_no, amount, order_id, url): 
    print("\n\n\n\n url",url)
    processed_url = check_url(url)
    logger_login.info("Login request received with party_name: %s, roll_no: %s, amount: %s, order_id: %s, url: %s", party_name, roll_no, amount, order_id, url)
  
    
    try:
        site_name = frappe.local.site 
        try:
            c = fetch_and_process_data(site_name)

            # integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name,redirect_url, cancel_url FROM `payment_integration`"
            if processed_url == "test":
                integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name,redirect_url, cancel_url FROM `payment_integration` where dev_type='test'"
                
            elif processed_url == "production":
                integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name,redirect_url, cancel_url FROM `payment_integration` where dev_type='production'"
            else:
                frappe.msgprint("Please contact Administrator.")
                return

            c.execute(integration_dbvalue)
            integration_value = c.fetchall()
        except pymysql.Error as table_error:
            print(f"Table not found : {table_error}")
            return None
        finally:
          
            c.close()
        

        if integration_value:  
            for row in integration_value:
                access_code = row[0]
                working_key = row[1]
                merchant_id = row[2]
                site_name = row[3]
                redirect_url = row[4]
                cancel_url = row[5]

                passed_url = urlparse(url)
                db_url_name = urlparse(site_name)

                if passed_url.netloc == db_url_name.netloc:
                    p_merchant_id = merchant_id

                    p_billing_name = party_name
                    p_customer_identifier = roll_no
                    p_amount = amount
                    p_order_id = order_id
                   

                    merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + \
                        redirect_url + '&' + 'cancel_url=' + cancel_url + '&' + 'language=' + language + '&' + \
                        'billing_name=' + p_billing_name + '&' + \
                        'customer_identifier=' + p_customer_identifier

                    logger_login.info("Merchant_data: %s", merchant_data)
                    encryption = encrypt(merchant_data, working_key)
                    logger_login.info("Encryption_data: %s", encryption)

                    return {"encRequest": str(encryption), "accessCode": access_code, "baseUrl": url}

                else:
                    raise ValueError("Invalid URL")
        else:
            logging.warning("Please contact Administrator.")
            frappe.msgprint("Please contact Administrator.")

    except Exception as e:
        logger_login.error("Login Error: %s", str(e))
        return str(e)



@frappe.whitelist(allow_guest=True)
def get_order_status():
    try:
        transaction_data = frappe.request.args.get('transaction_data')
        if not transaction_data:
            return "Invalid transaction_data in the request."

        transaction_data = json.loads(transaction_data)
        response_data = transaction_data.get('response_data')

        if not response_data:
            return "Invalid response_data in the received data."

        order_id = response_data.get('order_id')
        transaction_id = response_data.get('tracking_id')
        order_status = response_data.get('order_status')
        amount_paid = response_data.get('mer_amount')
        billing_name = response_data.get('illing_name')
        time_of_transaction = response_data.get('trans_date')
        transaction_info = f"Order ID: {order_id}\nTransaction ID: {transaction_id}\nAmount Paid: {amount_paid}\nBilling Name: {billing_name}\nTime of Transaction: {time_of_transaction}"
        logger_transaction.info("cc Response:%s", response_data)
        if order_id and transaction_id:
            doc = frappe.get_doc("OnlinePayment", order_id)  # Assuming 'order_id' is the doc_name
            doc.transaction_id = transaction_id
            doc.transaction_status = order_status
            doc.transaction_status_description = transaction_info
            doc.date_time_of_transaction=time_of_transaction
            doc.save(ignore_permissions=True)
            doc.run_method('submit')

           
            return "Order status and tracking ID updated successfully in Frappe."
        else:
            return "Invalid 'order_id' or 'tracking_id' in the received data."

    except Exception as e:
        return f"Error processing the data: {str(e)}"


@frappe.whitelist(allow_guest=True)
def get_token(user):
    user_passed = 'hdfc'
    if user == user_passed:
        token = secrets.token_hex(32)
        frappe.session.data['api_token'] = token
        return {'token': token}
    else:
        return _('Invalid credentials.')
    


def getTransactionDetails(doc, url):
    processed_url = check_url(url)
    try:
        response = requests.get(url)
        current_url = response.url
        site_name = frappe.local.site 
        c = fetch_and_process_data(site_name)  # Assuming this function is defined elsewhere
        # integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name, dev_type,redirect_url ,cancel_url FROM `payment_integration`"
         
        if processed_url == "test":
            integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name,dev_type,redirect_url, cancel_url FROM `payment_integration` where dev_type='test'"
            
        elif processed_url == "production":
            integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name,dev_type,redirect_url, cancel_url FROM `payment_integration` where dev_type='production'"
        else:
            frappe.msgprint("Please contact Administrator.")
            return
        c.execute(integration_dbvalue)
        integration_value = c.fetchall()
        c.close()

        for row in integration_value:
            access_code = row[0]
            working_key = row[1]
            site_name = row[3]

            passed_url = urlparse(current_url)
            db_url_name = urlparse(site_name)

            if passed_url.netloc == db_url_name.netloc:
                orderNo = doc.name
                referenceNo = doc.transaction_id

                merchant_json_data = {
                    'reference_no': referenceNo,
                    'order_no': orderNo
                }

                merchant_data = json.dumps(merchant_json_data)
                encrypted_data = encrypt(merchant_data, working_key)

                final_data = 'enc_request='+encrypted_data+'&'+'access_code='+access_code + \
                             '&'+'command=orderStatusTracker&request_type=JSON&response_type=JSON'

                r = requests.post(
                    'https://apitest.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
                t = r.text
                key_value_pairs = t.split("&")

                enc_response_value = None
                for pair in key_value_pairs:
                    if pair.startswith("enc_response="):
                        enc_response_value = pair[len("enc_response="):]
                        break

                decryptData = decrypt(enc_response_value, working_key)

                start_idx = decryptData.find('{')
                end_idx = decryptData.rfind('}}') + 2
                json_string = decryptData[start_idx:end_idx]
                data_dict = json.loads(json_string)
                order_no = data_dict["Order_Status_Result"]["order_no"]
                order_status = data_dict["Order_Status_Result"]["order_status"]
                order_bank_ref_no = data_dict["Order_Status_Result"]["order_bank_response"]
                order_gross_amt = data_dict["Order_Status_Result"]["order_gross_amt"]
                order_amt = data_dict["Order_Status_Result"]["order_amt"]
                reference_no = data_dict["Order_Status_Result"]["reference_no"]
                order_date_time = data_dict["Order_Status_Result"]["order_status_date_time"]
                final_status_info = f"Order ID: {order_no}\nTransaction ID: {reference_no}\nGross Amount : {order_gross_amt}\nOrder Amount : {order_amt}\nOrder Status: {order_status}\nTime of Transaction: {order_date_time}\nBank Ref No.: {order_bank_ref_no}"

                doc.status = final_status_info
                # Logging the final_status_info
                logger_transaction.info("Status API Result:%s", data_dict)
               
                break

    except Exception as e:
        # Logging the error message
        logger_transaction.error(f"An error occurred: {str(e)}")
        return str(e)


    # else:
    #     raise ValueError("Invalid URL")


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




def create_or_update_table_with_data(data):
   
    conn = pymysql.connect('erpdb')
    cursor = conn.cursor()

   
    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS your_table_name (
			name         INT(11)  PRIMARY KEY,
			access_code  TEXT,
			working_key  TEXT,
			merchant_id  TEXT,
			site_name    VARCHAR(90),
			gateway_name VARCHAR(50),
			status       INT(11),
			event_date   DATETIME,
			user_name    VARCHAR(20),
			dev_type     VARCHAR(20),
			redirect_url VARCHAR(80),
			cancel_url   VARCHAR(80)
		);

    '''

    
    insert_or_update_sql = '''
        INSERT OR REPLACE INTO example_table (name ,access_code ,working_key ,merchant_id ,site_name ,gateway_name ,status ,event_date ,user_name ,dev_type ,redirect_url ,cancel_url )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

   
    cursor.execute(create_table_sql)
  
    for row in data:
        cursor.execute(insert_or_update_sql, (row['name'], row['access_code'], row['working_key'],row['merchant_id'],row['site_name'],row['gateway_name'],
                                              row['status'],row['event_date'],row['user_name'],row['dev_type'],row['redirect_url'],row['cancel_url']))

    conn.commit()
    conn.close()


data_to_insert = [
    {'name': 1, 'access_code': 'AVYA87KG31AX44AYXA', 'working_key': 'F5D6C4A01508C64EEF91EBDB72336ECB', 'merchant_id': '2649161', 'site_name': 'http://localhost:8000/app/onlinepayment/', 'gateway_name': 'hdfc', 
     'status': 1, 'event_date': '2023-08-02', 'user_name': 'rupali bhatta', 'dev_type': 'test', 'redirect_url': 'http://127.0.0.1:8080/ccavResponseHandler', 'cancel_url': 'http://127.0.0.1:8080/ccavResponseHandler'},

    {'name': 2, 'access_code': 'AVYA87KG31AX44AYXA', 'working_key': 'F5D6C4A01508C64EEF91EBDB72336ECB', 'merchant_id': '2649161', 'site_name': 'https://wscdemo.eduleadonline.com/app/onlinepayment/', 'gateway_name': 'hdfc', 
     'status': 1, 'event_date': '2023-08-02', 'user_name': 'rupali bhatta', 'dev_type': 'production', 'redirect_url': 'http://127.0.0.1:8080/ccavResponseHandler', 'cancel_url': 'http://127.0.0.1:8080/ccavResponseHandler'},

   
]


# create_or_update_table_with_data(data_to_insert)
