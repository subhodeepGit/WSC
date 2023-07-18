# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

class FixedDeposit(Document):
    def validate(self):
        self.maturity_date_calculate()


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
        


@frappe.whitelist()
def calculate_fd(fd_amount=None, interest_rate=None, interest_payable=None,interest_type=None,days=None,
                    weeks=None,months=None,quarterly=None,semi_annually=None,annually=None):
    fd_amount=float(fd_amount)
    interest_rate=float(interest_rate)
    days=float(days)
    weeks=float(weeks)
    months=float(months)
    quarterly=float(quarterly)
    semi_annually=float(semi_annually)
    annually=float(annually)

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
        pass




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


def calculate_compound_interest(principal, rate, time):
 
    # Calculates compound interest
    Amount = principal * (pow((1 + rate / 100), time))
    CI = Amount - principal
    print("Compound interest is", CI)