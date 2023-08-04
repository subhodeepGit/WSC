# database_operations.py

import os
import json
import pymysql
import frappe

# def fetch_and_process_data():
#     username = os.getenv('USER') 
#     site_name = frappe.local.site   
#     file_path = os.path.join("/home", username, "frappe-bench", "sites", site_name, "site_config.json")
#     with open(file_path, "r") as file:
#         config_data = json.load(file)
#     db_name = config_data["db_name"]
#     file_path = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "hdfcpaymentintegration", "db_name.txt")
#     with open(file_path, "w") as file:
#         file.write(db_name) 
#     try:
#         conn = pymysql.connect(
#             host="localhost",
#             user="integration",
#             password="erp@123",
#             database=db_name)
#         c = conn.cursor()
#         return c

#     except pymysql.Error as e:
#         print("Error connecting to the database:", e)

# # Run the fetch_and_process_data function when the file is executed directly
# if __name__ == "__main__":
#     fetch_and_process_data()

def fetch_and_process_data(site_name):
    username = os.getenv('USER')
    
    # Construct the file paths
    site_config_file_path = os.path.join("/home", username, "frappe-bench", "sites", site_name, "site_config.json")
    db_name_file_path = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "hdfcpaymentintegration", "db_name.txt")
    
    try:
        # Read the site configuration
        with open(site_config_file_path, "r") as config_file:
            config_data = json.load(config_file)
        db_name = config_data["db_name"]
        
        # Write the db_name to the file
        with open(db_name_file_path, "w") as db_name_file:
            db_name_file.write(db_name)
            
        # Connect to the database
        conn = pymysql.connect(
            host="localhost",
            user="integration",
            password="erp@123",
            database=db_name)
        c = conn.cursor()
        return c

    except Exception as e:
        print(f"Error processing data for site {site_name}: {e}")
        return None

if __name__ == "__main__":
    site_names = frappe.get_all("Site", filters={"enabled": 1}, pluck="name")
    print("\n\n\n\n",site_names)
    for site_name in site_names:
        if site_name == "site_name_1":
            # Process data for site_name_1
            cursor = fetch_and_process_data(site_name)
            if cursor:
                # Call additional functions for site_name_1
                pass  # Your code here
        elif site_name == "erp.soulunileaders.com":
            # Process data for site_name_2
            cursor = fetch_and_process_data(site_name)
            if cursor:
                # Call additional functions for site_name_2
                pass  # Your code here
        else:
            # Default data processing for other sites
            cursor = fetch_and_process_data(site_name)
            if cursor:
                # Call additional functions for other sites
                pass  # Your code here
