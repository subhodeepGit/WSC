# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FixedDeposit(Document):
    pass

@frappe.whitelist()
def calculate_fd(fd_amount=None, interest_rate=None, interest_payable=None,interest_type=None,days=None,weeks=None,months=None,quarterly=None,semi_annually=None,annually=None):
    print("\n\n\n\n")
    fd_amount=float(fd_amount)
    interest_rate=float(interest_rate)
    days=float(days)
    weeks=float(weeks)
    months=float(months)
    quarterly=float(quarterly)
    semi_annually=float(semi_annually)
    annually=float(annually)

 
    if interest_type=="Simple":
        interest_rate = interest_rate / 100  # Convert percentage to decimal
        if interest_payable == "Days":
            time = days/365
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time)
        
        if interest_payable == "Weeks":
            time = weeks/52
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time)
        
        if interest_payable == "Months":
            time = months/12
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time)

        if interest_payable == "Quarterly":
            time = quarterly/4
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time)

        if interest_payable == "Semi-Annually":
            time = semi_annually/6
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time)

        if interest_payable == "Annually":
            time = annually
            maturity_amount = calculate_simple_interest(fd_amount,interest_rate,time)
    
        return maturity_amount

    if interest_type=="Compound":
        pass


    # Days
    # Weeks
    # Months
    # Quarterly
    # Semi-Annually
    # Annually

def calculate_simple_interest(principal,rate,time):
    amount=0.0
    amount = principal*(1+(rate*time))
    return round(amount,2)