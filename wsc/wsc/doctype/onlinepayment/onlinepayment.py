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
import os
import logging
from wsc.wsc.notification.custom_notification import email_transaction_status
from datetime import datetime

class OnlinePayment(Document):
    def validate(self):
        if self.paying_amount<10:
            frappe.throw("Paying amount can't be less the <b>Rs.10</b>")

        if self.paying_amount>self.total_outstanding_amout:
            frappe.throw("Paying Amount can't be more then Total Outstanding Amount")
        if self.total_outstanding_amout==0:
            frappe.throw("Outstanding Amount can't be Rs.0 ")  
        if self.is_new() and self.docstatus==0:
            data=frappe.get_all("OnlinePayment",{"transaction_status":"success","payment_status":0,"party":self.party})    
            if data:
                frappe.throw("The last transaction was successful.A receipt for money will be generated.")

    def on_cancel(doc):
        frappe.throw("Once form is submitted it can't be cancelled")    
    
    def on_submit(doc):
        # getTransactionDetails(doc)
        email_transaction_status(doc)
        frappe.msgprint("Your Transaction is completed. Your Transaction Id is " +
                doc.transaction_id + "."  " Status is " + frappe.bold(doc.transaction_status))
        
# logging.basicConfig(filename='/home/erpnext/frappe-bench/apps/wsc/wsc/wsc/doctype/onlinepayment/transaction_log.log', level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
def find_file_path(filename):
    for dirpath, dirnames, filenames in os.walk('/'):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None

file_name_transaction_log = 'transaction_log.log'
file_path_transaction_log = find_file_path(file_name_transaction_log)
# print("\n\n\n\n\n\n--------------------->", file_path_transaction_log)
# '/home/wsc/frappe-bench/apps/wsc/wsc/wsc/doctype/onlinepayment/transaction_log.log'

