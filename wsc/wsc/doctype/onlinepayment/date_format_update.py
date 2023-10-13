import frappe
from datetime import datetime
def execute():
    date_format()


def date_format():
    data = frappe.get_all("OnlinePayment",
                          filters={'date_time_of_transaction': ('!=', None)},
                          fields=['name', 'date_time_of_transaction'])
   
    
    if data:
        for entry in data:
            doc=frappe.get_doc("OnlinePayment",entry["name"])   
            # print("doc:::::",doc) 
            transaction_time = entry['date_time_of_transaction']
            # print(f"Old date format {entry['name']}: {transaction_time}")

            try:
               
                new_date = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                try:
                    
                    new_date = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                   
                    new_date = datetime.strptime(transaction_time, "%m/%d/%Y %H:%M:%S")
          
            new_date_string = new_date.strftime("%Y-%m-%d %H:%M:%S")
            doc.date_time_of_transaction=new_date_string
            doc.save(ignore_permissions=True)
            doc.submit()
            # print(f"New date format {entry['name']}: {new_date_string}")
            # print("\n\n\n\n")
    else:
        print("No data found with a valid 'date_time_of_transaction'.")

