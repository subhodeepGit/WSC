# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

class FixedDeposit(Document):
    def validate(self):
        self.maturity_date_calculate()

    def on_submit(self):
        je_pay(self)  

    def on_cancel(self):
        if self.matured==0 and self.matured_posting_journal_entry:
            cancel_doc = frappe.get_doc("Journal Entry",self.posting_journal_entry)
            cancel_doc.cancel()
        else:
            frappe.throw("Already Maturity Posting Is Completed")

    def on_update_after_submit(self):
        if not self.matured_posting_journal_entry:
            matured_je_pay(self)
        else:
            frappe.throw("Already Posting Is Completed")                

    def maturity_date_calculate(self):
        interest_payable=self.interest_payable
        if interest_payable=="Days":
            fd_start_date=datetime.strptime(self.fd_start_date, '%Y-%m-%d').date()
            tenure_days=int(self.tenure_days)
            self.maturity_date=fd_start_date + timedelta(days=tenure_days)
        elif interest_payable=="Weeks":
            fd_start_date=datetime.strptime(self.fd_start_date, '%Y-%m-%d').date()
            tenure_days=int(self.tenurein_weeks)*7
            self.maturity_date=fd_start_date + timedelta(days=tenure_days)
        elif interest_payable=="Months":
            fd_start_date=datetime.strptime(self.fd_start_date, '%Y-%m-%d').date()
            tenurein_months=int(self.tenurein_months)
            self.maturity_date=fd_start_date + relativedelta(months=tenurein_months)
        elif interest_payable=="Quarterly":
            fd_start_date=datetime.strptime(self.fd_start_date, '%Y-%m-%d').date()
            tenurein_months=int(self.tenurein_quarter)*3
            self.maturity_date=fd_start_date + relativedelta(months=tenurein_months)
        elif interest_payable=="Semi-Annually":
            fd_start_date=datetime.strptime(self.fd_start_date, '%Y-%m-%d').date()
            tenurein_months=int(self.tenuresemi_annually)*6
            self.maturity_date=fd_start_date + relativedelta(months=tenurein_months)
        elif interest_payable=="Annually":
            fd_start_date=datetime.strptime(self.fd_start_date, '%Y-%m-%d').date()
            tenurein_months=int(self.tenurein_annually)*12
            self.maturity_date=fd_start_date + relativedelta(months=tenurein_months)


def matured_je_pay(self):
    je = frappe.new_doc("Journal Entry")
    je.posting_date = self.posting_date
    je.append("accounts",{
    'account' : self.bank_account,
    'debit_in_account_currency' :self.final_maturity_amount,
    })
    je.append("accounts",{
    'account' : self.fd_account,
    'credit_in_account_currency' : self.fd_amount,
    })
    je.append("accounts",{
    'account' : self.interest_account,
    'credit_in_account_currency' : self.final_maturity_interest_amount,
    })
    je.save()
    je.submit()
    frappe.db.set_value("Fixed Deposit",self.name,"matured_posting_journal_entry",je.name)

def je_pay(self):
    je = frappe.new_doc("Journal Entry")
    je.posting_date = self.posting_date
    je.append("accounts",{
    'account' : self.bank_account,
    'credit_in_account_currency' : self.fd_amount,
    })
    je.append("accounts",{
    'account' : self.fd_account,
    'debit_in_account_currency' :self.fd_amount,
    })
    je.save()
    je.submit()
    # self.posting_journal_entry=je.name
    frappe.db.set_value("Fixed Deposit",self.name,"posting_journal_entry",je.name)

@frappe.whitelist()
def calculate_fd(fd_amount=None, interest_rate=None, interest_payable=None,interest_type=None,days=None,
                    weeks=None,months=None,quarterly=None,semi_annually=None,annually=None):
    fd_amount=float(fd_amount)
    interest_rate=float(interest_rate)
    if days:
        days=int(days)
    if weeks:  
        weeks=int(weeks)
    if months:
        months=int(months)
    if quarterly:    
        quarterly=int(quarterly)
    if semi_annually:    
        semi_annually=int(semi_annually)
    if annually:    
        annually=int(annually)

    maturity_amount=[]
    if interest_type=="Simple":
        interest_rate = interest_rate / 100  # Convert percentage to decimal
        if interest_payable == "Days":
            time = days
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Weeks":
            time = weeks
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Months":
            time = months
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Quarterly":
            time = quarterly
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Semi-Annually":
            time = semi_annually
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Annually":
            time = annually
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time,interest_payable)
        total_si=0    
        for t in maturity_amount:
            total_si +=t['interest']
        fd_amount=fd_amount+total_si
        return {"maturity_amount":maturity_amount,"grand_maturity_amount":fd_amount}

    if interest_type=="Compound":
        if interest_payable == "Annually":
            time = annually
            maturity_amount = calculate_compound_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Days":
            time = days
            maturity_amount = calculate_compound_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Weeks":
            time = weeks
            maturity_amount = calculate_compound_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Months":
            time = months
            maturity_amount = calculate_compound_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Quarterly":
            time = quarterly
            maturity_amount = calculate_compound_interest(fd_amount,interest_rate,time,interest_payable)
        if interest_payable == "Semi-Annually":
            time = semi_annually
            maturity_amount = calculate_compound_interest(fd_amount,interest_rate,time,interest_payable)                           
        fd_amount=0
        for t in maturity_amount:
            fd_amount=t['total']    
        return {"maturity_amount":maturity_amount,"grand_maturity_amount":fd_amount}    




def calculate_simple_interest(principal,rate,time,interest_payable):
    maturity_amount=[]
    for t in range(0,int(time)):
        data={}
        data['term']="Term-%s"%(t+1)
        data["principal_amount"]=principal
        si = (principal * 1 * rate)/100
        data['interest']=si
        data['total']=principal+si
        maturity_amount.append(data)
    return maturity_amount


def calculate_compound_interest(principal, rate, time,interest_payable):
    list_of_int=[]
    last_data={}
    for t in range(time):
        data_info={}
        if not last_data:
            # Calculates compound interest for fast term
            time_value=1
            Amount = principal * (pow((1 + rate / 100), time_value))
            CI = Amount - principal
            data_info['term']="Team-%s"%(t+1)
            data_info['principal_amount']=principal
            data_info['interest']=round(CI,2)
            data_info['total']=round(Amount,2)
            last_data=data_info
            list_of_int.append(data_info)
        else:
            # Calculates compound interest for the rest of temm
            time_value=1
            principal=principal+last_data['interest']
            Amount = principal * (pow((1 + rate / 100), time_value))
            CI = Amount - principal
            data_info['term']="Team-%s"%(t+1)
            data_info['principal_amount']=principal
            data_info['interest']=round(CI,2)
            data_info['total']=round(Amount,2)
            last_data=data_info
            list_of_int.append(data_info)
    return  list_of_int