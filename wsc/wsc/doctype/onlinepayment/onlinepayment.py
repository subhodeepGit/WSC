# Copyright (c) 2022, SOUL ltd and contributors
# For license information, please see license.txt

from jpype import startJVM, shutdownJVM, java, addClassPath, JClass, JInt
addClassPath("/home/erpnext/frappe-bench/apps/wsc/wsc/wsc/doctype/onlinepayment/TokenClass.jar")
addClassPath("/home/erpnext/frappe-bench/apps/wsc/wsc/wsc/doctype/onlinepayment/CommerceConnect.jar")
startJVM(convertStrings=True)  #is used for the proper conversion of java.lang.String to Python string literals
import webbrowser
from urllib.request import urlopen
import frappe
from frappe.model.document import Document
from urllib.request import urlopen
import json
import datetime


class OnlinePayment(Document):
    def on_submit(doc): 
        getTransactionDetails(doc,doc.name)  
        frappe.msgprint("Your Transaction is completed. Your Transaction Id is " + doc.transactionid) 
             

        # def __init__(self):
        #     self.getTransactionDetails(doc,doc.name)  
        #     frappe.msgprint("Your Transaction is completed. Your Transaction Id is " + doc.transactionid)
       
       
def getTransactionDetails(doc,name):  
    getDoc=frappe.get_doc("ICICI settings Production")
    merchantId = getDoc.merchantid
    key=getDoc.key
    iv=getDoc.iv
    merchantTxnId=name
    fpTransactionId=""
    apiURL="https://www.fdconnect.com/FDConnectL3Services/getTxnInquiryDetail"     # Production Api
    try: 
        tokenclass = JClass('TokenClass')
        transactionDetailsData = tokenclass.inquiryTest(java.lang.String("%s"% merchantId), java.lang.String("%s"% key),
                                            java.lang.String("%s"%iv),java.lang.String("%s"% apiURL),
                                            java.lang.String("%s"% merchantTxnId),
                                            java.lang.String("%s"% fpTransactionId)) 
        
        transactionDetailsData = json.loads(str(transactionDetailsData)) 
           
        frappe.db.set_value("OnlinePayment",transactionDetailsData["saleTxnDetail"]["merchantTxnId"],"transactionid",transactionDetailsData["fpTransactionId"])
        frappe.db.set_value("OnlinePayment",transactionDetailsData["saleTxnDetail"]["merchantTxnId"],"transaction_status",transactionDetailsData["saleTxnDetail"]["transactionStatus"])        
        frappe.db.set_value("OnlinePayment",transactionDetailsData["saleTxnDetail"]["merchantTxnId"],"transaction_status_description",transactionDetailsData["saleTxnDetail"]["transactionStatusDescription"])         
        frappe.db.commit() 

        doc.transactionid=transactionDetailsData["fpTransactionId"] 
        doc.transaction_status=transactionDetailsData["saleTxnDetail"]["transactionStatus"]
        doc.transaction_status_description=transactionDetailsData["saleTxnDetail"]["transactionStatusDescription"]
               
    except Exception as err:
        print(repr(err))

    return str(transactionDetailsData) 
  

        
@frappe.whitelist()        
def getSessionToken(name,paying_amount): 
    getDoc=frappe.get_doc("ICICI settings Production")
    merchantId = getDoc.merchantid
    key=getDoc.key      
    iv=getDoc.iv
    configId= getDoc.configid
    apiURL="https://www.fdconnect.com/FDConnectL3Services/getToken"     # Production Api
    amountValue=paying_amount          
    currencyCode="INR" 
    merchantTxnId=name  
    transactionType="sale"    
    

    resultURL="https://paymentkp.eduleadonline.com/paymentreturn?id=" + name       #server  production

    try:
        tokenclass = JClass('TokenClass') 
        tokenId = tokenclass.getToken(java.lang.String("%s"% merchantId), java.lang.String("%s"% key),
                            java.lang.String("%s"%iv),java.lang.String("%s"% apiURL),
                            java.lang.String("%s"% amountValue),java.lang.String("%s"% currencyCode),java.lang.String("%s"% merchantTxnId),
                            java.lang.String("%s"% transactionType),java.lang.String("%s"% resultURL))
        
        if str(tokenId) != None:
            newURL= "https://www.fdconnect.com/Pay/?sessionToken=" + str(tokenId) + "&configId="+configId;             
           
        else :
            frappe.throw("Session has expired. Please create new transaction")  
                    
    except Exception as err:
        print(repr(err))

    return {"TokenId":str(tokenId),"configId":configId}






