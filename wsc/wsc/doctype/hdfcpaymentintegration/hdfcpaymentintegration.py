# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
# /home/erpnext/frappe-bench/apps/wsc/wsc/wsc/doctype/hdfcpaymentintegration/hdfcpaymentintegration.py
#Created By :Rupali_Bhatta : 17-07-2023
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
import logging
import os
import sys
username = os.getenv('USER')
module_path = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "hdfcpaymentintegration")
sys.path.append(module_path)
from .database_operations import fetch_and_process_data
# from  hdfcpaymentintegration.database_operations import fetch_and_process_data



class HdfcPaymentIntegration(Document):
    def on_cancel(doc):
        frappe.throw("Once form is submitted it can't be cancelled")

    def on_submit(doc):
        getTransactionDetails(
            doc, 'http://localhost:8000/app/hdfcpaymentintegration')
        frappe.msgprint("Your Transaction is completed. Your Transaction Id is " +
                        doc.transaction_id + "."  " Status is " + frappe.bold(doc.transaction_status))


# accessCode = 'AVYA87KG31AX44AYXA'
# workingKey = 'F5D6C4A01508C64EEF91EBDB72336ECB'
# merchant_id = '2649161'
# redirect_url: "http://127.0.0.1:8080/ccavResponseHandler",
# cancel_url: "http://127.0.0.1:8080/ccavResponseHandler",
currency = 'INR'
language = 'EN'


@frappe.whitelist()
def login(party_name, roll_no, amount, order_id, url):
#     # site_name = frappe.utils.get_site_name()
#     # print("Current site name:", site_name)
#     username = os.getenv('USER')
#     print("Username:", username)
#     site_name = frappe.local.site
#     print("Current site name:", site_name)
#     file_path = os.path.join("/home", username, "frappe-bench", "sites", site_name, "site_config.json")

#     # Read the JSON content from the file
#     with open(file_path, "r") as file:
#         config_data = json.load(file)

#     # Fetch the value of "db_name"
#     db_name = config_data["db_name"]

#     print("db_name:", db_name)


#     file_path = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "hdfcpaymentintegration", "db_name.txt")

# # Open the file for writing
#     with open(file_path, "w") as file:
#         file.write(db_name)



#     print("\n\n\n\n")
#     print("hdfcpaymentintegration.py url-----",url)
#     # http://erp.soulunileaders.com:8000/app/hdfcpaymentintegration/PAY-2023-0122
#     # netloc='erp.soulunileaders.com:8000'


#     try:
#         conn = pymysql.connect(
#             host="localhost",
#             user="hdfctest",
#             password="India@1234",
#             database=db_name)
#         c = conn.cursor()

    try:
        # fetch_and_process_data()
        c = fetch_and_process_data()


        integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name, dev_type,redirect_url ,cancel_url FROM `hdfc_test`"
        c.execute(integration_dbvalue)
        integration_value = c.fetchall()
        # print("\n\n\n\n")
        # print("integration_value data-----", integration_value)
        c.close()

        for row in integration_value:
            access_code = row[0]
            working_key = row[1]
            merchant_id = row[2]
            site_name = row[3]
            dev_type = row[4]
            redirect_url = row[5]
            cancel_url = row[6]

            passed_url = urlparse(url)
            print("\n\n\n\n")
            print("hdfcpaymentintegration.py passed_url-----", passed_url)
            db_url_name = urlparse(site_name)
            print("\n\n\n\n")
            print("hdfcpaymentintegration.py db_url_name-----", db_url_name)

            if passed_url.netloc == db_url_name.netloc:
                p_merchant_id = merchant_id

                p_billing_name = party_name
                p_customer_identifier = roll_no
                p_amount = amount
                p_order_id = order_id

                p_redirect_url = redirect_url
                p_cancel_url = cancel_url

                merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + \
                    p_redirect_url + '&' + 'cancel_url=' + p_cancel_url + '&' + 'language=' + language + '&' + \
                    'billing_name=' + p_billing_name + '&' + \
                    'customer_identifier=' + p_customer_identifier

                # print("\n\n\n\n\n\n")
                # print("merchant_data--",merchant_data)
                # You need to define the encrypt function
                encryption = encrypt(merchant_data, working_key)

                return {"encRequest": str(encryption), "accessCode": access_code, "baseUrl": url}

            else:
                raise ValueError("Invalid URL")

    except Exception as e:

        return str(e)


@frappe.whitelist(allow_guest=True)
def get_order_status():
    transaction_data = frappe.request.args.get('transaction_data')
    if transaction_data:
        try:
            transaction_data = json.loads(transaction_data)
            # print("\n\n\n\n")
            # print("rcvd data-----", transaction_data)
            response_data = (transaction_data['response_data'])
            # print("\n\n\n\n")
            # print("response_data data-----", response_data)
            doc_name = response_data.get('order_id')
            order_id = response_data.get('order_id')
            transaction_id = response_data.get('tracking_id')
            order_status = response_data.get('order_status')
            amount_paid = response_data.get('mer_amount')
            billing_name = response_data.get('illing_name')
            time_of_transaction = response_data.get('trans_date')
            transaction_info = f"Order ID: {order_id}\nTransaction ID: {transaction_id}\nAmount Paid: {amount_paid}\nBilling Name: {billing_name}\nTime of Transaction: {time_of_transaction}"
            # print("\n\n\n\n")
            # print("rcvd data transaction_info-----", transaction_info)

            if order_id and transaction_id:
                doc = frappe.get_doc("HdfcPaymentIntegration", doc_name)

                doc.transaction_id = transaction_id
                doc.transaction_status = order_status

                doc.transaction_info = transaction_info

                doc.save(ignore_permissions=True)

                doc.run_method('submit')
                return "Order status and tracking ID updated successfully in Frappe."
            else:
                return "Invalid 'order_id' or 'tracking_id' in the received data."
        except Exception as e:
            return f"Error processing the data: {str(e)}"
    else:
        return "Invalid transaction_data in the request."