logging.basicConfig(filename=file_path_transaction_log, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
currency = 'INR'
language = 'EN'
   

@frappe.whitelist()
def get_outstanding_amount(student):
	fee_voucher_list=frappe.get_all("Fees",filters=[["student","=",student],["outstanding_amount","!=",0],["docstatus","=",1]],
															fields=['outstanding_amount'],
															order_by="due_date asc")
	outstanding_amount=0
	for t in fee_voucher_list:
		outstanding_amount=t['outstanding_amount']+outstanding_amount
	return outstanding_amount

@frappe.whitelist()
def open_gateway(party_name, party, amount, order_id,url,gw_provider,form_status,formProgress): 
    
   
    if form_status == "Yes" :
        frappe.throw("Please Save the Form Before Initiate The Transaction.")
    if formProgress=="Initiated" or formProgress=="Completed"  :
        frappe.throw("Your Last Transaction was already Initiated by the Bank. So please Initiate New Transaction.")

    data=frappe.get_all("OnlinePayment",{"transaction_status":"success","payment_status":0,"party":party})  
    if data:
        frappe.throw("Last Transaction is not yet settled.So new Transaction can not be initiated.") 

    logging.info("Processing open_gateway function...1")
    logging.info("op url passed 2 %s",url)
    logging.info("op gw_provider 3%s", gw_provider)

    try:       
        if gw_provider == "hdfc": 
            progress_doc=frappe.get_doc("OnlinePayment",order_id)
            progress_doc.transaction_progress="Initiated"
            progress_doc.save()
            getDoc = frappe.get_doc("HDFCSetting")            
            logging.info("op getDoc 4: %s", getDoc)
            is_prod = getDoc.get("is_production")
            # is_prod = frappe.get_value("HDFCSetting", None, "is_prod")
            logging.info("is_prod 5: %s", is_prod)
            
            if is_prod is 0:
                logging.info("if is_prod is 0: %s", is_prod)
                merchant_id = getDoc.get("merchant_id")
                access_code = getDoc.get("access_code")
                working_key = getDoc.get("working_key")
                redirect_url = getDoc.get("redirect_url")
                cancel_url = getDoc.get("cancel_url")
                site_name = getDoc.get("site_name")
                gateway_name = gw_provider
                dev_type = getDoc.get("dev_type")
                logging.info("merchant_id : %s", merchant_id)
                
                p_merchant_id = merchant_id
                p_billing_name = party_name
                p_customer_identifier = party
                p_amount = amount
                p_order_id = order_id
                p_merchant_url = url
                logging.info("p_merchant_url : %s", p_merchant_url)

                merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + redirect_url + '&' + 'cancel_url=' + cancel_url + '&' + 'language=' + language + '&' + 'billing_name=' + p_billing_name + '&' + 'customer_identifier=' + p_customer_identifier + '&' + 'merchant_param1='+ p_merchant_url + '&' + 'delivery_name=' + gateway_name
                # merchant_data = 'tid='+ party + '&' + 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + redirect_url + '&' + 'cancel_url=' + cancel_url + '&' + 'language=' + language + '&' + 'billing_name=' + p_billing_name + '&' + 'customer_identifier=' + p_customer_identifier + '&' + 'merchant_param1='+ p_merchant_url + '&' + 'delivery_name=' + gateway_name
                logging.info("merchant_data : %s", merchant_data)
                encryption = encrypt(merchant_data, working_key)

                logging.info("encryption 5: %s", encryption)
                logging.info("accessCode 6: %s", access_code)
                logging.info("is_prod 7: %s", is_prod)
                
                return {"encRequest": str(encryption), "accessCode": access_code, "is_prod": is_prod}
                
            elif is_prod is 1:
                logging.info("is_prod is 1: %s", is_prod)
                myDoc = frappe.get_doc("HDFCSetting")
                merchant_id = myDoc.get("merchant_id")
                access_code = myDoc.get("access_code")
                working_key = myDoc.get("working_key")
                redirect_url = myDoc.get("redirect_url")
                cancel_url = myDoc.get("cancel_url")
                site_name = myDoc.get("site_name")
                gateway_name = myDoc.get("gateway_name")
                dev_type = myDoc.get("dev_type")
                logging.info("merchant_id : %s", merchant_id)
            
                p_merchant_id = merchant_id
                p_billing_name = party_name
                p_customer_identifier = party
                p_amount = amount
                p_order_id = order_id
                p_merchant_url = url
                logging.info("p_merchant_url : %s", p_merchant_url)

                merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + redirect_url + '&' + 'cancel_url=' + cancel_url + '&' + 'language=' + language + '&' + 'billing_name=' + p_billing_name + '&' + 'customer_identifier=' + p_customer_identifier + '&' + 'merchant_param1='+ p_merchant_url + '&' + 'delivery_name=' + gateway_name
                
                logging.info("merchant_data : %s", merchant_data)
                encryption = encrypt(merchant_data, working_key)

                logging.info("encryption 5: %s", encryption)
                logging.info("accessCode 6: %s", access_code)
                logging.info("is_prod 7: %s", is_prod)
                
                return {"encRequest": str(encryption), "accessCode": access_code, "is_prod": is_prod}

            else:
                frappe.throw("Error: is_prod value is None")

#################################################  AXIS GATEWAY  ########################################################################

        if gw_provider == "AXIS":
            getDoc = frappe.get_doc("AXIS Settings")
            logging.info("AXIS--"+"op getDoc 4: %s", getDoc)
            is_prod = getDoc.get("is_production")
            logging.info("AXIS--"+"is_prod 5: %s", is_prod)
            
            if is_prod == 0:
                logging.info("AXIS--"+"if is_prod is 0: %s", is_prod)
                merchant_id = getDoc.get("merchant_id")
                access_code = getDoc.get("access_code")
                working_key = getDoc.get("working_key")
                redirect_url = getDoc.get("redirect_url")
                cancel_url = getDoc.get("cancel_url")
                site_name = getDoc.get("site_name")
                gateway_name = gw_provider
                dev_type = getDoc.get("dev_type")
                logging.info("AXIS--"+"merchant_id : %s", merchant_id)
                
                p_merchant_id = merchant_id
                p_billing_name = party_name
                p_customer_identifier = party

                p_amount = amount
                p_order_id = order_id
                p_merchant_url = url
                logging.info("AXIS--"+"p_merchant_url : %s", p_merchant_url)

                merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + redirect_url + '&' + 'cancel_url=' + cancel_url + '&' + 'language=' + language + '&' + 'billing_name=' + p_billing_name + '&' + 'customer_identifier=' + p_customer_identifier + '&' + 'merchant_param1='+ p_merchant_url + '&' + 'delivery_name=' + gateway_name
                
                logging.info("AXIS--"+"merchant_data : %s", merchant_data)
                encryption = encrypt(merchant_data, working_key)

                logging.info("AXIS--"+"encryption 5: %s", encryption)
                logging.info("AXIS--"+"accessCode 6: %s", access_code)
                logging.info("AXIS--"+"is_prod 7: %s", is_prod)
                
                return {"encRequest": str(encryption), "accessCode": access_code, "is_prod": is_prod}
                
            elif is_prod is 1:
                logging.info("AXIS--"+"is_prod is 1: %s", is_prod)
                myDoc = frappe.get_doc("AXIS Settings")
                merchant_id = myDoc.get("merchant_id")
                access_code = myDoc.get("access_code")
                working_key = myDoc.get("working_key")
                redirect_url = myDoc.get("redirect_url")
                cancel_url = myDoc.get("cancel_url")
                site_name = myDoc.get("site_name")
                gateway_name = myDoc.get("gateway_name")
                dev_type = myDoc.get("dev_type")
                logging.info("AXIS--"+"merchant_id : %s", merchant_id)
            
                p_merchant_id = merchant_id
                p_billing_name = party_name
                p_customer_identifier = party
                p_amount = amount
                p_order_id = order_id
                p_merchant_url = url
                logging.info("AXIS--"+"p_merchant_url : %s", p_merchant_url)

                merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + redirect_url + '&' + 'cancel_url=' + cancel_url + '&' + 'language=' + language + '&' + 'billing_name=' + p_billing_name + '&' + 'customer_identifier=' + p_customer_identifier + '&' + 'merchant_param1='+ p_merchant_url + '&' + 'delivery_name=' + gateway_name
                
                logging.info("AXIS--"+"merchant_data : %s", merchant_data)
                encryption = encrypt(merchant_data, working_key)

                logging.info("AXIS--"+"encryption 5: %s", encryption)
                logging.info("AXIS--"+"accessCode 6: %s", access_code)
                logging.info("AXIS--"+"is_prod 7: %s", is_prod)
                
                return {"encRequest": str(encryption), "accessCode": access_code, "is_prod": is_prod}
                
            else:
                frappe.throw("Error: is_prod value is None")

    except Exception as e:
        # return str(e)
        logging.info("Error saving document:", str(e))


@frappe.whitelist(allow_guest=True)
def get_order_status():
    try:
        transaction_data = frappe.request.args.get('transaction_data')
        logging.info("transaction_data- %s",transaction_data)
        if not transaction_data:
            return "Invalid transaction_data in the request."

        transaction_data = json.loads(transaction_data)
        response_data = transaction_data.get('response_data')
        logging.info("response_data-%s",response_data)

        if not response_data:
            return "Invalid response_data in the received data."

        order_id = response_data.get("b'order_id")[0]
        logging.info(" order_id-%s",order_id)
        transaction_id = response_data.get('tracking_id')[0]
        logging.info(" transaction_id %s",transaction_id)
        order_status = response_data.get('order_status')[0]
        logging.info(" order_status %s",order_status)
        amount_paid = response_data.get('mer_amount')[0]
        logging.info(" amount_paid %s",amount_paid)
        billing_name = response_data.get('billing_name')[0]
        logging.info(" billing_name %s",billing_name)
        
        if "trans_date" in response_data:          
            
            if response_data["trans_date"][0]=='null':                
                time_of_transaction= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(" time_of_transaction %s",time_of_transaction)
            else:
                
                transaction_time = response_data.get('trans_date')[0]               
                logging.info(" server transaction_time %s",transaction_time)
                date_obj = datetime.strptime(transaction_time, "%d/%m/%Y %H:%M:%S")
                time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")

                # time_of_transaction = response_data.get('trans_date')[0]
                logging.info(" time_of_transaction %s",time_of_transaction)
        else:
                     
            transaction_time = response_data.get('order_date_time')[0]
            logging.info(" server transaction_time %s",transaction_time)
            date_obj = datetime.strptime(transaction_time, "%d/%m/%Y %H:%M:%S")
            time_of_transaction = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            # time_of_transaction = response_data.get('trans_date')[0]
            logging.info(" time_of_transaction %s",time_of_transaction)          

       
        status_message = response_data.get('status_message')[0]
        logging.info(" status_message %s",status_message) 
        gateway_name = response_data.get('delivery_name')[0]
        gateway_nameinupper=gateway_name.upper()
        logging.info(" gateway_name %s", gateway_name)
        transaction_info = f"Order ID: {order_id}\nStatus Message: {status_message}\nPaying Amount: {amount_paid}\nBilling Name: {billing_name}"
       
        
        # if order_id and transaction_id:
        if order_status !='Timeout':
            logging.info("inside if.....................")
            logging.info(" order_id %s",order_id)
            logging.info(" transaction_id %s",transaction_id)
            doc = frappe.get_doc("OnlinePayment", order_id)  # 'order_id' is the doc_name
            
            logging.info("inside doc.....................%s",doc)
            doc.transaction_id = transaction_id
            doc.transaction_status = order_status
            doc.transaction_status_description = transaction_info
            doc.date_time_of_transaction=time_of_transaction
            doc.gateway_name=gateway_nameinupper
            doc.transaction_progress="Completed"
            
            try:
                logging.info("inside try.....................")
                doc.save(ignore_permissions=True)
                logging.info("inside save.....................")
                doc.submit()
                getTransactionDetails(doc)
                frappe.msgprint("Your Transaction is completed. Your Transaction Id is " +doc.transaction_id + "."  " Status is " + frappe.bold(doc.transaction_status))
                # return "Order status and tracking ID updated successfully in Frappe."
                logging.info("Order status and tracking ID updated successfully in Frappe.")
            except Exception as save_exception:
                # return f"Error saving document: {repr(save_exception)}"
                logging.info(f"Error saving document: {repr(save_exception)}")

    except Exception as e:
        # return f"Error processing the data: {str(e)}"
        logging.info(f"Error processing the data: {str(e)}")


@frappe.whitelist(allow_guest=True)
def get_token(user):
    # user_passed = 'hdfc'
    # if user == user_passed:
    if user == 'hdfc':
        token = secrets.token_hex(32)
        frappe.session.data['api_token'] = token
        return {'token': token}
    
    if user == 'axis':
        token = secrets.token_hex(32)
        frappe.session.data['api_token'] = token
        return {'token': token}
    else:
        return _('Invalid credentials.')

def getTransactionDetails(doc):    
    try:                                
        getDoc = frappe.get_doc("HDFCSetting")
        logging.info("gt getDoc: %s", getDoc)
        is_prod = getDoc.get("is_production")
        # is_prod = frappe.get_value("HDFCSetting", None, "is_prod")
        logging.info("gt is_prod: %s", is_prod)
        
        if is_prod is 0:
            logging.info("is_prod is 0: %s", is_prod)           
            access_code = getDoc.get("access_code")
            working_key = getDoc.get("working_key")
           
            orderNo = doc.name
            referenceNo = doc.transaction_id

            merchant_json_data = {                
                'order_no': orderNo
            }

            merchant_data = json.dumps(merchant_json_data)
            encrypted_data = encrypt(merchant_data, working_key)

            final_data = 'enc_request='+encrypted_data+'&'+'access_code='+access_code + \
                            '&'+'command=orderStatusTracker&request_type=JSON&response_type=JSON'
            logging.info("Final API final_data: %s", final_data)
            r = requests.post('https://login.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
            # r = requests.post('https://api.ccavenue.com/apis/servlet/DoWebTran', params=final_data)
            # r = requests.post('https://apitest.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
            

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
            logging.info(" order_status: %s",order_status)
            order_bank_ref_no = data_dict["Order_Status_Result"]["order_bank_response"]
            order_gross_amt = data_dict["Order_Status_Result"]["order_gross_amt"]
            order_amt = data_dict["Order_Status_Result"]["order_amt"]
            reference_no = data_dict["Order_Status_Result"]["reference_no"]
            order_date_time = data_dict["Order_Status_Result"]["order_status_date_time"]
            
            final_status_info = f"Order ID: {order_no}\nTransaction ID: {reference_no}\nGross Amount : {order_gross_amt}\nOrder Amount : {order_amt}\nOrder Status: {order_status}\nTime of Transaction: {order_date_time}\nBank Ref No.: {order_bank_ref_no}"
            logging.info(" final_status_info : %s",data_dict)
            logging.info(" SUCESSFULLY COMPLETED")

           
            final_api = frappe.new_doc("HDFC Final Transaction Status")   
            final_api.transactionid = reference_no
            final_api.order_status = order_status
            final_api.order_number = order_no
            final_api.order_gross_amount = order_gross_amt
            final_api.order_amount = order_amt
            final_api.dev_type =  "Test"   
            final_api.transaction_status = final_status_info
            final_api.save(ignore_permissions=True)           
            # final_api.run_method('submit')   
            final_api.submit()        
            # doc.status = final_status_info

        elif is_prod is 1:
            logging.info("is_prod is : %s", is_prod)
            myDoc = frappe.get_doc("HDFCSetting")
            logging.info("is_prod is None inside If 4: %s", is_prod)           
            access_code = myDoc.get("access_code")
            working_key = myDoc.get("working_key")
           
            orderNo = doc.name
            referenceNo = doc.transaction_id

            merchant_json_data = {
               
                'order_no': orderNo
            }

            merchant_data = json.dumps(merchant_json_data)
            encrypted_data = encrypt(merchant_data, working_key)

            final_data = 'enc_request='+encrypted_data+'&'+'access_code='+access_code + \
                            '&'+'command=orderStatusTracker&request_type=JSON&response_type=JSON'
            logging.info("Final API final_data: %s", final_data)
            r = requests.post('https://login.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
            # r = requests.post('https://api.ccavenue.com/apis/servlet/DoWebTran', params=final_data)
            # r = requests.post('https://apitest.ccavenue.com/apis/servlet/DoWebTrans', params=final_data)
            
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
            logging.info("Data Dict :%s",data_dict)
            order_no = data_dict["Order_Status_Result"]["order_no"]
            order_status = data_dict["Order_Status_Result"]["order_status"]
            order_bank_ref_no = data_dict["Order_Status_Result"]["order_bank_ref_no"]
            order_gross_amt = data_dict["Order_Status_Result"]["order_gross_amt"]
            order_amt = data_dict["Order_Status_Result"]["order_amt"]
            reference_no = data_dict["Order_Status_Result"]["reference_no"]
            order_date_time = data_dict["Order_Status_Result"]["order_status_date_time"]
            order_status_reason= data_dict["Order_Status_Result"]["order_bank_response"]
            final_status_info = f"Order ID: {order_no}\nTransaction ID: {reference_no}\nGross Amount : {order_gross_amt}\nOrder Amount : {order_amt}\nOrder Status: {order_status}\nTime of Transaction: {order_date_time}\nBank Ref No.: {order_bank_ref_no}\nBank Response.:{order_status_reason}"
            logging.info(" final_status_info : %s",data_dict)
            logging.info(" SUCESSFULLY COMPLETED")
            
            final_api = frappe.new_doc("HDFC Final Transaction Status")   
            final_api.transactionid = reference_no
            final_api.order_status = order_status
            final_api.order_number = order_no
            final_api.order_gross_amount = order_gross_amt
            final_api.order_amount = order_amt
            final_api.dev_type =  "Production"   
            final_api.transaction_status = final_status_info
            final_api.save(ignore_permissions=True)           
            # final_api.run_method('submit')        
            final_api.submit()   
            # doc.status = final_status_info
            
        else:
            frappe.throw("Error: is_prod value is None")  

    except Exception as e:	
        return str(e)
    

           

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



