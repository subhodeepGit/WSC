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
# from .database_operations import fetch_and_process_data
from .database_operations import fetch_config_data

from frappe import db

class OnlinePayment(Document):
	# def validate(self):
	# 	if self.paying_amount>self.total_outstanding_amout:
	# 		frappe.throw("Paying Amount can't be more then Total Outstanding Amount")
	# 	if self.total_outstanding_amout==0:
	# 		frappe.throw("Outstanding Amount can't be Rs.0 ")  

	def on_cancel(doc):
		frappe.throw("Once form is submitted it can't be cancelled")

	
	
	def on_submit(doc):
		get_url= frappe.utils.get_url()  
		logging.info(" get_url----->%s",get_url)     
		# getTransactionDetails(doc, 'http://erp.soulunileaders.com:8000/app/onlinepayment')
		getTransactionDetails(doc, get_url)
		frappe.msgprint("Your Transaction is completed. Your Transaction Id is " +
				doc.transaction_id + "."  " Status is " + frappe.bold(doc.transaction_status))
logging.basicConfig(filename='/home/erpnext/frappe-bench/apps/wsc/wsc/wsc/doctype/onlinepayment/transaction_log.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

currency = 'INR'
language = 'EN'

def check_url(p_url):
	parsed_url = urlparse(p_url)
	# logging.info("parsed_url: %s", parsed_url)
	if parsed_url.scheme == "http":
		return "test"
	else:
		return "production"
	

# @frappe.whitelist()
# def get_outstanding_amount(student):
# 	fee_voucher_list=frappe.get_all("Fees",filters=[["student","=",student],["outstanding_amount","!=",0],["docstatus","=",1]],
# 															fields=['outstanding_amount'],
# 															order_by="due_date asc")
# 	outstanding_amount=0
# 	for t in fee_voucher_list:
# 		outstanding_amount=t['outstanding_amount']+outstanding_amount
# 	return outstanding_amount

@frappe.whitelist()
def login(party_name, roll_no, amount, order_id, url): 
	logging.info("Processing login function...")

	logging.info("Input URL: %s", url)
	processed_url = check_url(url)
	logging.info("Processed URL: %s", processed_url)
	
	try:
		site_name = frappe.local.site 
		logging.info("site_name: %s", site_name)	
		config_file_path = "/home/erpnext/frappe-bench/apps/wsc/wsc/wsc/hdfcIntegration/hdfc_test_server_config.json"
		logging.info("config_file_path: %s", config_file_path)		
		config_data = fetch_config_data(config_file_path) 
		
		

		if processed_url == "test":
			if config_data:
					logging.info("config_data: %s", config_data)
					merchant_id = config_data.get("Merchant ID")
					access_code = config_data.get("Access Code")
					working_key = config_data.get("Working Key")
					redirect_url = config_data.get("Redirect URL")
					cancel_url = config_data.get("Cancel URL")
					site_name = config_data.get("Site Name")
					gateway_name = config_data.get("Gateway Name")
					dev_type = config_data.get("Dev Type")
		elif processed_url == "production":				
			if config_data:
				logging.info("config_data production: %s", config_data)
				merchant_id = config_data.get("Merchant ID")
				access_code = config_data.get("Access Code")
				working_key = config_data.get("Working Key")
				redirect_url = config_data.get("Redirect URL")
				cancel_url = config_data.get("Cancel URL")
				site_name = config_data.get("Site Name")
				gateway_name = config_data.get("Gateway Name")
				dev_type = config_data.get("Dev Type")

				# passed_url = urlparse(url)
				# logging.info("passed_url: %s", passed_url)

				# config_sitename = urlparse(site_name)
				# logging.info("config_sitename: %s", config_sitename)

				# logging.info("passed_url.netloc: %s", passed_url.netloc)
				# logging.info("config_sitename.netloc: %s", config_sitename.netloc)

		# else:
		# 	# Print a message or log an error
		# 	print("Please contact Administrator.")				

				
		

			# if passed_url.netloc == config_sitename.netloc:
			if 1==1:
				p_merchant_id = merchant_id
				p_billing_name = party_name
				p_customer_identifier = roll_no
				p_amount = amount
				p_order_id = order_id

				merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + \
					redirect_url + '&' + 'cancel_url=' + cancel_url + '&' + 'language=' + language + '&' + \
					'billing_name=' + p_billing_name + '&' + \
					'customer_identifier=' + p_customer_identifier

			
				encryption = encrypt(merchant_data, working_key)
				
				logging.info("encryption: %s", encryption)
				logging.info("accessCode: %s", access_code)
				logging.info("baseUrl: %s", url)
				return {"encRequest": str(encryption), "accessCode": access_code, "baseUrl": url}

			else:
				raise ValueError("Invalid URL")

	except Exception as e:
		
		return str(e)


@frappe.whitelist(allow_guest=True)
def get_order_status():
	try:
		transaction_data = frappe.request.args.get('transaction_data')
		print("\n\n\n\n\n transaction_data",transaction_data)
		if not transaction_data:
			return "Invalid transaction_data in the request."

		transaction_data = json.loads(transaction_data)
		response_data = transaction_data.get('response_data')
		print("\n\n\n\n\n response_data",response_data)

		if not response_data:
			return "Invalid response_data in the received data."

		order_id = response_data.get("b'order_id")[0]
		print("\n\n\n\n\n order_id",order_id)
		transaction_id = response_data.get('tracking_id')[0]
		print("\n\n\n\n\n transaction_id",transaction_id)
		order_status = response_data.get('order_status')[0]
		print("\n\n\n\n\n order_status",order_status)
		amount_paid = response_data.get('mer_amount')[0]
		print("\n\n\n\n\n amount_paid",amount_paid)
		billing_name = response_data.get('billing_name')[0]
		print("\n\n\n\n\n billing_name",billing_name)
		time_of_transaction = response_data.get('trans_date')[0]
		print("\n\n\n\n\n time_of_transaction",time_of_transaction)
		transaction_info = f"Order ID: {order_id}\nTransaction ID: {transaction_id}\nAmount Paid: {amount_paid}\nBilling Name: {billing_name}\nTime of Transaction: {time_of_transaction}"
		
		if order_id and transaction_id:
			print("\n\n\n\n\n\n   inside if.....................")
			print("\n\n\n\n\n order_id",order_id)
			print("\n\n\n\n\n transaction_id",transaction_id)
			doc = frappe.get_doc("OnlinePayment", order_id)  # Assuming 'order_id' is the doc_name
			
			print("\n\n\n\n\n\n   inside doc.....................",doc)
			doc.transaction_id = transaction_id
			doc.transaction_status = order_status
			doc.transaction_status_description = transaction_info
			doc.date_time_of_transaction=time_of_transaction
			try:
				print("\n\n\n\n\n\n   inside try.....................")
				doc.save(ignore_permissions=True)
				print("\n\n\n\n\n\n   inside save.....................")
				doc.run_method('submit')
				frappe.msgprint("Your Transaction is completed. Your Transaction Id is " +
				doc.transaction_id + "."  " Status is " + frappe.bold(doc.transaction_status))
				return "Order status and tracking ID updated successfully in Frappe."
			except Exception as save_exception:
				return f"Error saving document: {repr(save_exception)}"


		   
		# 	return "Order status and tracking ID updated successfully in Frappe."
		# else:
		# 	return "Invalid 'order_id' or 'tracking_id' in the received data."

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
		# c = fetch_and_process_data(site_name)  # Assuming this function is defined elsewhere
		# integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name, dev_type,redirect_url ,cancel_url FROM `payment_integration`"
		config_file_path = "/home/erpnext/frappe-bench/apps/wsc/wsc/wsc/hdfcIntegration/hdfc_test_server_config.json"
		logging.info("FSA config_file_path: %s", config_file_path)	
		config_data = fetch_config_data(config_file_path) 
		logging.info("FSA config_data: %s", config_data)

		# if processed_url == "test":
		if config_data:
				logging.info("FSA config_data Inside IF: %s", config_data)
				merchant_id = config_data.get("Merchant ID")
				access_code = config_data.get("Access Code")
				working_key = config_data.get("Working Key")
				redirect_url = config_data.get("Redirect URL")
				cancel_url = config_data.get("Cancel URL")
				site_name = config_data.get("Site Name")
				gateway_name = config_data.get("Gateway Name")
				dev_type = config_data.get("Dev Type")
			# integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name,dev_type,redirect_url, cancel_url FROM `payment_integration` where dev_type='test'"
			
		# elif processed_url == "production":
		# 	if config_data:
		# 			print("\n\n\n\n config_data", config_data)
		# 			merchant_id = config_data.get("Merchant ID")
		# 			access_code = config_data.get("Access Code")
		# 			working_key = config_data.get("Working Key")
		# 			redirect_url = config_data.get("Redirect URL")
		# 			cancel_url = config_data.get("Cancel URL")
		# 			site_name = config_data.get("Site Name")
		# 			gateway_name = config_data.get("Gateway Name")
		# 			dev_type = config_data.get("Dev Type")
			# integration_dbvalue = "SELECT access_code, working_key, merchant_id, site_name,dev_type,redirect_url, cancel_url FROM `payment_integration` where dev_type='production'"
		# else:
		# 	frappe.msgprint("Please contact Administrator.")
			
		# c.execute(integration_dbvalue)
		# integration_value = c.fetchall()
		# c.close()
		
			# passed_url = urlparse(current_url)
			# config_sitename = urlparse(site_name)

			# if passed_url.netloc == config_sitename.netloc:
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
				logging.info("Final API final_data: %s", final_data)
				r = requests.post(
					'https://apitest.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
				
				t = r.text
				logging.info("Final API Req: %s", r)
				key_value_pairs = t.split("&")
				logging.info("Final API key_value_pairs: %s", key_value_pairs)

				enc_response_value = None
				for pair in key_value_pairs:
					if pair.startswith("enc_response="):
						enc_response_value = pair[len("enc_response="):]
						logging.info("Final API enc_response_value: %s", enc_response_value)
						break

				decryptData = decrypt(enc_response_value, working_key)
				logging.info(" final_status_info decryptData: %s",decryptData)
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
				logging.info(" final_status_info : %s",data_dict)
				doc.status = final_status_info
				# logger_login the final_status_info
					
			   
				

	except Exception as e:
		# logger_login the error message
		
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