@frappe.whitelist(allow_guest=True)
def get_token(user):
    user_passed = 'hdfc'
    if user == user_passed:
        token = secrets.token_hex(32)
        frappe.session.data['api_token'] = token
        return {'token': token}
    else:
        return _('Invalid credentials.')


# 4012 0010 3714 1112


def getTransactionDetails(doc, url):
    try:
        response = requests.get(url)
        current_url = response.url
        # print("\n\n\n\n\n\n")
        # print("current_url--", current_url)

        conn = pymysql.connect(
            host="localhost",
            user="hdfctest",
            password="India@1234",
            database="erpdb")
        c = conn.cursor()

        integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name, dev_type,redirect_url ,cancel_url FROM `hdfc_test`"
        c.execute(integration_dbvalue)
        integration_value = c.fetchall()
        # print("\n\n\n\n")
        # print("integration_value data-----", integration_value)
        c.close()

        for row in integration_value:
            access_code = row[0]
            working_key = row[1]
            site_name = row[3]

            passed_url = urlparse(current_url)
            print("\n\n\n\n")
            print("hdfcpaymentintegration.py passed_url-----", passed_url)
            db_url_name = urlparse(site_name)
            print("\n\n\n\n")
            print("hdfcpaymentintegration.py db_url_name-----", db_url_name)

            if passed_url.netloc == db_url_name.netloc:
                orderNo = doc.name
                referenceNo = doc.transaction_id

                merchant_json_data = {
                    'reference_no': referenceNo,
                    'order_no': orderNo
                }

                merchant_data = json.dumps(merchant_json_data)
                # print("\n\n\n\n")
                # print("merchant_data-->", merchant_data)
                encrypted_data = encrypt(merchant_data, working_key)

                final_data = 'enc_request='+encrypted_data+'&'+'access_code='+access_code + \
                    '&'+'command=orderStatusTracker&request_type=JSON&response_type=JSON'
                # print("\n\n\n\n")
                # print("final_data-->", final_data)
                r = requests.post(
                    'https://apitest.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
                t = r.text
                # print("\n\n\n\n")
                # print("RES r-->", r.text)
                key_value_pairs = t.split("&")
                # Iterate through the key-value pairs to find the 'enc_response' value
                enc_response_value = None
                for pair in key_value_pairs:
                    if pair.startswith("enc_response="):
                        enc_response_value = pair[len("enc_response="):]
                        break

                decryptData = decrypt(enc_response_value, working_key)
                # print("\n\n\n\n")
                # print("decryptData-->", decryptData)
                start_idx = decryptData.find('{')
                end_idx = decryptData.rfind('}}') + 2  # Add 2 to include the last two '}' characters
                json_string = decryptData[start_idx:end_idx]
                # print(json_string)
                data_dict = json.loads(json_string)
                # print("\n\n\n", data_dict)
                # Now, you can access the values from the dictionary
                order_no = data_dict["Order_Status_Result"]["order_no"]
                # print("\n\n\n", order_no)
                order_status = data_dict["Order_Status_Result"]["order_status"]

                order_bank_ref_no = data_dict["Order_Status_Result"]["order_bank_response"]

                order_gross_amt = data_dict["Order_Status_Result"]["order_gross_amt"]

                order_amt = data_dict["Order_Status_Result"]["order_amt"]

                reference_no = data_dict["Order_Status_Result"]["reference_no"]

                order_date_time = data_dict["Order_Status_Result"]["order_status_date_time"]

                final_status_info = f"Order ID: {order_no}\nTransaction ID: {reference_no}\nGross Amount : {order_gross_amt}\nOrder Amount : {order_amt}\nOrder Status: {order_status}\nTime of Transaction: {order_date_time}\nBank Ref No.: {order_bank_ref_no}"
                # print("\n\n\n\n")
                # print("final_status_info-->", final_status_info)
                doc.status = final_status_info
                break

    except Exception as e:
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
    {'name': 1, 'access_code': 'AVYA87KG31AX44AYXA', 'working_key': 'F5D6C4A01508C64EEF91EBDB72336ECB', 'merchant_id': '2649161', 'site_name': 'http://localhost:8000/app/hdfcpaymentintegration/', 'gateway_name': 'hdfc', 
     'status': 1, 'event_date': '2023-08-02', 'user_name': 'rupali bhatta', 'dev_type': 'test', 'redirect_url': 'http://127.0.0.1:8080/ccavResponseHandler', 'cancel_url': 'http://127.0.0.1:8080/ccavResponseHandler'},

    {'name': 2, 'access_code': 'AVYA87KG31AX44AYXA', 'working_key': 'F5D6C4A01508C64EEF91EBDB72336ECB', 'merchant_id': '2649161', 'site_name': 'https://wscdemo.eduleadonline.com/app/hdfcpaymentintegration/', 'gateway_name': 'hdfc', 
     'status': 1, 'event_date': '2023-08-02', 'user_name': 'rupali bhatta', 'dev_type': 'production', 'redirect_url': 'http://127.0.0.1:8080/ccavResponseHandler', 'cancel_url': 'http://127.0.0.1:8080/ccavResponseHandler'},

   
]


# create_or_update_table_with_data(data_to_insert)