@frappe.whitelist()
def getDecryptedData(doc,encData=None,fdcTxnId=None):
    getDoc=frappe.get_doc("ICICI settings Production")
    merchantId = getDoc.merchantid
    apiURL="https://www.fdconnect.com/FDConnectL3Services/decryptMerchantResponse"     # Production Api
    try:
        
        if encData!=None and fdcTxnId!=None:
            tokenclass = JClass('TokenClass')
            decData = tokenclass.getDecryptResponse(java.lang.String("%s"% merchantId), java.lang.String("%s"% encData),
                                                    java.lang.String("%s"%fdcTxnId),java.lang.String("%s"% apiURL))             
            decData = json.loads(str(decData))
            # print("\n\n\n\n\n")
            # print("decData----------------",decData)
            
            # if decData["merchantTxnId"]!= None:
            # id= frappe.get_doc("OnlinePayment",decData["merchantTxnId"])
            if (decData["transactionStatus"]=="FAILED"):
                ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        
            else:
                ct=decData["transactionDateTime"]
                
    except Exception as e: 
        print(repr(e))
    if decData!=None:
        if "errorCode" in decData.keys():
            pass
        else :
            return {"transactionid":decData["fpTransactionId"],"transaction_status":decData["transactionStatus"],
                "transaction_status_description":decData["transactionStatusDescription"],"datetime":ct} 

    if decData==None:
        pass
               

@frappe.whitelist()        
def getTokenNew(name,paying_amount,partyNo,partyName,rollNo=None,SamsPortalId=None): 
    getDoc=frappe.get_doc("ICICI settings Production")
    merchantId = getDoc.merchantid
    key=getDoc.key      
    iv=getDoc.iv
    configId= getDoc.configid
    apiURL="https://www.fdconnect.com/FDConnectL3Services/getToken"     # Production Api
    amountValue=paying_amount          
    currencyCode="INR" 
    merchantTxnId=name  
    transactionType="sale"  
    party_No=partyNo
    party_Name=partyName     
    if rollNo !=None:
       roll_No=rollNo
    else :
        roll_No="rollNo"

        
    if SamsPortalId  !=None :
        SAMSPortalId=SamsPortalId
    else:
        SAMSPortalId="SamsPortalId"


    resultURL="https://paymentkp.eduleadonline.com/paymentreturn?id=" + name       #server  production

    try:
        tokenclass = JClass('TokenClass') 
        tokenId = tokenclass.getTokenNew(java.lang.String("%s"% merchantId), java.lang.String("%s"% key),
                            java.lang.String("%s"%iv),java.lang.String("%s"% apiURL),
                            java.lang.String("%s"% amountValue),java.lang.String("%s"% currencyCode),java.lang.String("%s"% merchantTxnId),
                            java.lang.String("%s"% transactionType),java.lang.String("%s"% resultURL),java.lang.String("%s"% party_No),
                            java.lang.String("%s"% party_Name),java.lang.String("%s"% roll_No),java.lang.String("%s"% SAMSPortalId))
        # print('\n\n\n\n\n\n\n') 
        # print(tokenId)                   
        
        if str(tokenId) != None:
            newURL= "https://www.fdconnect.com/Pay/?sessionToken=" + str(tokenId) + "&configId="+configId
           
        else :
            frappe.throw("Session has expired. Please create new transaction")  
    except Exception as err:
        print(repr(err))

    return {"TokenId":str(tokenId),"configId":configId}

# @frappe.whitelist()
# def submission(doc): 
# 	print("\n\n\n\n\n")
# 	print ("doc--->",doc)
# 	if doc!=None:
# 		submitDoc=frappe.get_doc("OnlinePayment",doc)
# 		print ("submitDoc--->",submitDoc)
# 		submitDoc.save()
# 		submitDoc.submit()

