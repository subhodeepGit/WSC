#!/usr/bin/python
#Created By :Rupali_Bhatta : 17-07-2023
from ccavutil import encrypt, decrypt
from string import Template
from urllib.parse import parse_qs
import requests
import json
import pymysql
from urllib.parse import urlparse
import os


def res(encResp,url):
      
    try:
        
        print("\n\n\n\n ccResponse  res  url",url)
        # ccResponse  res  url http://127.0.0.1:8080/ccavResponseHandler
        username = os.getenv('USER')
        file_path = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "hdfcpaymentintegration", "db_name.txt")

    # Read the value from the file
        with open(file_path, "r") as file:
            db_name = file.read().strip()

        if db_name:
            print("db_name in Other Program:", db_name)
        else:
            print("db_name not found.")

        conn = pymysql.connect(
            host="localhost",
            user="hdfctest",
            password="India@1234",
            database=db_name)
        c = conn.cursor()

        integration_dbvalue = "SELECT  working_key,redirect_url,cancel_url, site_name FROM `hdfc_test`"
        c.execute(integration_dbvalue)
        integration_value = c.fetchall()
        # print("\n\n\n\n")
        # print("ccResponse DB data-----", integration_value)
        c.close()

        for row in integration_value:
            db_working_key = row[0]
            db_redirect_url = row[1]
            print("\n\n\n\n")
            print("ccResponse db_redirect_url-----", db_redirect_url)
            cancel_url = row[2]
            db_base_redirect_url = row[3]
            print("\n\n\n\n")
            print("ccResponse db_base_redirect_url-----", db_base_redirect_url)

            passed_url = urlparse(url)
            print("\n\n\n\n")
            print("ccResponse passed_url-----", passed_url)
            db_url_name = urlparse(db_redirect_url)
            print("\n\n\n\n")
            print("ccResponse db_url_name-----", db_url_name)

            if passed_url.netloc == db_url_name.netloc:
                
    
                decResp = decrypt(encResp, db_working_key)
                parsed_data = parse_qs(decResp)
                # print("ccResponse parsed_data:::::::::", parsed_data)
                cleaned_data = {key.strip("b'"): value[0] if value else None for key, value in parsed_data.items()}

                order_id = cleaned_data.get('order_id', None)
                tracking_id = cleaned_data.get('tracking_id', None)
                order_status = cleaned_data.get('order_status', None)
                amount = cleaned_data.get('amount', None)
                billing_name = cleaned_data.get('illing_name', None)
                trans_date = cleaned_data.get('trans_date', None)

                # base_redirect_url = 'http://localhost:8000/app/hdfcpaymentintegration/'
                                        
                redirect_url = "{}{}".format(db_base_redirect_url, order_id)
                print("\n\n\n\n\n ccResponse redirect_url",redirect_url)
                #  ccResponse redirect_url http://erp.soulunileaders.com:8000/app/PAY-2023-0122

                base_url = urlparse(db_base_redirect_url).scheme + "://" + urlparse(db_base_redirect_url).netloc
                print("\n\n\n\n\n ccResponse base_url",base_url)
                # ccResponse base_url http://erp.soulunileaders.com:8000

                api_endpoint_get_token = '/api/method/wsc.wsc.doctype.hdfcpaymentintegration.hdfcpaymentintegration.get_token'
                api_getToken = base_url + api_endpoint_get_token

                # api_getToken = 'http://localhost:8000/api/method/wsc.wsc.doctype.hdfcpaymentintegration.hdfcpaymentintegration.get_token'
                user = 'hdfc'	
                response = requests.post(api_getToken, json={'user': user})
                if response.status_code == 200:
                    try:
                        data = response.json()
                        token = data['message']['token'].strip()
                    
                    except json.JSONDecodeError:
                        print("Invalid JSON response from the API.")
                    if token:
                        
                        transaction_data = {
                            'response_data': cleaned_data
                        }
                        # print("\n\n\n\n\n")
                        # print("ccResponse data sending---",transaction_data)

                        headers = {
                        'Authorization': f'Bearer {token}'  
                        }


                        m_base_url = urlparse(db_base_redirect_url).scheme + "://" + urlparse(db_base_redirect_url).netloc
                        print("\n\n\n\n\n m_base_url",m_base_url)
                        api_endpoint_get_order_status = '/api/method/wsc.wsc.doctype.hdfcpaymentintegration.hdfcpaymentintegration.get_order_status'
                        frappe_api_endpoint = m_base_url + api_endpoint_get_order_status

                        # frappe_api_endpoint = 'http://localhost:8000/api/method/wsc.wsc.doctype.hdfcpaymentintegration.hdfcpaymentintegration.get_order_status'


                        params = {
                            'transaction_data': json.dumps(transaction_data)  
                        }
                        response = requests.post(frappe_api_endpoint, params=params, headers=headers)
                        

                        try:
                            
                            if transaction_data['response_data']["order_status"]:									
                                print("Order status updated successfully in Frappe.")
                            else:
                                print("Failed to update order status in Frappe:")
                        except json.JSONDecodeError:
                            print("Invalid JSON response from the Frappe API.")
                        except Exception as e:
                            print("Error while communicating with Frappe API:", str(e))

                    else:
                        print("Token not found in the response.", response.status_code)
                else:
                    print("Failed to get the token. Status code:", response.status_code)

    except Exception as e:       

        return str(e)        


    html = '''\
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Transaction Status</title>
            <style>

        body {
            background: #ffffff; 
        }

        .center-screen {
        margin-top: 300px;
        display: block;
        justify-content: center;
        align-items: center;
        text-align: center;
        }
            </style>

            <body>
                <pre class="center-screen">
                <h2 style="font-size:24px;">Processing...</h2>
                
                </pre>
            <script>
                    
                    var redirect_url = '$redirect_url';
                    
                    // Delay the redirection by 5 seconds (5000 milliseconds)
                    setTimeout(function() {
                        window.location.href = redirect_url;
                    },1000);
            </script>
                
            </body>
        </head>

        </html>

    '''
    data_to_substitute = {
        'order_id': order_id,
        'order_status': order_status,
        'tracking_id': tracking_id,
        'amount': amount,
        'trans_date': trans_date,
        'redirect_url': redirect_url
    }

    html_content = Template(html).safe_substitute(data_to_substitute)
    # fin = Template(html).safe_substitute(response=data)
    return html_content
