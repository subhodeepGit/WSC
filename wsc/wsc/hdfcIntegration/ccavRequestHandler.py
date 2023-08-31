#!/usr/bin/python
#Created By :Rupali_Bhatta : 17-07-2023
from flask import request, redirect, Flask, render_template
from ccavutil import encrypt,decrypt
from ccavResponseHandler import res
from string import Template
from waitress import serve

app = Flask('ccavRequestHandler') 

@app.route('/')
def webprint():
    return render_template('dataForm.html')

@app.route('/ccavResponseHandler', methods=['GET', 'POST'])
def ccavResponseHandler():
    
    workingKey = 'F5D6C4A0155454refedfertrtrB72336ECB'
    workingKey2 = 'F5D6C4A01508C64EEF91EBDB72336ECB'
    
    selected_working_key = 'F5D6C4A01508C64EEF91EBDB72336ECB'      
    
    if selected_working_key == workingKey:
               
        plainText = res(request.form['encResp'],workingKey)
        print(request.form['encResp'])	       
        print("Output with workingKey:", workingKey)
        return plainText
    elif selected_working_key == workingKey2:        
        plainText = res(request.form['encResp'],workingKey2)
        print(request.form['encResp'])	       
        print("Output with workingKey2:", workingKey2)
        return plainText
    else:
        print("Invalid working key selection")
       


# 	p_merchant_id = request.form['merchant_id']
# 	p_order_id = request.form['order_id']
# 	p_currency = request.form['currency']
# 	p_amount = request.form['amount']
# 	p_redirect_url = request.form['redirect_url']
# 	p_cancel_url = request.form['cancel_url']
# 	p_language = request.form['language']
# 	p_billing_name = request.form['billing_name']
# 	p_billing_address = request.form['billing_address']
# 	p_billing_city = request.form['billing_city']
# 	p_billing_state = request.form['billing_state']
# 	p_billing_zip = request.form['billing_zip']
# 	p_billing_country = request.form['billing_country']
# 	p_billing_tel = request.form['billing_tel']
# 	p_billing_email = request.form['billing_email']
# 	p_delivery_name = request.form['delivery_name']
# 	p_delivery_address = request.form['delivery_address']
# 	p_delivery_city = request.form['delivery_city']
# 	p_delivery_state = request.form['delivery_state']
# 	p_delivery_zip = request.form['delivery_zip']
# 	p_delivery_country = request.form['delivery_country']
# 	p_delivery_tel = request.form['delivery_tel']
# 	p_merchant_param1 = request.form['merchant_param1']
# 	p_merchant_param2 = request.form['merchant_param2']
# 	p_merchant_param3 = request.form['merchant_param3']
# 	p_merchant_param4 = request.form['merchant_param4']
# 	p_merchant_param5 = request.form['merchant_param5']
# 	p_promo_code = request.form['promo_code']
# 	p_customer_identifier = request.form['customer_identifier']




if __name__ == '__main__':
    # app.run(host = '127.0.0.1', debug = True, port = 8080)
    serve(app, host='0.0.0.0', port=5000, debug = True, url_scheme='https')




